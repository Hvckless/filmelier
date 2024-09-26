/**
 *
 * 사용자의 특수 URL 입력을 처리하는 라우터입니다
 *
 * @author Hvckless
 */
class URLResolver {
    isValid(url) {
        if (url.split("/")[1] == "protected") {
            return true;
        }
        return false;
    }
    resolveData(res, url, param) {
        let queryString = url.split("/")[2];
        console.log("쿼리 스트링 출력");
        console.log(queryString);
        return null;
    }
}
export default URLResolver;
