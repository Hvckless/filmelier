import FileHandler from "../file/FileHandler.js";

class BufferHandler{
    public async Image2Buffer():Promise<void>{

        let hello:ArrayBuffer = await new FileHandler().readImageFile();

        console.log(hello);

    }
}

export default BufferHandler;