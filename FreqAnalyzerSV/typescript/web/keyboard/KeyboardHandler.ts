import FileHandler from "../file/FileHandler.js";
import MoviePanelHandler from "../movie/MoviePanelHandler.js";
import MovieList from "../movie/MovieList.js";

import Console from "../console/Console.js";

class KeyboardHandler{
    public onkeydown(event){

        let movieHandler:MoviePanelHandler = new MoviePanelHandler();



        switch(event.code){
            case 'KeyC': {
                (
                    async ()=>{
                        let sometext:string = await new FileHandler().readTextFile();
                        let textsplit:string[] = sometext.split("\r\n");
                        
                        movieHandler.createMoviePanel(textsplit.length, textsplit);
                    }
                )();
                break;
            }
            case 'KeyV': {
                (
                    async ()=>{
                        let filelist:FileList = await new FileHandler().uploadDirectory();

                        MovieList.getInstance.movieReviewList = filelist;

                        

                        Array.from(filelist).forEach((file)=>{
                            let filename:string = file.name.split(".")[0];

                            MovieList.getInstance.movieDictionary[filename] = false;
                        });

                        movieHandler.createMoviePanel(filelist.length, Object.keys(MovieList.getInstance.movieDictionary));
                    }
                )();

                break;
            }
            case 'KeyB': {
                let worker = new Worker("../../typeout/web/worker/MovieAnalyzer.js");

                worker.postMessage([MovieList.getInstance.movieDictionary, MovieList.getInstance.movieReviewList])



                worker.onmessage = (event)=>{

                    //콘솔 로그
                    Console.getInstance.sendLog(event.data);

                    //최하단으로 스크롤
                    let consoleDiv = document.querySelector("#console") as HTMLDivElement;
                    consoleDiv.scrollTo(0, consoleDiv.scrollHeight);

                }

                break;
            }
            case 'KeyZ': {
                console.log(MovieList.getInstance.movieDictionary);
                break;
            }
            case 'KeyQ': {
                //콘솔 토글

                Console.getInstance.toggle();

                break;
            }
            default : {
                console.log("YOU PRESSED UNKNOWN KEY");
            }
        }
    }
}

export default KeyboardHandler;