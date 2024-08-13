/**
 * 
 * [CheckedReviewList, ReviewFileList]
 * 
 * @param event 
 */
self.onmessage = async (event)=>{

    postMessage("\n분석 시작\n");

    let _movieDict:MovieDict = event.data[0] as MovieDict;
    let _movieReview:FileList = event.data[1] as FileList;

    let _movieAnalyzer = new MovieAnalyzer();

    _movieAnalyzer.setDictionary(_movieDict);
    _movieAnalyzer.setMovieFileList(_movieReview);

    postMessage(await _movieAnalyzer.analyze());
    
    
}

class MovieAnalyzer{

    private movieDictionary:MovieDict;
    private movieFileList:FileList = null;

    private selectedCNT:number = 0;
    private selectedDictionary:MovieCount = {};

    private sortDict = {};



    public async analyze():Promise<string>{
        return new Promise(async (resolve, reject)=>{

            let fileHandler:FileHander = new FileHander();
            let checkedFileList:FileList;

            const promies:Promise<void>[] = Array.from(this.movieFileList).map(async (file:File)=>{
                try{
                    if(this.movieDictionary[file.name.split(".")[0]] == false)
                        return;

                    
                    this.selectedCNT++;
                    this.sortDict[this.selectedCNT] = [];
                    
                    postMessage("movie " + file.name.split(".")[0] + " loaded\n");

                    const data:string = await fileHandler.readTextFile(file);

                    data.split(",").forEach((word:string)=>{
                       if(this.selectedDictionary[word] == undefined){
                            this.selectedDictionary[word] = [1, "undefined"];
                       }else{
                            this.selectedDictionary[word][0]++;
                       }
                    });

                    
                    postMessage(data+"\n");
                }catch(error){
                    postMessage(error);
                }
            });

            await Promise.all(promies);

            Object.entries(this.selectedDictionary).forEach(([key, value])=>{
                if(key.length == 1){
                    delete this.selectedDictionary[key];
                }
                if(value[0]==1){
                    delete this.selectedDictionary[key];
                }else{
                    //console.log(this.sortDict);
                    this.sortDict[value[0]].push(key);
                    value[1] = (value[0]/this.selectedCNT)*100 + "%";
                }
                
            });
            console.log(this.sortDict);
            console.log(this.selectedDictionary);
            postMessage("분석 완료-------------\n");
            Object.entries(this.selectedDictionary).forEach(([key, value])=>{

                postMessage(key + " : " + value[1] + "\n");

            });
            resolve("work done\n");

        });
    }
    public setDictionary(moviedict:MovieDict):void{
        this.movieDictionary = moviedict;
    }
    public getDictionary():MovieDict{
        return this.movieDictionary;
    }
    public setMovieFileList(filelist:FileList):void{
        this.movieFileList = filelist;
    }
    public getMovieFileList():FileList{
        return this.movieFileList;
    }

}

/**
 * Worker 전용 파일 처리기
 */
class FileHander{
    public async readTextFile(file:File):Promise<string>{
        return new Promise((resolve, reject)=>{
            let reader:FileReader = new FileReader();
            reader.readAsText(file, "utf-8");

            reader.onload = ()=>{
                resolve(reader.result as string);
            }

            reader.onerror = ()=>{
                reject(new Error("an error occured while reading the file"));
            }
        });
    }
}

/**
 * Worker 전용 Dict타입
 */
type MovieDict = {
    [keys:string]:boolean;
}

type MovieCount = {
    [keys:string]:[int:number, percentage:string];
}