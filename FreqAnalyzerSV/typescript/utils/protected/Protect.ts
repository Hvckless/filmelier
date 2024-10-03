import JSONObject from "../type/JSONObject";
import { Parameter } from "../type/Parameter";

interface Protect{
    initial(param?:Parameter):JSONObject;
}

export default Protect;