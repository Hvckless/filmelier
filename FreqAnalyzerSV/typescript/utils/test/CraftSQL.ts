import * as fs from "fs";

import MySQLayer from "../sql/MySQLayer";

/**
 * MySQLayer 동작 테스트용 가짜 데이터 핸들러입니다
 * 프로덕션에서 사용하지 마세요
 */
class CraftSQL implements MySQLayer{
    searchMovies(context: string): Array<string> {
        fs.readdir("../../../src/image/ignore/" ,(err: NodeJS.ErrnoException | null, files: string[]):void=>{

            files.forEach((file)=>{

                console.log(file);

            });

        });

        return ["ab","cd"];
    }
    getMoviePoster(moviename: string): Buffer {
        throw new Error("Method not implemented.");


    }
}