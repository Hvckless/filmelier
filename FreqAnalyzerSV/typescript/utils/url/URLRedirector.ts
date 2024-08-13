import * as http from "http";

class URLRedirector{
    redirect(res:http.ServerResponse<http.IncomingMessage>, targetURL:string):void{
        res.writeHead(302, {
            'Location': targetURL
          });
        res.end();
        return;
    }
}

export default URLRedirector;