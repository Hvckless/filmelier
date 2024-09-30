// import fs from "fs";
// import path from "path";
// @ts-ignore
// import db from "../config/mysql";

import fs from "fs";
import path from "path";

import Mysql from "./config/mysql";

//import db from "../config/mysql.js";

let db = new Mysql();

//const fs = require("fs");
//const path = require("path");
//const db = require("../config/mysql.js");

const conn = db.init();
//
// const movieNamePath = path.resolve(__dirname, "../../Crawling/crawling/movie_list.txt");
// const imagesDir = path.resolve(__dirname, "../../Crawling/crawling/image");


const movieNamePath = "../Crawling/crawling/movie_list.txt";
const imagesDir = "../Crawling/crawling/image";

const movieNames:string[] = fs.readFileSync(movieNamePath, 'utf-8').split('\n').map((name:string) =>name.trim());

movieNames.forEach((movieNames: string) => {
    const imagePath = path.join(imagesDir, `${movieNames}.jpg`);
    if (fs.existsSync(imagePath)){
        const image = fs.readFileSync(imagePath);
        const imageBase64 = image.toString('base64');

        const sql = 'insert into movie_info(movie_name,movie_image) values (?, ?)';
        conn.query(sql, [movieNames, image], (err: Error, result: any) =>{
            if (err) throw err;
            console.log(`${movieNames} 데이터 업로드 완료`);
        });
    } else {
        console.log(`${movieNames} 가 존재하지 않습니다`);
    }
});

conn.end();