import JSONObject from "../type/JSONObject";
import { Parameter } from "../type/Parameter";

interface Protect{
    initial(param?:Parameter):Promise<JSONObject>;
}

export default Protect;