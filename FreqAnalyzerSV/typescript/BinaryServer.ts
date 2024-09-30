import * as http from "http";
import * as fs from "fs";



const server:http.Server = http.createServer((req:http.IncomingMessage, res:http.ServerResponse<http.IncomingMessage>)=>{

    if(req.url.split("/").length > 1){

        const moviename = req.url.split("/")[1];

        const path = `./src/image/ignore/${moviename}.jfif`;

        try{
            const file:Buffer = fs.readFileSync(path);

            res.write(file);
        }catch(error){
            res.write("this is not file");
        }
        

        
    }

    res.end();

});

server.listen(80);