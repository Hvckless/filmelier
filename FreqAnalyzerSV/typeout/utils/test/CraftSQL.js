import * as fs from "fs";
/**
 * MySQLayer 동작 테스트용 가짜 데이터 핸들러입니다
 * 프로덕션에서 사용하지 마세요
 */
class CraftSQL {
    searchMovies(context) {
        fs.readdir("../../../src/image/ignore/", (err, files) => {
            files.forEach((file) => {
                console.log(file);
            });
        });
        return ["ab", "cd"];
    }
    getMoviePoster(moviename) {
        throw new Error("Method not implemented.");
    }
}
