import JSONObject from "../type/JSONObject";
import { Parameter } from "../type/Parameter";
import Protect from "./Protect";
import * as path from "path";
import { spawn } from "child_process";
import PythonRunner from "../process/PythonRunner";

class AnalyzeMovieData implements Protect, PythonRunner{
    private python_process: any;

    constructor() {
        // 서버 시작 시 파이썬 프로세스 생성
        const python_exec:string = path.resolve(process.cwd(), "../NLPyCodes/OOP/venv/bin/python");
        const pcs_path:string = path.resolve(process.cwd(), '../NLPyCodes/OOP/similarity.py');

        this.python_process = spawn(python_exec, [pcs_path], {
            cwd: path.resolve(process.cwd(), '../NLPyCodes/OOP'),
            stdio: ['pipe','pipe','pipe']
        });

        // 에러 발생 시 처리
        this.python_process.stderr.on('data', (data) => {
            console.error(`파이썬 에러: ${data.toString()}`);
        });

        // 종료시 처리
        this.python_process.on('close', (code) => {
            console.log(`파이썬 프로세스 종료 ${code}`);
        });
    }
    async execute(param: Parameter): Promise<string> {
        return new Promise((resolve, reject)=>{

            let newdata:string = "HELLo";

            resolve(newdata);
        });
    }
    async initial(param: Parameter): Promise<JSONObject> {
        return new Promise(async (resolve, reject)=>{

            let obj_keys:Array<string> = Object.keys(param);
            let movie_name_list:string = "[";

            for(let i = 0; i < obj_keys.length; i++){
                movie_name_list += `'${obj_keys[i]}'`;

                if(i != (obj_keys.length - 1)){
                    movie_name_list += ',';
                }
            }

            movie_name_list += "]";

            if(obj_keys.length > 0){
                // 파이썬 프로세스에 데이터 전송
                this.python_process.stdin.write(`${movie_name_list}\n`);

                // 파이썬 프로세스의 출력값 수신
                this.python_process.stdout.on('data', (data)=>{
                    resolve({"regMsg": `${data.toString()}`});
                });

                //console.log(python_exec + " : " + pcs_path + " : " + movie_name_list);

                // python_process.stdout.on('data', (data)=>{
                //     try{
                //         const parse_data:JSONObject = JSON.parse(data.toString());

                //         resolve(parse_data);
                //     }catch(error){
                //         reject({"reqMsg":`EM : ${error.message}`});
                //     }
                // });

                // python_process.stderr.on('data', (data)=>{
                //     reject({"reqMsg":`${data}`});
                // })

                // python_process.on('close',(data)=>{
                //     resolve({"reqMsg":data});
                // });
                //resolve({"reqMsg":"hello world!"});

            }else{
                reject({"reqMsg":"parameter does not exist"});
            }
        });
    }

}

export default AnalyzeMovieData;