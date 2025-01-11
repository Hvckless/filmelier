import { SV_STAT } from "./variable/SV_STAT.js";
class server_settings {
    constructor() {
        //옵션 세팅 START
        /**
         * 서버 배포 상태를 나타내는 필드.
         * @see SV_STAT
         */
        this.server_stat_type = SV_STAT.DEV;
        switch (this.server_stat_type) {
            case SV_STAT.DEV: {
                this.mysql_ip = "192.168.0.61";
                this.sql_search_movie_type = "FakeSQL.do";
                this.sql_search_rank_type = "FakeMovieData.do";
            }
            case SV_STAT.DEV_NOPYTHON: {
                this.mysql_ip = "192.168.0.61";
                this.sql_search_movie_type = "CraftSQL.do";
                this.sql_search_rank_type = "FakeMovieData.do";
            }
            case SV_STAT.RELEASE: {
                this.mysql_ip = "external-ip";
                this.sql_search_movie_type = "CraftSQL.do";
                this.sql_search_rank_type = "AnalyzeMovieData.do";
            }
        }
    }
    static getInstance() {
        return this.instance;
    }
}
//옵션 세팅 END
//인스턴트 관리 코드 START
server_settings.instance = new server_settings();
export default server_settings;
