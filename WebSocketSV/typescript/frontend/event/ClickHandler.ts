import GlobalDefine from "../variables/GlobalDefine.js";
import MovieListHandler from "../movie/MovieListHandler.js";

class ClickHandler{

    constructor(){
        document.querySelectorAll(".editor-tabmenu-content").forEach((element)=>{
            GlobalDefine.tabmenu_content.push(element);
        });
    }

    /**
     * 탭메뉴를 클릭했을 때 탭이 변경되도록 하는 함수
     * @param ev 마우스 이벤트
     */
    tabmenuClickEvent(ev:MouseEvent){

        // let htmlElement:any = document.querySelectorAll(".editor-tabmenu-font");

        // if(!(htmlElement instanceof HTMLSpanElement)){
        //     return;
        // }

        // htmlElement.onclick = (ev:MouseEvent)=>{
        //     console.log("HELLO WORLD?");
        // }

        if(!(ev.target instanceof HTMLSpanElement)){
            throw new Error("Target Element may not Tabmenu. It mustbe span element");
        }

        let target = document.querySelector(`div[name='${ev.target.textContent}'`);

        if(!(target instanceof HTMLDivElement)){
            throw new Error("Div Element Not Found. You Find about " + ev.target.textContent);
        }


        GlobalDefine.tabmenu_content.forEach((element:HTMLElement)=>{
            element.classList.remove("show");
            element.classList.add("hidden");
        });

        target.classList.remove("hidden");
        target.classList.add("show");


    }

    addMovieClickEvent(ev:MouseEvent){
        // if(!(ev.target instanceof HTMLDivElement)){
        //     throw new Error("Target Element may not Tabmenu. It mustbe Div element");
        // }

        let target = ev.target as HTMLElement;

        console.log(target.parentElement);

        let movie_title:string = (target.parentElement.querySelector("input[name='영화 제목']") as HTMLInputElement).value;
        let movie_review:Array<string> = (target.parentElement.querySelector("textarea[name='영화 리뷰']") as HTMLTextAreaElement).value.split("\n");

        MovieListHandler.instance.addMovieComponent(movie_title, movie_review);
    }

}

export default ClickHandler;