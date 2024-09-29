import * as http from "http";

import ResolvedData from "../type/ResolvedData";
import { Parameter } from "../type/Parameter";

/**
 * 
 * 사용자의 특수 URL 입력을 처리하는 라우터입니다
 * 
 * @author Hvckless
 */
class URLResolver{
    private protectedDOC:string = "protected";
    public isRequest(url:string):boolean{
        if(url.split("/")[1]==this.protectedDOC){
            return true;
        }
        return false;
    }
    public isProtected(url:string):boolean{
        if(url.split("/").includes(this.protectedDOC)){
            return true;
        }
        return false;
    }
    public resolveData(res:http.ServerResponse<http.IncomingMessage>, url:string, param?:Parameter):ResolvedData{

        let queryString:string = url.split("/")[2];

        console.log("쿼리 스트링 출력");
        console.log(queryString);
        console.log(param);


        return null;
    }

}

export default URLResolver;