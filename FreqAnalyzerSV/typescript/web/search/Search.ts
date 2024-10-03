import JSONObject from "../../utils/type/JSONObject.js";
import MovieContentHandler from "../movie/MovieContentHandler.js";
import FetchAPI from "../network/FetchAPI.js";
import FilmAnimation from "../style/FilmAnimation.js";

class Search{
    private searchContext:string;


    public async submit(element:HTMLInputElement){
        element.blur(); //포커스 상태 취소

        this.searchContext = element.value; //searchContext에 검색 내용 저장
        console.log(this.searchContext);
        element.value = ""; //원본 input 내용 삭제

        //로딩 애니메이션용 JavaScript
        let timer:NodeJS.Timeout = new FilmAnimation().startSearhFieldLoading(element); 


        await FetchAPI.getJSON("/protected/FakeSQL.do?hello=world")
            .then((data:JSONObject)=>{
                clearInterval(timer);
                element.placeholder = "Done! now you can search another one!";

                new MovieContentHandler().createMoviePanel(data);
            })
            .catch((err)=>{
                console.error(err);
            });

        


    }
}

export default Search;