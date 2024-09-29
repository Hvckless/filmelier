import * as http from "http";
import * as fs from "fs";
const server = http.createServer((req, res) => {
    if (req.url.split("/").length > 1) {
        const moviename = req.url.split("/")[1];
        const path = `./src/image/ignore/${moviename}.jfif`;
        try {
            const file = fs.readFileSync(path);
            res.write(file);
        }
        catch (error) {
            res.write("this is not file");
        }
    }
    res.end();
});
server.listen(80);
