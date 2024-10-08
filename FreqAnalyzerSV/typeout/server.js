import * as http from "http";
import * as fs from "fs";
import * as mime from "mime-types";
import URLRedirector from "./utils/url/URLRedirector.js";
import URLResolver from "./utils/url/URLResolver.js";
import ParameterResolver from "./utils/url/ParameterResolver.js";
const urlResolver = new URLResolver();
const parameterResolver = new ParameterResolver();
const server = http.createServer((req, res) => {
    if (req.url == "/") {
        new URLRedirector().redirect(res, '/src/html/index.html');
        return;
    }
    /**
     * HTTP 서버가 내부적으로 사용하는 파일 전송 함수
     * 파일 데이터와 파일 타입을 첨부하여 사용자에게 전달한다
     * @param res 응답 받을 클라이언트
     * @param filepath 파일 경로
     */
    const sendFile = (res, filepath) => {
        fs.readFile(filepath, (error, data) => {
            if (error) {
                console.error("Failed to read file:", error);
                res.writeHead(500, { 'Content-Type': 'text/plain' });
                res.end("Internal Server Error");
                return;
            }
            let fileExtension = mime.lookup(filepath.split("/")[(filepath.split("/").length - 1)].split("?")[0]) + "";
            console.log(filepath + " / " + fileExtension);
            res.writeHead(200, {
                'Content-Type': fileExtension,
                'Cache-Control': 'no-cache'
            });
            res.end(data);
        });
    };
    /**
     * HTTP 서버가 내부적으로 버퍼를 전송하는 함수
     * API 요청을 통해 바이너리 버퍼를 사용자에게 전달한다
     * @param res
     * @param buffer
     */
    const sendBuffer = (res, json) => {
        res.writeHead(200, {
            'Content-Type': 'text/json; charset=utf-8',
            'Cache-Control': 'no-cache'
        });
        res.write(JSON.stringify(json));
        res.end();
    };
    let urlstruct = req.url.split("?");
    let url = urlstruct[0];
    /**
     *
     * 파레메터는 키:값 JSON의 배열이다
     */
    let param = null;
    if (urlstruct.length > 1) {
        param = parameterResolver.resolveParameter(urlstruct[1]);
    }
    let body = "";
    if (req.method == "POST") {
        req.on('data', (data) => {
            body += data;
        });
        req.on('end', () => {
            console.log("포스트 데이터 : " + body);
            param = JSON.parse(body);
            fs.stat("." + url, (error, stats) => {
                if (urlResolver.isRequest(url)) {
                    urlResolver.resolveData(res, url, param)
                        .then((data) => {
                        sendBuffer(res, data);
                    })
                        .catch((error) => {
                        console.error(error);
                        sendFile(res, "./src/html/fallback/nourl.html");
                    });
                    return;
                }
                else {
                    sendFile(res, "./src/html/fallback/nourl.html");
                    return;
                }
            });
        });
    }
    if (req.method == "GET") {
        fs.stat("." + url, (error, stats) => {
            /**
             * 아직 완전하지 않은 기능. protected로 요청하지 마시오
             */
            if (urlResolver.isRequest(url)) {
                //sendBuffer(res, urlResolver.resolveData(res, url, param)[0]);
                urlResolver.resolveData(res, url, param)
                    .then((data) => {
                    sendBuffer(res, data);
                })
                    .catch((error) => {
                    console.error(error);
                    sendFile(res, "./src/html/fallback/nourl.html");
                });
                return;
            }
            /**
             * 사용자가 protected된 리소스에 요청하려 할 때 요청을 드랍합니다
             */
            if (urlResolver.isProtected(url)) {
                sendFile(res, "./src/html/fallback/requesterr.html");
                return;
            }
            if (stats == undefined) {
                console.log("NO FILE : " + url);
                sendFile(res, "./src/html/fallback/nourl.html");
            }
            else {
                if (stats.isFile()) {
                    sendFile(res, "." + url);
                }
                else {
                    console.log("NO FILE : " + url);
                    sendFile(res, "./src/html/fallback/nourl.html");
                }
            }
        });
    }
});
server.listen(5000);
