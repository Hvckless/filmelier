class FilmAnimation {
    constructor() {
        this.loadingStates = ["Loading.", "Loading..", "Loading..."];
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
