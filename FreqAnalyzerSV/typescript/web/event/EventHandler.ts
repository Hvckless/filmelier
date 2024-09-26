class EventHandler{
    public increaseCounter(){
        let spanElement:HTMLSpanElement = document.querySelector("#contentPanel > span");
        spanElement.textContent = (parseInt(spanElement.textContent)+1)+"";
    }
}

export default EventHandler;