class EventHandler {
    increaseCounter() {
        let spanElement = document.querySelector("#contentPanel > span");
        spanElement.textContent = (parseInt(spanElement.textContent) + 1) + "";
    }
}
export default EventHandler;
