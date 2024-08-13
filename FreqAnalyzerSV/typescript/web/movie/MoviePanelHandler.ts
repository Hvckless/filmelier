import ClassToggler from '../../utils/ClassToggler.js';
import MovieList from './MovieList.js';

class MoviePanelHandler{
    public createMoviePanel(amount:number, movielist:string[]):void{

        for(let i = 0; i < amount; i++){
            let panel = document.createElement("div");
            panel.className = "movieContent";

            let text = document.createElement("span");
            text.textContent = movielist[i];

            panel.append(text);

            panel.addEventListener("mousedown", (event)=>{
                this.onClick(event);
            });

            document.querySelector("#movieWrapper").append(panel);
        }

    }
    /**
     * @param event 이벤트
     */
    private onClick(event:MouseEvent):void{

        let moviePanel:HTMLDivElement = event.target as HTMLDivElement;

        let classToggler:ClassToggler = new ClassToggler();

        classToggler.toggle(moviePanel, "movieChecked");
        MovieList.getInstance.toggleDictionary(moviePanel.querySelector("span").textContent);


    }
}

export default MoviePanelHandler;