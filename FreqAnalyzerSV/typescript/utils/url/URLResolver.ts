import * as http from "http";

import ResolvedData from "../type/ResolvedData";

/**
 * 
 * 사용자의 특수 URL 입력을 처리하는 라우터입니다
 * 
 * @author Hvckless
 */
class URLResolver{
    public isValid(url:string):boolean{
        if(url.split("/")[1]=="protected"){
            return true;
        }
        return false;
    }
    public resolveData(res:http.ServerResponse<http.IncomingMessage>, url:string, param?:string):ResolvedData{

        let queryString:string = url.split("/")[2];

        console.log("쿼리 스트링 출력");
        console.log(queryString);


        return null;
    }

}

export default URLResolver;