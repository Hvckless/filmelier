class MovieList {
    constructor() {
        this.movieDictionary = {};
    }
    /**
     * 딕셔너리의 특정 키값을 토글링하는 함수
     * @param element 포함값을 true, false로 토글할 딕셔너리 키
     */
    toggleDictionary(element) {
        if (this.movieDictionary[element]) {
            this.movieDictionary[element] = false;
        }
        else {
            this.movieDictionary[element] = true;
        }
    }
}
MovieList.getInstance = new MovieList();
export default MovieList;
