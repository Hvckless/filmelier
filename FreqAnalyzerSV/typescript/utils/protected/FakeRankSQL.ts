import MySQLayer from "../sql/MySQLayer";
import JSONObject from "../type/JSONObject";
import MovieJSON from "../type/MovieJSON";
import { Parameter } from "../type/Parameter";
import Protect from "./Protect";

class FakeRankSQL implements Protect, MySQLayer{
    searchDataList(context: string): MovieJSON {
        throw new Error("Method not implemented.");
    }
    initial(param?: Parameter): Promise<JSONObject> {
        throw new Error("Method not implemented.");
    }

}

export default FakeRankSQL;