var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
/**
 *
 * [CheckedReviewList, ReviewFileList]
 *
 * @param event
 */
self.onmessage = (event) => __awaiter(this, void 0, void 0, function* () {
    postMessage("\n분석 시작\n");
    let _movieDict = event.data[0];
    let _movieReview = event.data[1];
    let _movieAnalyzer = new MovieAnalyzer();
    _movieAnalyzer.setDictionary(_movieDict);
    _movieAnalyzer.setMovieFileList(_movieReview);
    postMessage(yield _movieAnalyzer.analyze());
});
class MovieAnalyzer {
    constructor() {
        this.movieFileList = null;
        this.selectedCNT = 0;
        this.selectedDictionary = {};
        this.sortDict = {};
    }
    analyze() {
        return __awaiter(this, void 0, void 0, function* () {
            return new Promise((resolve, reject) => __awaiter(this, void 0, void 0, function* () {
                let fileHandler = new FileHander();
                let checkedFileList;
                const promies = Array.from(this.movieFileList).map((file) => __awaiter(this, void 0, void 0, function* () {
                    try {
                        if (this.movieDictionary[file.name.split(".")[0]] == false)
                            return;
                        this.selectedCNT++;
                        this.sortDict[this.selectedCNT] = [];
                        postMessage("movie " + file.name.split(".")[0] + " loaded\n");
                        const data = yield fileHandler.readTextFile(file);
                        data.split(",").forEach((word) => {
                            if (this.selectedDictionary[word] == undefined) {
                                this.selectedDictionary[word] = [1, "undefined"];
                            }
                            else {
                                this.selectedDictionary[word][0]++;
                            }
                        });
                        postMessage(data + "\n");
                    }
                    catch (error) {
                        postMessage(error);
                    }
                }));
                yield Promise.all(promies);
                Object.entries(this.selectedDictionary).forEach(([key, value]) => {
                    if (key.length == 1) {
                        delete this.selectedDictionary[key];
                    }
                    if (value[0] == 1) {
                        delete this.selectedDictionary[key];
                    }
                    else {
                        //console.log(this.sortDict);
                        this.sortDict[value[0]].push(key);
                        value[1] = (value[0] / this.selectedCNT) * 100 + "%";
                    }
                });
                console.log(this.sortDict);
                console.log(this.selectedDictionary);
                postMessage("분석 완료-------------\n");
                Object.entries(this.selectedDictionary).forEach(([key, value]) => {
                    postMessage(key + " : " + value[1] + "\n");
                });
                resolve("work done\n");
            }));
        });
    }
    setDictionary(moviedict) {
        this.movieDictionary = moviedict;
    }
    getDictionary() {
        return this.movieDictionary;
    }
    setMovieFileList(filelist) {
        this.movieFileList = filelist;
    }
    getMovieFileList() {
        return this.movieFileList;
    }
}
/**
 * Worker 전용 파일 처리기
 */
class FileHander {
    readTextFile(file) {
        return __awaiter(this, void 0, void 0, function* () {
            return new Promise((resolve, reject) => {
                let reader = new FileReader();
                reader.readAsText(file, "utf-8");
                reader.onload = () => {
                    resolve(reader.result);
                };
                reader.onerror = () => {
                    reject(new Error("an error occured while reading the file"));
                };
            });
        });
    }
}
