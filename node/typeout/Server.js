var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
import express from "express";
import GetMovie from "./GetMovie.js";
import PythonRunner from "./PythonRunner.js";
const app = express();
app.get("/movies/:paramMovieName", (req, res) => __awaiter(void 0, void 0, void 0, function* () {
    const paramMovieName = req.params.paramMovieName;
    try {
        // 영화 정보를 가져옴
        const movieResult = yield new GetMovie().getMovieInfo(paramMovieName);
        console.log("영화 이름:", paramMovieName);
        // 영화 정보에서 영화 이름만 추출
        if (movieResult != ' ') {
            const movieName = movieResult.map((movie) => movie.name);
            // 파이썬 파일에 영화 이름을 전달
            const pythonResult = yield new PythonRunner().runScript(movieName);
            const similarMovie = Object.keys(pythonResult);
            console.log("추천된 영화 이름:", pythonResult);
            const similarMovieInfo = yield new GetMovie().getSimilarMovieInfo(similarMovie);
            // 결과를 클라이언트에게 반환
            res.json({
                movies: movieResult, // 영화 정보
                pythonOutput: similarMovieInfo // 파이썬 스크립트 결과
            });
        }
        else {
            res.status(404).send("해당하는 영화를 찾을 수 없습니다");
        }
    }
    catch (err) {
        console.log("오류: ", err.message);
        res.status(500).send(err.message);
    }
}));
app.listen(3030, () => {
    console.log("서버3000  실행중");
});
