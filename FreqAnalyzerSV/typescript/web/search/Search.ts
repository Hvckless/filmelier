import FilmAnimation from "../style/FilmAnimation.js";

class Search{
    private searchContext:string;


    public submit(element:HTMLInputElement){
        element.blur(); //포커스 상태 취소

        this.searchContext = element.value; //searchContext에 검색 내용 저장
        element.value = ""; //원본 input 내용 삭제

        let timer:NodeJS.Timeout = new FilmAnimation().startSearhFieldLoading(element);

        setTimeout(()=>{
            clearInterval(timer);
        }, 5000);


    }
}

export default Search;