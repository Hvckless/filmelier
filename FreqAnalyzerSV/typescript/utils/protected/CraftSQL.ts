import MySQLayer from "../sql/MySQLayer";
import Protect from "./Protect";
import JSONObject from "../type/JSONObject";

import MySQL from "../sql/MySQL";

import { Parameter } from "../type/Parameter";
import MovieJSON from "../type/MovieJSON";

class CraftSQL implements Protect, MySQLayer{
    searchDataList(context: string): MovieJSON {
        throw new Error("Method not implemented.");
    }


    async initial(param: Parameter):Promise<JSONObject> {
        return new Promise((resolve, reject)=>{
            const sql = 'select movie_name, movie_image from movie_info where movie_name like ?';
            const moviename = decodeURI(param["moviename"]);
            const queryParam = `%${moviename}%`; // 부분 일치 검색
            MySQL.instance.getConnection().query(sql, queryParam, (err:Error, results:any)=>{
                if(err){
                    reject(err);
                }

                if(results.length > 0){
                    const movieInfo = results.map((row:any)=>({
                        name: row.movie_name,
                        image: Buffer.from(row.movie_image).toString("base64"),
                    }));

                    resolve(movieInfo);
                }else{
                    reject(new Error("해당하는 영화를 찾을 수 없습니다"));
                }
            });
        });
    }



}

export default CraftSQL;