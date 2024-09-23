import * as http from "http"
import * as fs from "fs"
import * as mime from "mime-types"

class FileHandler{
    public sendFile(res:http.ServerResponse<http.IncomingMessage>, filepath:string):void{
        fs.readFile(filepath, 'utf-8', (error:NodeJS.ErrnoException, data:Buffer):Buffer=>{


            if(error){
                console.error("Failed to read file", error);
            }


            return data;
        });
    }
}


const sendFile = (res:http.ServerResponse<http.IncomingMessage>, filepath:string):void=>{
    fs.readFile(filepath, 'utf-8', (error:NodeJS.ErrnoException, data:Buffer)=>{

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