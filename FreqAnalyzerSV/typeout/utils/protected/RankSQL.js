import MySQL from "../sql/MySQL.js";
class RankSQL {
    searchDataList(context) {
        throw new Error("Method not implemented.");
    }
    initial(param) {
        console.log("파라메터 출력");
        console.log(param);
        return new Promise((resolve, reject) => {
            const sql = 'select movie_name, movie_image from movie_info where movie_name in (?)';
            let key_array = [];
            Object.keys(param).forEach((key) => {
                key_array.push(param[key]);
            });
            if (key_array.length < 1) {
                reject(new Error("요청이 존재하지 않습니다."));
            }
            MySQL.instance.getConnection().query(sql, [param], (err, results) => {
                if (err) {
                    reject(err);
                    return;
                }
                if (results.length < 1) {
                    reject(new Error("영화가 존재하지 않습니다."));
                    return;
                }
                const movie_info = results.map((row) => ({
                    name: row.movie_name,
                    image: Buffer.from(row.movie_image).toString("base64"),
                }));
                resolve(movie_info);
            });
        });
    }
}
export default RankSQL;
