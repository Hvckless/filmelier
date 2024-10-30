import * as http from "http";
import WebSocket from "ws";
import express from "express";
class Main {
    constructor() {
        this.webexpress = express();
        this.webexpress.use("/public", express.static(__dirname + "/public"));
        const webserver = http.createServer(this.webexpress);
        webserver.listen(8080);
        this.websocket = new WebSocket.Server({ webserver });
    }
}
let app = new Main();
