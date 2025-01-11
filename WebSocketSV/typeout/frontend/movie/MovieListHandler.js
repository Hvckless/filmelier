import GlobalDefine from "../variables/GlobalDefine.js";
class MovieListHandler {
    constructor() { }
    addMovieComponent(title, review) {
        if (GlobalDefine.movie_content_list[title] == null) {
            let tabmenu_movie_panel = document.querySelector("#editor-movielist-review-panel");
            let top_movie_panel = document.createElement('div');
            top_movie_panel.classList.add("editor-movielist-movie");
            let movie_title_component = document.createElement('span');
            movie_title_component.textContent = title;
            movie_title_component.onclick = () => {
                GlobalDefine.movie_review_name = movie_title_component.textContent;
                GlobalDefine.movie_review_index = 0;
                this.renderMovieReview();
            };
            let movie_delete_component = document.createElement('div');
            movie_delete_component.classList.add("editor-movielist-movie-deleteBTN");
            top_movie_panel.append(movie_title_component);
            top_movie_panel.append(movie_delete_component);
            tabmenu_movie_panel.append(top_movie_panel);
        }
        GlobalDefine.movie_content_list[title] = review;
    }
    renderMovieReview() {
        // console.log(target);
        // console.log(GlobalDefine.movie_content_list[target.textContent][114]);
    }
}
MovieListHandler.instance = new MovieListHandler();
export default MovieListHandler;
