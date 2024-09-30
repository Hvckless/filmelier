class TransitionHandler{

    public applyTransition():void{
        let module:NodeListOf<HTMLElement> = document.querySelectorAll(".waitTransition");

        module.forEach((element:HTMLElement)=>{

            if(element.classList.contains("trans-Nav")){
                element.classList.add("transition-navigation");
            }

            if(element.classList.contains("trans-WidthHeight")){
                element.classList.add("transition-WidthHeight");
            }

        });
    }

}

export default TransitionHandler;