class FilmAnimation{
    public startSearhFieldLoading(element:HTMLInputElement):NodeJS.Timeout{
        console.log("START ANIMATION!");

        let kokowork:NodeJS.Timeout = setInterval(()=>{
            console.log("animating...");
        }, 1000);

        return kokowork;
    }
}

export default FilmAnimation;