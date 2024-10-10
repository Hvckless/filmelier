var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
import MovieContentHandler from "../movie/MovieContentHandler.js";
import FetchAPI from "../network/FetchAPI.js";
import FilmAnimation from "../style/FilmAnimation.js";
class Search {
    submit(element) {
        return __awaiter(this, void 0, void 0, function* () {
            document.querySelector("#movieContents").innerHTML = ""; //이전 검색 삭제
            element.blur(); //포커스 상태 취소
            this.searchContext = element.value; //searchContext에 검색 내용 저장
            console.log(this.searchContext);
            element.value = ""; //원본 input 내용 삭제
            //로딩 애니메이션용 JavaScript
            let timer = new FilmAnimation().startSearhFieldLoading(element);
            yield FetchAPI.getJSON("/protected/FakeSQL.do?moviename=" + this.searchContext)
                .then((data) => {
                clearInterval(timer);
                element.placeholder = "Done! now you can search another one!";
                MovieContentHandler.getInstance.createMoviePanel(data, document.querySelector("#movieContents"));
                document.querySelector("#sendAnalysticsButton").classList.remove("invisible");
                document.querySelector("#sendAnalysticsButton").classList.add("showflex");
            })
                .catch((err) => {
                console.error(err);
            });
        });
    }
}
export default Search;
