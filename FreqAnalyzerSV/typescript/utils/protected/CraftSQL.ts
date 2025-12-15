import MySQLayer from "../sql/MySQLayer";
import Protect from "./Protect";
import JSONObject from "../type/JSONObject";

import MySQL from "../sql/MySQL.js";

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

            if(moviename.length < 1){
                return reject(new Error("영화 이름 길이는 1 이상이어야 합니다"));
            }

            const queryParam = `%${moviename}%`; // 부분 일치 검색
            MySQL.instance.getConnection().query(sql, queryParam, (err:Error, results:any)=>{
                if(err){
                    return reject(err);
                }
                if((results === null) || (results === undefined)){
                    return reject(new Error("해당하는 영화를 찾을 수 없습니다."));
                }

                if(results.length > 0){
                    const movieInfo = results.map((row:any)=>({
                        name: row.movie_name,
                        image: Buffer.from(row.movie_image).toString("base64"),
                        //image: row.movie_image,
                    }));

                    return resolve(movieInfo);
                }else{
                    return reject(new Error("해당하는 영화를 찾을 수 없습니다"));
                }
            });
        });
    }



}

export default CraftSQL;