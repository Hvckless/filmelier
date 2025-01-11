import GlobalDefine from "../variables/GlobalDefine.js";
import MovieListHandler from "../movie/MovieListHandler.js";
class ClickHandler {
    constructor() {
        document.querySelectorAll(".editor-tabmenu-content").forEach((element) => {
            GlobalDefine.tabmenu_content.push(element);
        });
    }
    /**
     * 탭메뉴를 클릭했을 때 탭이 변경되도록 하는 함수
     * @param ev 마우스 이벤트
     */
    tabmenuClickEvent(ev) {
        // let htmlElement:any = document.querySelectorAll(".editor-tabmenu-font");
        // if(!(htmlElement instanceof HTMLSpanElement)){
        //     return;
        // }
        // htmlElement.onclick = (ev:MouseEvent)=>{
        //     console.log("HELLO WORLD?");
        // }
        if (!(ev.target instanceof HTMLSpanElement)) {
            throw new Error("Target Element may not Tabmenu. It mustbe span element");
        }
        let target = document.querySelector(`div[name='${ev.target.textContent}'`);
        if (!(target instanceof HTMLDivElement)) {
            throw new Error("Div Element Not Found. You Find about " + ev.target.textContent);
        }
        GlobalDefine.tabmenu_content.forEach((element) => {
            element.classList.remove("show");
            element.classList.add("hidden");
        });
        target.classList.remove("hidden");
        target.classList.add("show");
    }
    addMovieClickEvent(ev) {
        // if(!(ev.target instanceof HTMLDivElement)){
        //     throw new Error("Target Element may not Tabmenu. It mustbe Div element");
        // }
        let target = ev.target;
        console.log(target.parentElement);
        let movie_title = target.parentElement.querySelector("input[name='영화 제목']").value;
        let movie_review = target.parentElement.querySelector("textarea[name='영화 리뷰']").value.split("\n");
        MovieListHandler.instance.addMovieComponent(movie_title, movie_review);
    }
}
export default ClickHandler;
