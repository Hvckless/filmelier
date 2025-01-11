import { Parameter } from "../type/Parameter";

interface PythonRunner{
    /**
     * 
     * @param param 
     * @returns 파이썬 코드가 반환하는 데이터
     */
    execute(param:Parameter):Promise<string>;
}

export default PythonRunner;