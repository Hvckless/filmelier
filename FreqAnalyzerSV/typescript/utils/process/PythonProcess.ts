import * as path from "path";
import { spawn } from "child_process";

class PythonProcess{
    public python_process: any;
    private isReady: boolean = false;

    public static instance:any = new PythonProcess();

    private constructor(){
        //const python_exec:string = path.resolve(process.cwd(), "../NLPyCodes/OOP/venv/bin/python");
        //const pcs_path:string = path.resolve(process.cwd(), '../NLPyCodes/OOP/similarity.py');
        const python_exec:string = path.resolve(process.cwd(), "..\\NLPyCodes\\OOP\\venv\\Scripts\\python.exe");
        const pcs_path:string = path.resolve(process.cwd(), '..\\NLPyCodes\\OOP\\similarity.py');

        this.python_process = spawn(python_exec, [pcs_path], {
            cwd: path.resolve(process.cwd(), '../NLPyCodes/OOP'),
            stdio: ['pipe','pipe','pipe']
        });

        // 에러 발생 시 처리
        this.python_process.stderr.on('data', (data) => {
            console.error(`파이썬 에러: ${data.toString()}`);
        });

        this.python_process.stdout.once('data', (data) => {
            console.log(`Python 프로세스 실행 완료: ${data.toString()}`);
            this.isReady = true;  // Python이 준비됨
        });

        // 종료시 처리
        this.python_process.on('close', (code) => {
            console.log(`파이썬 프로세스 종료 ${code}`);

            this.python_process = spawn(python_exec, [pcs_path], {
                cwd: path.resolve(process.cwd(), '../NLPyCodes/OOP'),
                stdio: ['pipe','pipe','pipe']
            });
        });
    }
}

export default PythonProcess;