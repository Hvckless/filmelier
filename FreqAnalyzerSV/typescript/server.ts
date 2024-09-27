import * as http from "http";
import * as fs from "fs";
import * as mime from "mime-types";

import URLRedirector from "./utils/url/URLRedirector.js";
import URLResolver from "./utils/url/URLResolver.js";

const urlResolver:URLResolver = new URLResolver();

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

    /**
     * HTTP 서버가 내부적으로 버퍼를 전송하는 함수
     * API 요청을 통해 바이너리 버퍼를 사용자에게 전달한다
     * @param res 
     * @param buffer 
     */
    const sendBuffer = (res:http.ServerResponse<http.IncomingMessage>, buffer:Buffer):void=>{
        res.writeHead(200,
            {
                'Content-Type': 'image/jpeg',
                'Cache-Control': 'no-cache'
            }
        )
        res.end(buffer);
    }

    let urlstruct:Array<string> = req.url.split("?");

    let url:string = urlstruct[0];
    let param:string = null;

    if(urlstruct.length > 1){
        param = urlstruct[1];
    }

    fs.stat("."+url, (error:NodeJS.ErrnoException, stats:fs.Stats)=>{

        /**
         * 아직 완전하지 않은 기능. protected로 요청하지 마시오
         */
        if(urlResolver.isValid(url)){
            sendBuffer(res, urlResolver.resolveData(res, url, param)[0]);
            return;
        }



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

server.listen(5000);