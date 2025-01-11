import * as http from "http";
import * as https from "https";
import * as fs from "fs";

const key = fs.readFileSync('./src/protected/privkey.pem');
const cert = fs.readFileSync('./src/protected/fullchain.pem');

//const server:https.Server = https.createServer
const server:http.Server = http.createServer((req, res)=>{
    console.log("어떤 커넥션 발생");
    res.write("HELLO");
    res.end();
});

const SSLServer:https.Server = https.createServer({key: key, cert: cert}, (req:http.IncomingMessage, res:http.ServerResponse<http.IncomingMessage>)=>{
    console.log("어떤 SSL 커넥션 발생");
    res.write("SSL Conn");
    res.end();
});

server.listen(80);
SSLServer.listen(443);