var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
/**
 *
 * 사용자의 특수 URL 입력을 처리하는 라우터입니다
 *
 * @author Hvckless
 */
class URLResolver {
    constructor() {
        this.protectedDOC = "protected";
    }
    /**
     * 특수한 요청 (API요청)인지 확인하는 메서드
     * API요청이 맞다면 true를 반환한다
     * @param url 클라이언트가 요청한 URL
     * @returns API 요청 여부
     */
    isRequest(url) {
        if (url.split("/")[1] == this.protectedDOC) {
            return true;
        }
        return false;
    }
    /**
     * URL이 protected된 영역에 접근하는지 체크하는 메서드
     * protected가 중간에 포함되어있으면 true를 반환하며, 그런 경우 접근 제한 안내 메세지를 반환한다
     * @param url 클라이언트가 요청한 URL
     * @returns protected 여부
     */
    isProtected(url) {
        if (url.split("/").includes(this.protectedDOC)) {
            return true;
        }
        return false;
    }
    /**
     * /protected/somemethod.do?hello=world
     *
     *  -> somemethod.ts의 initial이 실행됨
     *
     * 요청을 실행하여 Promise로 반환하는 함수
     *
     *
     * @param res 응답받을 response client 데이터. 사용되지 않음
     * @param url 요청 URL
     * @param param 요청 parameter
     * @returns JSON 객체
     */
    resolveData(res, url, param) {
        return __awaiter(this, void 0, void 0, function* () {
            return new Promise((resolve, reject) => __awaiter(this, void 0, void 0, function* () {
                const queryString = url.split("/")[2];
                if (queryString.split(".").length != 2) {
                    reject(new Error("request method is incorrect" + ` url : ${url}`));
                }
                const modulename = queryString.split(".")[0];
                const extension = queryString.split(".")[1];
                if (extension == "do") {
                    try {
                        const module = yield import(`../protected/${modulename}.js`);
                        const moduleinstance = new module.default();
                        if (typeof moduleinstance.initial === 'function') {
                            resolve(yield moduleinstance.initial(param));
                        }
                        else {
                            resolve({ "resMsg": "The request does not exist" });
                        }
                    }
                    catch (e) {
                        resolve({ "resMsg": e });
                    }
                }
            }));
        });
    }
}
export default URLResolver;
