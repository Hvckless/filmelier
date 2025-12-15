import * as path from "path";
import * as os from "os";
import { ChildProcess, spawn } from "child_process";
import JSONObject from "../type/JSONObject";
import { rejects } from "assert";

interface PendingRequest{
    resolve: (value: any)=>void;
    reject: (reason?: any)=>void;
}

class PythonProcess{
    public python_process:ChildProcess | null = null;

    private platform:NodeJS.Platform = os.platform();
    private pathchar:string;
    private isReady: boolean = false;

    private request_queue: Array<PendingRequest> = [];

    public static instance:PythonProcess = new PythonProcess();

    private constructor(){
        this.startProcess();
    }

    private startProcess(){

        const isWin = this.platform === "win32";
        const pythonBin = isWin ? "Scripts/python.exe" : "bin/python";

        const python_exec:string = path.resolve(process.cwd(), "../NLPyCodes/OOPNp/venv", pythonBin);
        const pcs_path:string = path.resolve(process.cwd(), "../NLPyCodes/OOPNp/similarity.py");
        const cwd_path:string = path.resolve(process.cwd(), "../NLPyCodes/OOPNp")

        console.log(`파이썬 경로 : ${python_exec}`);

        this.python_process = spawn(python_exec, [pcs_path], {
            cwd: cwd_path,
            stdio: ['pipe','pipe','pipe']
        });

        console.log("python 추론 프로세스 로드 완료");

        this.python_process.stdout?.on('data', (data:Buffer)=>{
            console.log(`Python 프로세스 실행 완료: ${data.toString()}`);
            this.handle(data);
        })

        // 에러 발생 시 처리
        this.python_process.stderr?.on('data', (data) => {
            console.error(`파이썬 에러: ${data.toString()}`);
        });
        this.python_process.on('error', (err)=>{
            console.error(`파이썬 실행 실패 : `, err);
        });

        // 종료시 처리
        this.python_process.on('close', (code) => {
            console.warn(`파이썬 프로세스 종료 ${code}`);

            this.cleanQueue("프로세스 종료됨");
            this.python_process = null;

            console.log("python 추론 프로세스 리로드 3초전...")
            setTimeout(()=>{
                this.startProcess();
            }, 3000);
        });
    }

    public async execute(data:string): Promise<string>{

        return new Promise((resolve, reject)=>{
            if((this.python_process == null) || (this.python_process.stdin == null)){

                reject("python process is not running");

                return
            }

            this.request_queue.push({resolve, reject});
            this.python_process.stdin.write(`${data}\n`, 'utf-8');
        });

    }

    /**
     * 파이썬 프로세스가 데이터를 처리 완료했을 때 실행되는 메서드
     * 
     * @param data 파이썬 프로세스가 반환한 결과값
     * @returns handle은 처리한 Promise의 내부 resolve 메서드만을 실행하기 때문에 return하지 않음
     */
    private handle(data:Buffer):void{
        const data_string = data.toString('utf-8').trim();

        if(!data_string){
            return;
        }
        
        try{
            const result:JSONObject = JSON.parse(data_string);

            const cur_req:PendingRequest = this.request_queue.shift();

            if(cur_req){
                cur_req.resolve(result);
            }else{
                console.warn("데이터 매칭 불가 : ", result);
            }
        }catch(err){
            console.error("JSON 파싱 중 에러 : ", err);

            rejects(err);
        }

    }

    /**
     * 등록된 모든 큐를 취소하는 메서드
     * 
     * @param reason 취소 사유
     */
    private cleanQueue(reason: string):void{
        while(this.request_queue.length > 0){
            const req = this.request_queue.shift();
            req?.reject(reason);
        }
    }
}

export default PythonProcess;