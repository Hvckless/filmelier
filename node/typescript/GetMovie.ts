import fs from "fs";
import path from "path";

import Mysql from "./config/mysql.js";

interface movieCallback {(err: Error | null, result ?: any):void}

class GetMovie {
    private conn: any;

    constructor() {
        const db = new Mysql();
        this.conn = db.init();
    }

    public getMovieInfo(movieName: string, callback:movieCallback):void {
        const sql = 'select movie_name, movie_image from movie_info where movie_name like ?';
        const queryParam = `%${movieName}%`; // 부분 일치 검색

        this.conn.query(sql, queryParam, (err: Error, results: any) =>{
            if (err) {
                return callback(err); // 오류 발생 시 콜백 으로 전달
            }

            if (results.length > 0 ) {
                // 영화 이름과 이미지를 객체 배열로 생성
                const moviesInfo = results.map((row: any) =>({
                    name: row.movie_name,
                    image: row.movie_image,
                }));

                // 객체 배열을 콜백으로 전달
                callback(null, moviesInfo); // [{ name: "마션", image: "마션.jsp"}...]
            } else {
                callback(new Error("해당하는 영화를 찾을 수 없습니다"));
            }

        })
    }


}

export default GetMovie;

/*
let db = new Mysql()
const conn = db.init()

// 값을 err 또는 null,result 로 전달
// err 가 안뜨면 null 을 반환, result 와 함께 반환 한다.
// err 가 뜨면 result 를 반환 하지 않기 위해 result? 를 사용
export const getMovieInfo = (movieName: string, callback : (err: Error | null, result ?: any) => void)=>{
    const sql = 'select movie_name, movie_image from movie_info where movie_name like ?';
    const queryParam = `%${movieName}%`; // 부분 일치 검색

    conn.query(sql, [queryParam], (err: Error, results: any) =>{
        if (err) {
            return callback(err); // 오류 발생 시 콜백 으로 전달
        }

        if (results.length > 0 ) {
            // 영화 이름과 이미지를 객체 배열로 생성
            const moviesInfo = results.map((row: any) =>({
                name: row.movie_name,
                image: row.movie_image,
            }));

            // 객체 배열을 콜백으로 전달
            callback(null, moviesInfo); // [{ name: "마션", image: "마션.jsp"}...]
        } else {
            callback(new Error("해당하는 영화를 찾을 수 없습니다"));
        }

    })
}
*/