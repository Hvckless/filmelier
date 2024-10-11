export enum SV_STAT{

    /**
     * 개발중인 서버. 모든 요청사항이 가짜 데이터 생성 모듈로 리다이렉션됨
     */
    DEV,
    /**
     * MySQL으로 영화 데이터 요청 허용 / PythonRunner를 실행하지 않고 가짜 데이터 생성 모듈로 리다이렉션됨
     */
    DEV_NOPYTHON,
    /**
     * 릴리즈 서버. 모든 요청사항이 실제 서버로 리다이렉션됨
     */
    RELEASE,
    /**
     * 바이너리 서버. 테스트 전용
     */
    BINARY

}