var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
class FakeMovieData {
    initial(param) {
        return __awaiter(this, void 0, void 0, function* () {
            return new Promise((resolve, reject) => __awaiter(this, void 0, void 0, function* () {
                resolve({ "reqMsg": yield this.execute(param) });
            }));
        });
    }
    execute(param) {
        return __awaiter(this, void 0, void 0, function* () {
            return new Promise((resolve, reject) => {
                setTimeout(() => {
                    resolve(`{'87.111':'마션','67.235':'인투 더 월드','66.123':'주토피아','63.557':'어벤져스','57.531':'트랜스퍼런스','53.235':'울프 콜','27.125':'범죄도시','22.222':'겨울왕국','18.324':'스코어','11.253':'그래비티'}`);
                }, 500);
            });
        });
    }
}
export default FakeMovieData;
