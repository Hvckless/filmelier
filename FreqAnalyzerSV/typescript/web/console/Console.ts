class Console{
    private constructor(){

    }
    public static getInstance:Console = new Console();

    public getConsole = document.querySelector("#console");
    public getLogger = this.getConsole.querySelector("span");

    public toggle():void{
        if(this.getConsole.classList.contains("invisible")){
            this.getConsole.classList.remove("invisible");
            document.querySelector("#movieWrapper").classList.add("blur");
        }else{
            this.getConsole.classList.add("invisible");
            document.querySelector("#movieWrapper").classList.remove("blur");
        }
    }
    

    public sendLog(message:string):void{

        this.getLogger.textContent += message;

    }
}

export default Console;