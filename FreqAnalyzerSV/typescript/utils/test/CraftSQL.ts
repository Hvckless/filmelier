import MySQLayer from "../sql/MySQLayer";

/**
 * MySQLayer 동작 테스트용 가짜 데이터 핸들러입니다
 * 프로덕션에서 사용하지 마세요
 */
class CraftSQL implements MySQLayer{
    public queryMovie(searchContext: string): Buffer {
        throw new Error("Method not implemented.");
    }
}