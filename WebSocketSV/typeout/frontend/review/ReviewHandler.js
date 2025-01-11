class ReviewHandler {
    constructor() {
        this.categories = [];
        document.querySelector("#editor-content").querySelectorAll("input").forEach((element) => {
            this.categories.push(element.value);
        });
    }
}
export default ReviewHandler;
