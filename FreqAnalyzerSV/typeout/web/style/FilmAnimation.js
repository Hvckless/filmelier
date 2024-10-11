class FilmAnimation {
    constructor() {
        this.loadingStates = ["검색중.", "검색중..", "검색중..."];
    }
    startSearhFieldLoading(element) {
        let index = 0;
        let animation = setInterval(() => {
            element.placeholder = this.loadingStates[index];
            index = (index + 1) % this.loadingStates.length;
        }, 333);
        return animation;
    }
}
export default FilmAnimation;
