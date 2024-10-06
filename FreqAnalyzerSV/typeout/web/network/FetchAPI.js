var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
class FetchAPI {
    static getJSON(url) {
        return __awaiter(this, void 0, void 0, function* () {
            return new Promise((resolve, reject) => {
                fetch(url)
                    .then((response) => response.json())
                    .then((data) => {
                    if (data instanceof Object) {
                        resolve(data);
                    }
                    else {
                        reject({ "resMsg": "reponse is not JSON Object" });
                    }
                });
            });
        });
    }
    static postJSON(url, data) {
        return __awaiter(this, void 0, void 0, function* () {
            return new Promise((resolve, reject) => {
                fetch(url, {
                    method: "POST",
                    body: JSON.stringify(data)
                })
                    .then((response) => response.json())
                    .then((data) => {
                    if (data instanceof Object) {
                        resolve(data);
                    }
                    else {
                        reject({ "resMsg": "reponse is not JSON Object" });
                    }
                });
            });
        });
    }
}
export default FetchAPI;
