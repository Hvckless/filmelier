import PythonRunner from "../process/PythonRunner";
import JSONObject from "../type/JSONObject";
import { Parameter } from "../type/Parameter";
import Protect from "./Protect";

class FakeMovieData implements Protect, PythonRunner{
    async initial(param?: Parameter): Promise<JSONObject> {
        return new Promise(async (resolve, reject)=>{
            resolve({"reqMsg":await this.execute(param)});
        });
    }
    async execute(param: Parameter): Promise<string> {
        return new Promise((resolve, reject)=>{
            setTimeout(()=>{
                resolve(`{'87.111':'마션','67.235':'인터스텔라','66.123':'주토피아','63.557':'어벤저스','57.531':'트랜스포머','53.235':'울프 콜','27.125':'범죄도시','22.222':'겨울왕국','18.324':'컨택트','11.253':'그래비티'}`);
            }, 3000);
        });
    }

}

export default FakeMovieData;