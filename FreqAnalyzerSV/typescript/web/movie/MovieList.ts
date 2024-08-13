import MovieDict from "./MovieDict.js";

class MovieList{
    private constructor(){}

    public static getInstance:MovieList = new MovieList();

    public movieDictionary:MovieDict = {};
    public movieReviewList:FileList;

    /**
     * 딕셔너리의 특정 키값을 토글링하는 함수
     * @param element 포함값을 true, false로 토글할 딕셔너리 키
     */
    public toggleDictionary(element:string):void{
        if(this.movieDictionary[element]){
            this.movieDictionary[element] = false;
        }else{
            this.movieDictionary[element] = true;
        }
    }
}

export default MovieList;