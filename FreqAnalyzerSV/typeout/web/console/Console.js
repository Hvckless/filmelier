class Console {
    constructor() {
        this.getConsole = document.querySelector("#console");
        this.getLogger = this.getConsole.querySelector("span");
    }
    toggle() {
        if (this.getConsole.classList.contains("invisible")) {
            this.getConsole.classList.remove("invisible");
            document.querySelector("#movieWrapper").classList.add("blur");
        }
        else {
            this.getConsole.classList.add("invisible");
            document.querySelector("#movieWrapper").classList.remove("blur");
        }
    }
    sendLog(message) {
        this.getLogger.textContent += message;
    }
}
Console.getInstance = new Console();
export default Console;
