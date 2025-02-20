var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
import PythonProcess from "../process/PythonProcess.js";
class AnalyzeMovieData {
    constructor() {
        this.python_process = PythonProcess.instance.python_process;
    }
    execute(param) {
        return __awaiter(this, void 0, void 0, function* () {
            return new Promise((resolve, reject) => {
                let newdata = "HELLo";
                resolve(newdata);
            });
        });
    }
    initial(param) {
        return __awaiter(this, void 0, void 0, function* () {
            return new Promise((resolve, reject) => __awaiter(this, void 0, void 0, function* () {
                let obj_keys = Object.keys(param);
                let movie_name_list = "[";
                for (let i = 0; i < obj_keys.length; i++) {
                    movie_name_list += `'${decodeURIComponent(obj_keys[i])}'`;
                    if (i != (obj_keys.length - 1)) {
                        movie_name_list += ',';
                    }
                }
                movie_name_list += "]";
                if (obj_keys.length > 0) {
                    console.log(`Python으로 전송: ${movie_name_list}`);
                    this.python_process.stdin.write(`${movie_name_list}\n`, 'utf-8', (err) => {
                        if (err) {
                            console.error("데이터 전송 에러:", err);
                        }
                        else {
                            console.log("데이터 전송 완료:", movie_name_list);
                        }
                    });
                    this.python_process.stdout.on('data', (data) => {
                        try {
                            const result = JSON.parse(data.toString('utf-8').trim());
                            resolve({ "reqMsg": result });
                        }
                        catch (err) {
                            console.error(`결과 파싱 에러: ${err}`);
                            reject({ "reqMsg": `파싱 에러: ${err}` });
                        }
                    });
                }
                else {
                    reject({ "reqMsg": "parameter does not exist" });
                }
            }));
        });
    }
}
export default AnalyzeMovieData;
