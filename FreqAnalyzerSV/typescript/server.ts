import * as http from "http";
import * as https from "https";
import * as fs from "fs";
import * as mime from "mime-types";

import URLRedirector from "./utils/url/URLRedirector.js";
import URLResolver from "./utils/url/URLResolver.js";
import ParameterResolver from "./utils/url/ParameterResolver.js";

import { Parameter } from "./utils/type/Parameter.js";
import JSONObject from "./utils/type/JSONObject.js";

const urlResolver:URLResolver = new URLResolver();
const parameterResolver:ParameterResolver = new ParameterResolver();

const key = fs.readFileSync('./src/protected/privkey.pem');
const cert = fs.readFileSync('./src/protected/fullchain.pem');

const server:https.Server = https.createServer({key: key, cert: cert}, (req:http.IncomingMessage, res:http.ServerResponse<http.IncomingMessage>)=>{
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
    const sendBuffer = (res:http.ServerResponse<http.IncomingMessage>, json:JSONObject):void=>{
        res.writeHead(200,
            {
                'Content-Type':'text/json; charset=utf-8',
                'Cache-Control': 'no-cache'
            }
        )
        res.write(JSON.stringify(json));
        res.end();
    }

    let urlstruct:Array<string> = req.url.split("?");

    let url:string = urlstruct[0];

    /**
     * 
     * 파레메터는 키:값 JSON의 배열이다
     */
    let param:Parameter = null;

    if(urlstruct.length > 1){
        param = parameterResolver.resolveParameter(urlstruct[1]);
    }

    let body:string = "";

    if(req.method == "POST"){
        req.on('data',(data)=>{
            body += data;
        });
        req.on('end', ()=>{
            console.log("포스트 데이터 : " + body);
            param = JSON.parse(body);

            fs.stat("."+url, (error:NodeJS.ErrnoException, stats:fs.Stats)=>{
                if(urlResolver.isRequest(url)){
                    urlResolver.resolveData(res, url, param)
                        .then((data)=>{
                            sendBuffer(res, data);
                        })
                        .catch((error)=>{
                            console.error(error);
                            sendFile(res, "./src/html/fallback/nourl.html");
                        });
                    
                    return;
                }else{
                    sendFile(res, "./src/html/fallback/nourl.html");
                    return;
                }
            });
        });
    }

    if(req.method == "GET"){
        fs.stat("."+url, (error:NodeJS.ErrnoException, stats:fs.Stats)=>{

            /**
             * 아직 완전하지 않은 기능. protected로 요청하지 마시오
             */
            if(urlResolver.isRequest(url)){
                //sendBuffer(res, urlResolver.resolveData(res, url, param)[0]);
                urlResolver.resolveData(res, url, param)
                    .then((data)=>{
                        sendBuffer(res, data);
                    })
                    .catch((error)=>{
                        console.error(error);
                        sendFile(res, "./src/html/fallback/nourl.html");
                    });
                
                return;
            }
    
            /**
             * 사용자가 protected된 리소스에 요청하려 할 때 요청을 드랍합니다
             */
            if(urlResolver.isProtected(url)){
                sendFile(res, "./src/html/fallback/requesterr.html");
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
    }



    
});

server.listen(443);