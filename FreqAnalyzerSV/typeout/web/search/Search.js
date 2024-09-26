import FilmAnimation from "../style/FilmAnimation.js";
class Search {
    submit(element) {
        element.blur(); //포커스 상태 취소
        this.searchContext = element.value; //searchContext에 검색 내용 저장
        element.value = ""; //원본 input 내용 삭제
        let timer = new FilmAnimation().startSearhFieldLoading(element);
        setTimeout(() => {
            clearInterval(timer);
        }, 5000);
    }
}
export default Search;
