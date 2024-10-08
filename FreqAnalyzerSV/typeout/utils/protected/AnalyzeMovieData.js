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
import { spawn } from "child_process";
class AnalyzeMovieData {
    initial(param) {
        return __awaiter(this, void 0, void 0, function* () {
            return new Promise((resolve, reject) => __awaiter(this, void 0, void 0, function* () {
                let obj_keys = Object.keys(param);
                let movie_name_list = "[";
                for (let i = 0; i < obj_keys.length; i++) {
                    movie_name_list += `'${obj_keys[i]}'`;
                    if (i != (obj_keys.length - 1)) {
                        movie_name_list += ',';
                    }
                }
                movie_name_list += "]";
                if (obj_keys.length > 0) {
                    const python_exec = path.resolve(process.cwd(), "../NLPyCodes/OOP/venv/bin/python");
                    const pcs_path = path.resolve(process.cwd(), '../NLPyCodes/OOP/similarity.py');
                    const python_process = spawn(python_exec, [pcs_path, movie_name_list], {
                        cwd: path.resolve(process.cwd(), '../NLPyCodes/OOP'),
                        stdio: 'pipe'
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
                    python_process.stdout.on('data', (data) => {
                        //console.log(`Output: ${data.toString()}`);
                        resolve({ "reqMsg": `${data.toString()}` });
                    });
                    //resolve({"reqMsg":"hello world!"});
                }
                else {
                    reject({ "reqMsg": "parameter does not exist" });
                }
            }));
        });
    }
}
export default AnalyzeMovieData;
