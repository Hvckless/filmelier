import * as fs from "fs";
import * as mime from "mime-types";
class FileHandler {
    sendFile(res, filepath) {
        fs.readFile(filepath, 'utf-8', (error, data) => {
            if (error) {
                console.error("Failed to read file", error);
            }
            return data;
        });
    }
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
