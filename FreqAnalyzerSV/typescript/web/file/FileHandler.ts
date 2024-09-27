class FileHandler{
    /**
     * 사용 금지
     * @deprecated
     * @param event 
     */
    public readFile(event:Event){
        let reader = new FileReader();

        reader.readAsText((event.target as HTMLInputElement).files[0] ,"UTF-8");

        reader.onload = ():string|ArrayBuffer=>{
            return reader.result;
        }
    }
    public async readTextFile():Promise<string>{

        return new Promise((resolve, reject)=>{

            let file:HTMLInputElement = document.createElement('input');
            let reader:FileReader = new FileReader();
            file.type = "file";
            file.accept = ".txt";

            file.onchange = (event) => {
                reader.readAsText((event.target as HTMLInputElement).files[0], "UTF-8");
            };

            reader.onload = ()=>{
                resolve(reader.result as string);
            }

            reader.onerror = ()=>{
                reject(new Error("an Error occured while reading file"));
            }

            file.click();
        });
    }
    public async readImageFile():Promise<ArrayBuffer>{
        return new Promise((resolve, reject)=>{
            let file:HTMLInputElement = document.createElement('input');
            let reader:FileReader = new FileReader();
            file.type = "file";
            file.accept = ".jpg, .png";

            file.onchange = (event) => {
                if(event.target instanceof HTMLInputElement){
                    reader.readAsArrayBuffer(event.target.files[0]);
                }
            };

            reader.onload = ()=>{

                if(reader.result instanceof ArrayBuffer){
                    resolve(reader.result);
                }
            }

            reader.onerror = ()=>{
                reject(new Error("an Error occured while reading file"));
            }

            file.click();
        });
    }
    public uploadFile():void{

    }
    public async uploadDirectory():Promise<FileList>{
        let uploadFolder = document.createElement('input');

        uploadFolder.type="file";
        uploadFolder.setAttribute("webkitdirectory", "");


        uploadFolder.click();



        return new Promise((resolve, reject)=>{
            uploadFolder.onchange = async (event)=>{
                let files:FileList = (event.target as HTMLInputElement).files;

                if(files){
                    resolve(files);
                }else{
                    reject(new Error("no files selected"));
                }
            }
        });

        
    }
}

export default FileHandler;