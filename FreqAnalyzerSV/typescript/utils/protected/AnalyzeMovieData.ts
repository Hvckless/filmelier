import JSONObject from "../type/JSONObject";
import { Parameter } from "../type/Parameter";
import Protect from "./Protect";

class AnalyzeMovieData implements Protect{
    initial(param: Parameter): JSONObject {
        throw new Error("Method not implemented.");
    }
    
}

export default AnalyzeMovieData;