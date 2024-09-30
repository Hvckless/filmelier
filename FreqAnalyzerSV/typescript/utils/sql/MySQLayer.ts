interface MySQLayer{
    searchMovies(context:string):Array<string>;
    getMoviePoster(moviename:string):Buffer;
}

export default MySQLayer;