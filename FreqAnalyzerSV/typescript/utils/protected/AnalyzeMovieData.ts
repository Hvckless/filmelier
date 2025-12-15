import JSONObject from "../type/JSONObject";
import { Parameter } from "../type/Parameter";
import Protect from "./Protect";
import * as path from "path";
import { ChildProcess, spawn } from "child_process";
import PythonRunner from "../process/PythonRunner";
import PythonProcess from "../process/PythonProcess.js";

class AnalyzeMovieData implements Protect, PythonRunner{
    private python_process:ChildProcess | null = null;
    constructor() { }//this.python_process = PythonProcess.instance.python_process;
    async execute(param: Parameter): Promise<string> {
        return new Promise((resolve, reject)=>{

            let newdata:string = "HELLo";

            resolve(newdata);
        });
    }
    async initial(param: Parameter): Promise<JSONObject> {
        return new Promise(async (resolve, reject)=>{

            this.python_process = PythonProcess.instance.python_process;

            let obj_keys:Array<string> = Object.keys(param);
            let movie_name_list:string = "[";

            for(let i = 0; i < obj_keys.length; i++){
                movie_name_list += `'${decodeURIComponent(obj_keys[i])}'`;

                if(i != (obj_keys.length - 1)){
                    movie_name_list += ',';
                }
            }

            movie_name_list += "]";

            if (obj_keys.length > 0) {
                console.log(`Python으로 전송: ${movie_name_list}`);

                try{
                    const result:string = await PythonProcess.instance.execute(movie_name_list);

                    resolve({"reqMsg": result});
                }catch(err){
                    console.error(`처리 실패 : ${err}`);
                    reject({ "reqMsg": `파싱 에러: ${err}` });
                }


            } else {
                reject({ "reqMsg": "parameter does not exist" });
            }
        });
    }

}

export default AnalyzeMovieData;