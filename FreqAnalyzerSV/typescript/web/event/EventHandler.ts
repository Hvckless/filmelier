import BufferHandler from "../test/BufferHandler.js";

class EventHandler{
    public increaseCounter(){
        let spanElement:HTMLSpanElement = document.querySelector("#contentPanel > span");
        spanElement.textContent = (parseInt(spanElement.textContent)+1)+"";
    }
    public printBuffer(){
        new BufferHandler().Image2Buffer();
    }
}

export default EventHandler;