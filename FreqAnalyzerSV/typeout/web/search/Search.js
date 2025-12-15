var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
import server_settings from "../../config/server_settings.js";
import { SV_STAT } from "../../config/variable/SV_STAT.js";
import Vars from "../global/Vars.js";
import MovieContentHandler from "../movie/MovieContentHandler.js";
import FetchAPI from "../network/FetchAPI.js";
import FilmAnimation from "../style/FilmAnimation.js";
class Search {
    submit(element) {
        return __awaiter(this, void 0, void 0, function* () {
            document.querySelector("#movieContents").innerHTML = ""; //이전 검색 삭제
            this.searchContext = element.value; //searchContext에 검색 내용 저장
            if (this.searchContext.length < 1) {
                alert("검색어 길이는 1 이상어야 합니다");
                return;
            }
            else {
                console.log(this.searchContext);
                element.value = ""; //원본 input 내용 삭제
                //로딩 애니메이션용 JavaScript
                let timer = new FilmAnimation().startSearhFieldLoading(element);
                document.querySelector("#ranking_toprank").innerHTML = "";
                document.querySelector("#ranking_underrank").innerHTML = "";
                let ranking_panel = document.querySelector("#ranking");
                if (ranking_panel.classList.contains("showflex")) {
                    ranking_panel.classList.remove("showflex");
                    ranking_panel.classList.add("invisible");
                }
                let requestURL;
                switch (server_settings.getInstance().server_stat_type) {
                    case SV_STAT.DEV: {
                    }
                    case SV_STAT.DEV_NOPYTHON: {
                    }
                    case SV_STAT.BINARY: {
                    }
                }
                yield FetchAPI.getJSON("/protected/CraftSQL.do?moviename=" + this.searchContext)
                    .then((data) => {
                    clearInterval(timer);
                    element.placeholder = "검색 완료!";
                    if (Object.keys(Vars.SelectedMovies).length > 0) {
                        document.querySelector("#sendAnalysticsButton").setAttribute("isBlocked", "false");
                    }
                    MovieContentHandler.getInstance.createMoviePanel(data, document.querySelector("#movieContents"));
                    document.querySelector("#sendAnalysticsButton").classList.remove("invisible");
                    document.querySelector("#sendAnalysticsButton").classList.add("showflex");
                })
                    .catch((err) => {
                    console.error(err);
                });
            }
        });
    }
}
export default Search;
