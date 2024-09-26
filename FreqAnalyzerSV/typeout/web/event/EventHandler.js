import BufferHandler from "../test/BufferHandler.js";
class EventHandler {
    increaseCounter() {
        let spanElement = document.querySelector("#contentPanel > span");
        spanElement.textContent = (parseInt(spanElement.textContent) + 1) + "";
    }
    printBuffer() {
        new BufferHandler().Image2Buffer();
    }
}
export default EventHandler;
