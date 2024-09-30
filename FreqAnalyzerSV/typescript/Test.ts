import * as fs from "fs";


let url:string = "kinggod=world&koko=work";

type newTypeParameter = Array<KeyPair2>;
type KeyPair2 = {[key:string]:string};


function getParameter2(context:string):newTypeParameter{

    let result:newTypeParameter = [];

    context.split("&").forEach((param:string)=>{

        let paramFragment:Array<string> = param.split("=");

        if(paramFragment.length != 2){
            throw new Error("parameter is not constructed correctly.");
        }else{
            let _map:KeyPair2 = {};

            _map[paramFragment[0]] = paramFragment[1];

            result.push(_map);
        }

    });

    return result;
}


let resultOne:newTypeParameter = getParameter2(url);

console.log(resultOne);
console.log("JSON stringify");
console.log(JSON.stringify(resultOne));









let moviename:string = "martian";



console.log("DataBuffer Rewrite Test...");


type BufferJSON = {
    [moviename:string]:Buffer;
};

async function getMoviePoster(context:string):Promise<BufferJSON>{
    return new Promise(async (resolve, reject)=>{
        let result:BufferJSON = {};

        let file:Buffer = fs.readFileSync(`./src/image/ignore/${context}.jfif`);

        result[context] = file;

        
        const somemodule = await import("./TestDynamic.js");

        new somemodule["TestDynamic"]().initial();

        resolve(result);

    });

}


//console.log(getMoviePoster(moviename));


getMoviePoster(moviename)
    .then((data:BufferJSON)=>{
        console.log(data);
        console.log(Buffer.from(data["martian"]).toString("base64"));
        console.log(JSON.stringify(data));
    })
    .catch((err:any)=>{
        console.error(err);
    });
