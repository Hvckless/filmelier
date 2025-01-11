import * as http from "http";
import * as fs from "fs";

import * as mime from "mime-types";
import WebSocket from "ws";
import express from "express";

import URLRedirector from "./backend/utils/url/URLRedirector";

const server:http.Server = http.createServer((req:http.IncomingMessage, res:http.ServerResponse<http.IncomingMessage>)=>{

    if(req.url == "/"){
        new URLRedirector().redirect(res, '/src/html/index.html');
        return;
    }

    /**
     * HTTP 서버가 내부적으로 사용하는 파일 전송 함수
     * 파일 데이터와 파일 타입을 첨부하여 사용자에게 전달한다
     * @param res 응답 받을 클라이언트
     * @param filepath 파일 경로
     */
    const sendFile = (res:http.ServerResponse<http.IncomingMessage>, filepath:string):void=>{
        fs.readFile(filepath, (error:NodeJS.ErrnoException, data:Buffer)=>{

            if (error) {
                console.error("Failed to read file:", error);
                res.writeHead(500, { 'Content-Type': 'text/plain' });
                res.end("Internal Server Error");
                return;
            }

            
            let fileExtension = mime.lookup(filepath.split("/")[(filepath.split("/").length - 1)].split("?")[0])+"";
            console.log(filepath + " / " + fileExtension);
            res.writeHead(200, 
                {
                    'Content-Type': fileExtension,
                    'Cache-Control': 'no-cache'
                }
            )
            res.end(data);
        });
    }

    let url:string = req.url;

    fs.stat("."+url, (error:NodeJS.ErrnoException, stats:fs.Stats)=>{
        if(stats == undefined){
            console.log("NO FILE : " + url);
            sendFile(res, "./src/html/fallback/nourl.html");
        }else{
            if(stats.isFile()){
                sendFile(res, "."+url);
            }else{
                console.log("NO FILE : " + url);
                sendFile(res, "./src/html/fallback/nourl.html");
            }
        }
    });
});

server.listen(8080);



class Main{
    express:express;
    websocket:any;
    constructor(){
        this.express = express();
        let http_server:http.Server = http.createServer(this.express);
        http_server.listen(8081);
        this.websocket = new WebSocket.Server({http_server})
    }
}

let app:Main = new Main();