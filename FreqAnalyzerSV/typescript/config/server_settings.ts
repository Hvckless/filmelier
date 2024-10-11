import { SV_STAT } from "./variable/SV_STAT";

class server_settings{

    //옵션 세팅 START


    /**
     * 서버 배포 상태를 나타내는 필드.
     * @see SV_STAT
     */
    public server_stat_type = SV_STAT.DEV;

    public mysql_ip = "192.168.0.61";
    public sql_search_movie_type = "CraftSQL.do";
    public sql_search_rank_type = "AnalyzeMovieSend.do";
    


    //옵션 세팅 END





























    //인스턴트 관리 코드 START

    private static instance:server_settings = new server_settings();

    private constructor(){}

    public static getInstance():server_settings{
        return this.instance;
    }

    //인스턴트 관리 코드 END

}

export default server_settings;