class MovieContentHandler {
    createMoviePanel(movie_json) {
        let movie_panel = document.querySelector("#movieContents");
        movie_json.forEach((movie) => {
            Object.keys(movie).forEach((movie_name) => {
                let object_string = `

                    <div class="movie_content">
                        <image src="data:image/jpeg;base64,${movie[movie_name]}">
                        <div>
                            <span>${movie_name}</span>
                        </div>
                    </div>

                `;
                movie_panel.innerHTML += object_string;
            });
        });
        // Object.keys(movie_json).forEach((movie)=>{
        //     let object_string:string = `
        //         <div class="movie_content">
        //             <image src="data:image/jpeg;base64,${movie_json[movie]}">
        //             <div>
        //                 <span>${movie}</span>
        //             </div>
        //         </div>
        //     `;
        //     movie_panel.innerHTML += object_string;
        // });
    }
}
export default MovieContentHandler;
