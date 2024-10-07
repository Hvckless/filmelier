var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
import Vars from "../global/Vars.js";
import FetchAPI from "../network/FetchAPI.js";
import Search from "../search/Search.js";
/**
 * Singleton 패턴으로 생성된 핸들러
 * getInstance를 통해 접근
 */
class MovieContentHandler {
    constructor() { }
    /**
     * 영화 JSONObject를 기반으로 영화 목록 UI 생성 함수
     * @param movie_json 영화 데이터가 들어있는 JSONObject
     */
    createMoviePanel(movie_json) {
        let movie_panel = document.querySelector("#movieContents");
        for (let movie of movie_json) {
            let movie_name = movie["name"];
            let movie_image = movie["image"];
            let mv_content = document.createElement('div');
            mv_content.classList.add('movie_content');
            let mv_content_image_div = document.createElement('div');
            mv_content_image_div.classList.add('movie_content_img_panel');
            mv_content_image_div.classList.add('relative');
            let mv_content_image_star = document.createElement('div');
            mv_content_image_star.classList.add('movie_content_img_star');
            mv_content_image_star.classList.add('absolute');
            mv_content_image_star.setAttribute("mvname", `${movie_name}`);
            mv_content_image_star.onmouseleave = (ev) => {
                if (ev.target instanceof HTMLDivElement) {
                    ev.target.removeAttribute("starnum");
                }
            };
            let starcounter = Vars.SelectedMovies[`${movie_name}`];
            if (starcounter != undefined) {
                mv_content_image_star.setAttribute("starsel", starcounter);
            }
            for (let i = 0; i < 5; i++) {
                let mv_content_image_realstar = document.createElement('div');
                mv_content_image_realstar.classList.add('emptystar');
                mv_content_image_realstar.classList.add('starlight');
                mv_content_image_realstar.setAttribute("starnum", i + "");
                mv_content_image_realstar.onmouseenter = (ev) => {
                    if (ev.target instanceof HTMLDivElement) {
                        ev.target.parentElement.setAttribute("starnum", ev.target.getAttribute("starnum"));
                    }
                };
                mv_content_image_realstar.onmousedown = (ev) => {
                    if (ev.target instanceof HTMLDivElement) {
                        ev.target.parentElement.setAttribute("starsel", ev.target.getAttribute("starnum"));
                        MovieContentHandler.getInstance.insertContent(`${movie_name}`, ev.target.getAttribute("starnum"));
                    }
                };
                mv_content_image_star.append(mv_content_image_realstar);
            }
            let mv_content_image = document.createElement('img');
            mv_content_image.setAttribute('src', `data:image/jpeg;base64,${movie_image}`);
            mv_content_image.classList.add('absolute');
            let mv_content_button_div = document.createElement('div');
            //하단 코드는 릴리즈시 삭제
            mv_content_button_div.onclick = (ev) => {
                MovieContentHandler.getInstance.showList();
            };
            let mv_content_button_text = document.createElement('span');
            mv_content_button_text.textContent = `${movie_name}`;
            mv_content_button_div.append(mv_content_button_text);
            mv_content_image_div.append(mv_content_image);
            mv_content_image_div.append(mv_content_image_star);
            mv_content.append(mv_content_image_div);
            mv_content.append(mv_content_button_div);
            movie_panel.append(mv_content);
        }
        // movie_json.forEach((movie)=>{
        //     Object.keys(movie).forEach((movie_name)=>{
        //     });
        // });
    }
    /**
     * 영화에 별점을 줄 경우 작동하는 함수
     * 사용자가 좋아하는 영화 목록 로그를 생성한다
     * @param movie_name 영화 이름
     */
    createLogSpan(movie_name) {
        let searbox_logger = document.querySelector("#searchLog");
        let search_log_div = document.createElement('div');
        let search_log_text = document.createElement('span');
        search_log_text.classList.add('searchlog');
        search_log_text.textContent = movie_name;
        search_log_text.onmousedown = (ev) => {
            let input_area = document.querySelector("#searchInput");
            if (input_area instanceof HTMLInputElement) {
                input_area.value = `${movie_name}`;
                new Search().submit(input_area);
            }
        };
        let search_log_button = document.createElement('div');
        search_log_button.classList.add('ssearchLogRemover');
        search_log_button.textContent = "X";
        search_log_button.onmousedown = (ev) => {
            if (ev.target instanceof HTMLDivElement) {
                MovieContentHandler.getInstance.removeContent(ev.target.parentElement.querySelector(".searchlog").textContent);
                ev.target.parentElement.parentElement.removeChild(ev.target.parentElement);
                document.querySelector(`.movie_content_img_star[mvname='${movie_name}']`).removeAttribute("starsel");
            }
        };
        search_log_div.append(search_log_text);
        search_log_div.append(search_log_button);
        searbox_logger.append(search_log_div);
    }
    /**
     * 영화에 별점이 없을 때 별점을 주면 작동하는 함수
     * @param movie_name 영화 이름
     * @param value 점수
     */
    insertContent(movie_name, value) {
        if (Vars.SelectedMovies[movie_name] == undefined) {
            MovieContentHandler.getInstance.createLogSpan(movie_name);
        }
        let analysticsBTN = document.querySelector("#sendAnalysticsButton");
        if (analysticsBTN.getAttribute("isBlocked") != "false") {
            analysticsBTN.setAttribute("isBlocked", "false");
        }
        Vars.SelectedMovies[movie_name] = value;
    }
    /**
     * 컨텐츠를 관리 Object에서 삭제하는 함수
     * @param movie_name 영화 이름
     */
    removeContent(movie_name) {
        let analysticsBTN = document.querySelector("#sendAnalysticsButton");
        delete (Vars.SelectedMovies[movie_name]);
        if (Object.keys(Vars.SelectedMovies).length == 0) {
            analysticsBTN.setAttribute("isBlocked", "true");
        }
    }
    showList() {
        console.log(Vars.SelectedMovies);
    }
    AnalyzeMovieData() {
        return __awaiter(this, void 0, void 0, function* () {
            yield FetchAPI.postJSON("/protected/AnalyzeMovieData.do", Vars.SelectedMovies)
                .then((data) => {
                console.log(data);
            })
                .catch((err) => {
                console.error(err);
            });
        });
    }
}
/**
 * MovieContentHandler 인스턴스
 */
MovieContentHandler.getInstance = new MovieContentHandler();
export default MovieContentHandler;
