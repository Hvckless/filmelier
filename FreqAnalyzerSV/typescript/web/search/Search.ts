import JSONObject from "../../utils/type/JSONObject.js";
import Vars from "../global/Vars.js";
import MovieContentHandler from "../movie/MovieContentHandler.js";
import FetchAPI from "../network/FetchAPI.js";
import FilmAnimation from "../style/FilmAnimation.js";

class Search{
    private searchContext:string;


    public async submit(element:HTMLInputElement){
        document.querySelector("#movieContents").innerHTML = ""; //이전 검색 삭제

        this.searchContext = element.value; //searchContext에 검색 내용 저장
        console.log(this.searchContext);
        element.value = ""; //원본 input 내용 삭제

        //로딩 애니메이션용 JavaScript
        let timer:NodeJS.Timeout = new FilmAnimation().startSearhFieldLoading(element); 

        document.querySelector("#ranking_toprank").innerHTML = "";
        document.querySelector("#ranking_underrank").innerHTML = "";

        let ranking_panel = document.querySelector("#ranking")

        if(ranking_panel.classList.contains("showflex")){
            ranking_panel.classList.remove("showflex");
            ranking_panel.classList.add("invisible");
        }
        

        await FetchAPI.getJSON("/protected/CraftSQL.do?moviename="+this.searchContext)
            .then((data:Array<JSONObject>)=>{
                clearInterval(timer);
                element.placeholder = "검색 완료!";

                if(Object.keys(Vars.SelectedMovies).length > 0){
                    document.querySelector("#sendAnalysticsButton").setAttribute("isBlocked", "false");
                }

                MovieContentHandler.getInstance.createMoviePanel(data, document.querySelector("#movieContents"));

                document.querySelector("#sendAnalysticsButton").classList.remove("invisible");
                document.querySelector("#sendAnalysticsButton").classList.add("showflex");
            })
            .catch((err)=>{
                console.error(err);
            });

        


    }
}

export default Search;