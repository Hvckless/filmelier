import * as http from "http";
import { WebSocketServer } from 'ws';
import express from "express";
class Main {
    constructor() {
        this.webexpress = express();
        this.webexpress.use("/", express.static("./src/html"));
        this.webexpress.use("/src", express.static("./src"));
        this.webexpress.use("/typeout", express.static("./typeout"));
        let webserver = http.createServer(this.webexpress);
        webserver.listen(8080);
        let socketserver = http.createServer(this.socketexpress);
        socketserver.listen(8081);
        this.websocket = new WebSocketServer({ server: socketserver });
    }
}
let app = new Main();
app.websocket.on('connection', (ws) => {
    console.log("새 클라이언트 연결됨");
    ws.on('message', (message) => {
        console.log("CLIENT SENT : " + message);
    });
    ws.on('close', () => {
        console.log("client closed");
    });
});
