import path from "path"
import {spawn} from "node:child_process";

class PythonRunner {
    /**
     * 파이썬 파일과 연동 하여 영화 이름을 전달하고 추천 영화를 받아오는 함수.
     * 사용자가 입력한 영화를 , 로 구분된 문자열로 전달하고,
     * 파이썬에서 Json 으로 결과값을 보내주면 그대로 Json 으로 파싱하여 받아 반환한다.
     * @param movieName
     */
    public runScript(movieName:any) {
        return new Promise((resolve, reject) =>{
            // python 스크립트와 영화 이름을 array 로 전달
            const movieNameString = movieName.join(',') // 영화 이름들을 문자열로 전달
            const pythonProcess = spawn('python', ['../NLPyCodes/similarityRefac/similarityCalculator.py', movieNameString]);

            // 입력받은 값을 data 에 담아서 반환
            pythonProcess.stdout.on('data', (data)=>{
                try {
                    // data 를 Json 으로 변환
                    const parseData = JSON.parse(data.toString());
                    resolve(parseData); // Json 결과
                } catch (error){
                    reject(`Json 파싱 오류 : ${error.message}`);
                }
            });

            // 오류 처리
            pythonProcess.stderr.on('data', (data) =>{
                reject(`Error: ${data.toString()}`);
            });
        });
    };

}

export default PythonRunner;

