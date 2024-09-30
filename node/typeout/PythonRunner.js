import { spawn } from "node:child_process";
class PythonRunner {
    /**
     * 파이썬 파일과 연동하여 입력값을 전달하고 결과값을 받아오는 함수.
     * @param movieName
     */
    runScript(movieName) {
        return new Promise((resolve, reject) => {
            // python 스크립트와 영화 이름을 array 로 전달
            const movieNameString = movieName.join(',');
            const pythonProcess = spawn('python', ['../NLPyCodes/similarityRefac/similarityCalculator.py', movieNameString]);
            // 입력받은 값을 data 에 담아서 반환
            pythonProcess.stdout.on('data', (data) => {
                resolve(data.toString()); // 입력 받는 값는 buffer 객체로, 문자열로 변환
            });
            // 오류 처리
            pythonProcess.stderr.on('data', (data) => {
                reject(`Error: ${data.toString()}`);
            });
        });
    }
    ;
}
export default PythonRunner;
