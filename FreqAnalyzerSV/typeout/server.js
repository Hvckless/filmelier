import * as http from "http";
import * as fs from "fs";
import * as mime from "mime-types";
import URLRedirector from "./utils/url/URLRedirector.js";
const server = http.createServer((req, res) => {
    if (req.url == "/") {
        new URLRedirector().redirect(res, '/src/html/index.html');
        return;
    }
    const sendFile = (res, filepath) => {
        fs.readFile(filepath, 'utf-8', (error, data) => {
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
    fs.stat("." + req.url, (error, stats) => {
        if (stats == undefined) {
            console.log("NO FILE : " + req.url);
            sendFile(res, "./src/html/fallback/nourl.html");
        }
        else {
            if (stats.isFile()) {
                sendFile(res, "." + req.url);
            }
            else {
                console.log("NO FILE : " + req.url);
                sendFile(res, "./src/html/fallback/nourl.html");
            }
        }
    });
});
server.listen(5000);
