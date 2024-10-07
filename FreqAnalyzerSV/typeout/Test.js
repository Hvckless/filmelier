var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
import * as fs from "fs";
let url = "kinggod=world&koko=work";
function getParameter2(context) {
    let result = [];
    context.split("&").forEach((param) => {
        let paramFragment = param.split("=");
        if (paramFragment.length != 2) {
            throw new Error("parameter is not constructed correctly.");
        }
        else {
            let _map = {};
            _map[paramFragment[0]] = paramFragment[1];
            result.push(_map);
        }
    });
    return result;
}
let resultOne = getParameter2(url);
console.log(resultOne);
console.log("JSON stringify");
console.log(JSON.stringify(resultOne));
let moviename = "martian";
console.log("DataBuffer Rewrite Test...");
function getMoviePoster(context) {
    return __awaiter(this, void 0, void 0, function* () {
        return new Promise((resolve, reject) => __awaiter(this, void 0, void 0, function* () {
            let result = {};
            let file = fs.readFileSync(`./src/image/ignore/${context}.jfif`);
            result[context] = file;
            const somemodule = yield import("./TestDynamic.js");
            new somemodule["TestDynamic"]().initial();
            resolve(result);
        }));
    });
}
//console.log(getMoviePoster(moviename));
getMoviePoster(moviename)
    .then((data) => {
    console.log(data);
    console.log(Buffer.from(data["martian"]).toString("base64"));
    console.log(JSON.stringify(data));
})
    .catch((err) => {
    console.error(err);
});
