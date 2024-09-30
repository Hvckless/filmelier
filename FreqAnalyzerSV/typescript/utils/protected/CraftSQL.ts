import MySQLayer from "../sql/MySQLayer";
import Protect from "./Protect";

import { Parameter } from "../type/Parameter";

class CraftSQL implements Protect, MySQLayer{
    initial(param: Parameter):JSON {
        throw new Error("Method not implemented.");
    }


    searchMovies(context: string): Array<string> {
        throw new Error("Method not implemented.");
    }
    getMoviePoster(moviename: string): Buffer {
        throw new Error("Method not implemented.");
    }

}

export default CraftSQL;