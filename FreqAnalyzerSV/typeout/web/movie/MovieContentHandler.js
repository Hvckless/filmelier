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
    createMoviePanel(movie_json, target_panel) {
        let movie_panel = target_panel; //document.querySelector("#movieContents");
        console.log(movie_json);
        if ((movie_json === null) || (movie_json === undefined)) {
            console.error("해당 영화를 찾을 수 없습니다.");
            return;
        }
        for (let movie of movie_json) {
            let movie_name = movie["name"];
            let movie_image = movie["image"];
            let mv_content = document.createElement('div');
            mv_content.classList.add('movie_content');
            let mv_content_image_div = document.createElement('div');
            mv_content_image_div.classList.add('movie_content_img_panel');
            mv_content_image_div.classList.add('relative');
            // let mv_content_image_like = document.createElement('div');
            // mv_content_image_like.classList.add('movie_content_img_like');
            // mv_content_image_like.classList.add('absolute');
            // mv_content_image_like.setAttribute("mvname", `${movie_name}`);
            let mv_content_image_star = document.createElement('div');
            mv_content_image_star.classList.add('movie_content_img_star');
            mv_content_image_star.classList.add('absolute');
            mv_content_image_star.setAttribute("mvname", `${movie_name}`);
            //starrealcheck = 체크된 경우 사용 | starcheck = 마우스가 올라간 경우 사용
            mv_content_image_star.onmouseleave = (ev) => {
                if (ev.target instanceof HTMLDivElement) {
                    ev.target.removeAttribute("starnum");
                }
            };
            let starcounter = Vars.SelectedMovies[`${movie_name}`];
            if (starcounter != undefined) {
                mv_content_image_star.setAttribute("starsel", starcounter);
            }
            let mv_content_image_realstar = document.createElement('div');
            mv_content_image_realstar.classList.add('emptystar');
            mv_content_image_realstar.classList.add('starlight');
            mv_content_image_realstar.setAttribute("starnum", "4");
            mv_content_image_realstar.onmouseenter = (ev) => {
                if (ev.target instanceof HTMLDivElement) {
                    ev.target.parentElement.setAttribute("starnum", ev.target.getAttribute("starnum"));
                }
            };
            // 스타를 클릭하는 경우 starsel에 숫자를 기입해 
            mv_content_image_realstar.onmousedown = (ev) => {
                if (ev.target instanceof HTMLDivElement) {
                    let starvalue = ev.target.parentElement.getAttribute("starsel");
                    if (starvalue == null) {
                        //값이 없음 (체크 안 됨)
                        ev.target.parentElement.setAttribute("starsel", ev.target.getAttribute("starnum"));
                        MovieContentHandler.getInstance.insertContent(`${movie_name}`, ev.target.getAttribute("starnum"));
                    }
                    else {
                        //값이 있는 경우 (체크 됨)
                        MovieContentHandler.getInstance.removeContent(ev.target.parentElement.getAttribute("mvname"));
                    }
                }
            };
            mv_content_image_star.append(mv_content_image_realstar);
            // for(let i = 0; i < 5; i++){
            //     let mv_content_image_realstar = document.createElement('div');
            //     mv_content_image_realstar.classList.add('emptystar');
            //     mv_content_image_realstar.classList.add('starlight');
            //     mv_content_image_realstar.setAttribute("starnum", i+"");
            //     mv_content_image_realstar.onmouseenter = (ev:MouseEvent)=>{
            //         if(ev.target instanceof HTMLDivElement){
            //             ev.target.parentElement.setAttribute("starnum", ev.target.getAttribute("starnum"));
            //         }
            //     }
            //     mv_content_image_realstar.onmousedown = (ev:MouseEvent)=>{
            //         if(ev.target instanceof HTMLDivElement){
            //             ev.target.parentElement.setAttribute("starsel", ev.target.getAttribute("starnum"));
            //             MovieContentHandler.getInstance.insertContent(`${movie_name}`, ev.target.getAttribute("starnum"));
            //         }
            //     }
            //     mv_content_image_star.append(mv_content_image_realstar);
            // }
            let mv_content_image = document.createElement('img');
            let movie_image_decoded = window.atob(`${movie_image}`);
            mv_content_image.setAttribute('src', `data:image/jpeg;base64,${movie_image_decoded}`);
            mv_content_image.classList.add('absolute');
            let mv_content_button_div = document.createElement('div');
            mv_content_button_div.classList.add("movie_text_div");
            //하단 코드는 릴리즈시 삭제
            mv_content_button_div.onclick = (ev) => {
                MovieContentHandler.getInstance.showList();
            };
            let mv_content_button_text = document.createElement('span');
            mv_content_button_text.textContent = `${movie_name}`;
            mv_content_button_div.append(mv_content_button_text);
            mv_content_image_div.append(mv_content_image);
            mv_content_image_div.append(mv_content_image_star);
            // mv_content_image_div.append(mv_content_image_like);
            mv_content.append(mv_content_image_div);
            mv_content.append(mv_content_button_div);
            movie_panel.append(mv_content);
        }
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
        search_log_button.setAttribute("sslog_mvname", movie_name);
        search_log_button.textContent = "X";
        search_log_button.onmousedown = (ev) => {
            if (ev.target instanceof HTMLDivElement) {
                //LogSpan 삭제 메서드 실행
                MovieContentHandler.getInstance.removeContent(ev.target.getAttribute("sslog_mvname"));
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
        document.querySelector("#searchLog").childNodes.forEach((element) => {
            var _a;
            if (element.querySelector("span.searchLog").textContent == movie_name) {
                document.querySelector("#searchLog").removeChild(element);
                (_a = document.querySelector(`.movie_content_img_star[mvname='${movie_name}']`)) === null || _a === void 0 ? void 0 : _a.removeAttribute("starsel");
            }
        });
        delete (Vars.SelectedMovies[movie_name]);
        if (Object.keys(Vars.SelectedMovies).length == 0) {
            analysticsBTN.setAttribute("isBlocked", "true");
        }
    }
    showList() {
        console.log(Vars.SelectedMovies);
    }
    AnalyzeMovieData(obj) {
        return __awaiter(this, void 0, void 0, function* () {
            if (obj instanceof HTMLDivElement) {
                let analyzeBTN = document.querySelector("#sendAnalysticsButton");
                if ((Object.keys(Vars.SelectedMovies).length > 0) && (analyzeBTN.getAttribute("isBlocked") == "false")) {
                    analyzeBTN.setAttribute("isBlocked", "true");
                    let ct_panel = document.querySelector("#movieContents");
                    ct_panel.innerHTML = "";
                    let loading_panel = document.querySelector("#loading");
                    loading_panel.classList.remove("invisible");
                    loading_panel.classList.add("showflex");
                    /**
                     * 영화 분석 파이썬 코드를 실행하는 API 호출
                     *
                     */
                    yield FetchAPI.postJSON("/protected/AnalyzeMovieData.do", Vars.SelectedMovies)
                        .then((data) => {
                        loading_panel.classList.remove("showflex");
                        loading_panel.classList.add("invisible");
                        document.querySelector("#ranking").classList.remove("invisible");
                        let originObject = data["reqMsg"];
                        let sendData = [];
                        Object.keys(originObject).forEach((key) => {
                            sendData.push(originObject[key]);
                        });
                        analyzeBTN.classList.remove("showflex");
                        analyzeBTN.classList.add("invisible");
                        MovieContentHandler.getInstance.getMoviePoster(sendData);
                    })
                        .catch((err) => {
                        console.error(err);
                    });
                }
            }
        });
    }
    getMoviePoster(param) {
        return __awaiter(this, void 0, void 0, function* () {
            yield FetchAPI.postJSON("/protected/RankSQL.do", param)
                .then((data) => {
                document.querySelector("#sendAnalysticsButton").classList.remove("showflex");
                MovieContentHandler.getInstance.createPosterPanel(data, document.querySelector("#ranking_toprank"));
            })
                .catch((err) => {
                console.error(err);
            });
        });
    }
    createPosterPanel(movie_json, target_panel) {
        let movie_panel = target_panel; //document.querySelector("#movieContents");
        for (let i = 0; i < movie_json.length; i++) {
            //let movie = movie_json[i]; //구버전 json 포맷에 맞춘 코드
            let movie = movie_json.find((movie_json) => movie_json["index"] == i);
            if (movie == undefined) {
                continue;
            }
            let movie_name = movie["name"];
            let movie_image = movie["image"];
            let poster_top = document.createElement('div');
            let poster_image_div = document.createElement('div');
            let poster_image = document.createElement('img');
            poster_image_div.classList.add("movie_content_img_panel");
            let movie_image_decoded = window.atob(`${movie_image}`);
            poster_image.setAttribute('src', `data:image/jpeg;base64,${movie_image_decoded}`);
            poster_image_div.append(poster_image);
            let poster_title_div = document.createElement('div');
            let poster_title = document.createElement('span');
            poster_title_div.classList.add("movie_text_div");
            poster_title.textContent = movie_name;
            poster_title_div.append(poster_title);
            poster_top.append(poster_image_div);
            poster_top.append(poster_title_div);
            poster_top.classList.add("poster");
            if (i < 3) {
                poster_top.classList.add("topposter");
                movie_panel.append(poster_top);
            }
            else {
                poster_top.classList.add("underposter");
                document.querySelector("#ranking_underrank").append(poster_top);
            }
        }
    }
}
/**
 * MovieContentHandler 인스턴스
 */
MovieContentHandler.getInstance = new MovieContentHandler();
export default MovieContentHandler;
