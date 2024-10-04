var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
import MySQL from "../sql/MySQL";
class CraftSQL {
    searchDataList(context) {
        throw new Error("Method not implemented.");
    }
    initial(param) {
        return __awaiter(this, void 0, void 0, function* () {
            return new Promise((resolve, reject) => {
                const sql = 'select movie_name, movie_image from movie_info where movie_name like ?';
                const moviename = decodeURI(param["moviename"]);
                const queryParam = `%${moviename}%`; // 부분 일치 검색
                MySQL.instance.getConnection().query(sql, queryParam, (err, results) => {
                    if (err) {
                        reject(err);
                    }
                    if (results.length > 0) {
                        const movieInfo = results.map((row) => ({
                            name: row.movie_name,
                            image: Buffer.from(row.movie_image).toString("base64"),
                        }));
                        resolve(movieInfo);
                    }
                    else {
                        reject(new Error("해당하는 영화를 찾을 수 없습니다"));
                    }
                });
            });
        });
    }
}
export default CraftSQL;
