var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
import * as path from "path";
import * as os from "os";
import { spawn } from "child_process";
import { rejects } from "assert";
class PythonProcess {
    constructor() {
        this.python_process = null;
        this.platform = os.platform();
        this.isReady = false;
        this.request_queue = [];
        this.startProcess();
    }
    startProcess() {
        var _a, _b;
        const isWin = this.platform === "win32";
        const pythonBin = isWin ? "Scripts/python.exe" : "bin/python";
        const python_exec = path.resolve(process.cwd(), "../NLPyCodes/OOPNp/venv", pythonBin);
        const pcs_path = path.resolve(process.cwd(), "../NLPyCodes/OOPNp/similarity.py");
        const cwd_path = path.resolve(process.cwd(), "../NLPyCodes/OOPNp");
        console.log(`파이썬 경로 : ${python_exec}`);
        this.python_process = spawn(python_exec, [pcs_path], {
            cwd: cwd_path,
            stdio: ['pipe', 'pipe', 'pipe']
        });
        console.log("python 추론 프로세스 로드 완료");
        (_a = this.python_process.stdout) === null || _a === void 0 ? void 0 : _a.on('data', (data) => {
            console.log(`Python 프로세스 실행 완료: ${data.toString()}`);
            this.handle(data);
        });
        // 에러 발생 시 처리
        (_b = this.python_process.stderr) === null || _b === void 0 ? void 0 : _b.on('data', (data) => {
            console.error(`파이썬 에러: ${data.toString()}`);
        });
        this.python_process.on('error', (err) => {
            console.error(`파이썬 실행 실패 : `, err);
        });
        // 종료시 처리
        this.python_process.on('close', (code) => {
            console.warn(`파이썬 프로세스 종료 ${code}`);
            this.cleanQueue("프로세스 종료됨");
            this.python_process = null;
            console.log("python 추론 프로세스 리로드 3초전...");
            setTimeout(() => {
                this.startProcess();
            }, 3000);
        });
    }
    execute(data) {
        return __awaiter(this, void 0, void 0, function* () {
            return new Promise((resolve, reject) => {
                if ((this.python_process == null) || (this.python_process.stdin == null)) {
                    reject("python process is not running");
                    return;
                }
                this.request_queue.push({ resolve, reject });
                this.python_process.stdin.write(`${data}\n`, 'utf-8');
            });
        });
    }
    /**
     * 파이썬 프로세스가 데이터를 처리 완료했을 때 실행되는 메서드
     *
     * @param data 파이썬 프로세스가 반환한 결과값
     * @returns handle은 처리한 Promise의 내부 resolve 메서드만을 실행하기 때문에 return하지 않음
     */
    handle(data) {
        const data_string = data.toString('utf-8').trim();
        if (!data_string) {
            return;
        }
        try {
            const result = JSON.parse(data_string);
            const cur_req = this.request_queue.shift();
            if (cur_req) {
                cur_req.resolve(result);
            }
            else {
                console.warn("데이터 매칭 불가 : ", result);
            }
        }
        catch (err) {
            console.error("JSON 파싱 중 에러 : ", err);
            rejects(err);
        }
    }
    /**
     * 등록된 모든 큐를 취소하는 메서드
     *
     * @param reason 취소 사유
     */
    cleanQueue(reason) {
        while (this.request_queue.length > 0) {
            const req = this.request_queue.shift();
            req === null || req === void 0 ? void 0 : req.reject(reason);
        }
    }
}
PythonProcess.instance = new PythonProcess();
export default PythonProcess;
