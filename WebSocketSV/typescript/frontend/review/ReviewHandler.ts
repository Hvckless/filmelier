import GlobalDefine from "../variables/GlobalDefine.js";

class ReviewHandler{

    categories:Array<string> = [];

    constructor(){
        document.querySelector("#editor-content").querySelectorAll("input").forEach((element)=>{
            this.categories.push(element.value);
        });
    }
}

export default ReviewHandler;