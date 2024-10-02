import express from "express";
import GetMovie from "./GetMovie.js";
import PythonRunner from "./PythonRunner.js";

const app = express();

app.get("/movies/:paramMovieName", async (req: any, res: any) => {
    const paramMovieName = req.params.paramMovieName; // 사용자가 입력한 영화 이름

    try{
        // 영화 정보를 가져옴
        const movieResult:any = await new GetMovie().getMovieInfo(paramMovieName);
        console.log("영화 이름:", paramMovieName)

        // 영화 정보에서 영화 이름만 추출
        if (movieResult.length > 0) { // 영화 정보가 존재 하면
            console.log("영화 이름을 가져옵니다")
            // 객체 배열을 돌며 name 속성 만 추출하여 새로운 배열을 생성
            const movieName:string[] = movieResult.map((movie:any) => movie.name);

            // 파이썬 파일에 영화 이름을 전달
            const pythonResult:any = await new PythonRunner().runScript(movieName);

            // 파이썬 파일에서 받는 객체 배열을 돌며 name 속성 만 추출하여 새로운 배열을 생성
            const similarMovie:string[] = pythonResult.map((movie:any) => movie.name);
            console.log("추천된 영화 이름:", pythonResult)

            // 전달 받은 객체 배열에 있는 영화 검색
            const similarMovieInfo = await new GetMovie().getSimilarMovieInfo(similarMovie);


            // 영화 정보 및 결과를 클라이언트에게 Json 으로 반환
            res.json({
                movies: movieResult,        // 사용자가 입력한 영화 정보
                pythonOutput: similarMovieInfo  // 영화를 기반으로 추천된 영화들
            });
        } else { // 영화 정보가 없으면
            res.status(404).send("해당하는 영화를 찾을 수 없습니다");
        }
    }catch (err){
        console.log("오류: ", err.message);
        res.status(500).send(err.message)
    }


});

app.listen(3030, ()=>{
    console.log("서버3000  실행중")

})

