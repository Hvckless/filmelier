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
    isRequest(url) {
        if (url.split("/")[1] == this.protectedDOC) {
            return true;
        }
        return false;
    }
    isProtected(url) {
        if (url.split("/").includes(this.protectedDOC)) {
            return true;
        }
        return false;
    }
    resolveData(res, url, param) {
        let queryString = url.split("/")[2];
        console.log("쿼리 스트링 출력");
        console.log(queryString);
        console.log(param);
        return null;
    }
}
export default URLResolver;
