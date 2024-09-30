import express from "express";
import GetMovie from "./GetMovie.js";

const app = express();

app.get("/movies/:paramMovieName", (req: any, res: any) => {
    const paramMovieName = req.params.paramMovieName;

    new GetMovie().getMovieInfo(paramMovieName, (err: Error, result) => {
        if (err) {
            console.log("오류:", err.message);
            return res.status(500).send(err.message)
        }

        res.json({
            movies:result
        });
    });
});

app.listen(3000, ()=>{
    console.log("서버3000  실행중")

})
