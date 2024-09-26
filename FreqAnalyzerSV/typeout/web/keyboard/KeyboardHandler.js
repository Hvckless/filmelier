var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
import FileHandler from "../file/FileHandler.js";
import MoviePanelHandler from "../movie/MoviePanelHandler.js";
import MovieList from "../movie/MovieList.js";
import Console from "../console/Console.js";
import Search from "../search/Search.js";
class KeyboardHandler {
    onkeydown(event) {
        let movieHandler = new MoviePanelHandler();
        switch (event.code) {
            case 'KeyC': {
                /**
                 * 영화 목록을 받아오는 코드
                 */
                (() => __awaiter(this, void 0, void 0, function* () {
                    let sometext = yield new FileHandler().readTextFile();
                    let textsplit = sometext.split("\r\n");
                    movieHandler.createMoviePanel(textsplit.length, textsplit);
                }))();
                break;
            }
            case 'KeyV': {
                (() => __awaiter(this, void 0, void 0, function* () {
                    let filelist = yield new FileHandler().uploadDirectory();
                    MovieList.getInstance.movieReviewList = filelist;
                    Array.from(filelist).forEach((file) => {
                        let filename = file.name.split(".")[0];
                        MovieList.getInstance.movieDictionary[filename] = false;
                    });
                    movieHandler.createMoviePanel(filelist.length, Object.keys(MovieList.getInstance.movieDictionary));
                }))();
                break;
            }
            case 'KeyB': {
                let worker = new Worker("../../typeout/web/worker/MovieAnalyzer.js");
                worker.postMessage([MovieList.getInstance.movieDictionary, MovieList.getInstance.movieReviewList]);
                worker.onmessage = (event) => {
                    //콘솔 로그
                    Console.getInstance.sendLog(event.data);
                    //최하단으로 스크롤
                    let consoleDiv = document.querySelector("#console");
                    consoleDiv.scrollTo(0, consoleDiv.scrollHeight);
                };
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
            case 'Enter': {
                new Search().submit(event.target);
                break;
            }
            default: {
                console.log("YOU PRESSED UNKNOWN KEY");
            }
        }
    }
}
export default KeyboardHandler;
