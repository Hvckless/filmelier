import { Parameter } from "../type/Parameter";

class ParameterResolver{
    public resolveParameter(urlContext:string):Parameter{

        let result:Parameter = {};

        urlContext.split("&").forEach((param:string):void=>{

            let paramFragment:Array<string> = param.split("=");

            if(paramFragment.length != 2){
                throw new Error("parameter is not constructed correctly." + ` parameter : ${urlContext}`);
            }else{
                result[paramFragment[0]] = paramFragment[1];
            }
        });



        return result;

    }
}

export default ParameterResolver;