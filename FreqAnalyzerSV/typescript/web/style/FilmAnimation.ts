class FilmAnimation{
    private loadingStates:Array<string> = ["검색중.", "검색중..", "검색중..."];
    public startSearhFieldLoading(element:HTMLInputElement):NodeJS.Timeout{

        let index = 0;
        
        let animation:NodeJS.Timeout = setInterval(() => {
            element.placeholder = this.loadingStates[index];
            index = (index + 1) % this.loadingStates.length;
        }, 333);

        return animation
    }
}

export default FilmAnimation;