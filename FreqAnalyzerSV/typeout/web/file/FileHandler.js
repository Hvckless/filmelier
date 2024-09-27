var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
class FileHandler {
    /**
     * 사용 금지
     * @deprecated
     * @param event
     */
    readFile(event) {
        let reader = new FileReader();
        reader.readAsText(event.target.files[0], "UTF-8");
        reader.onload = () => {
            return reader.result;
        };
    }
    readTextFile() {
        return __awaiter(this, void 0, void 0, function* () {
            return new Promise((resolve, reject) => {
                let file = document.createElement('input');
                let reader = new FileReader();
                file.type = "file";
                file.accept = ".txt";
                file.onchange = (event) => {
                    reader.readAsText(event.target.files[0], "UTF-8");
                };
                reader.onload = () => {
                    resolve(reader.result);
                };
                reader.onerror = () => {
                    reject(new Error("an Error occured while reading file"));
                };
                file.click();
            });
        });
    }
    readImageFile() {
        return __awaiter(this, void 0, void 0, function* () {
            return new Promise((resolve, reject) => {
                let file = document.createElement('input');
                let reader = new FileReader();
                file.type = "file";
                file.accept = ".jpg, .png";
                file.onchange = (event) => {
                    if (event.target instanceof HTMLInputElement) {
                        reader.readAsArrayBuffer(event.target.files[0]);
                    }
                };
                reader.onload = () => {
                    if (reader.result instanceof ArrayBuffer) {
                        resolve(reader.result);
                    }
                };
                reader.onerror = () => {
                    reject(new Error("an Error occured while reading file"));
                };
                file.click();
            });
        });
    }
    uploadFile() {
    }
    uploadDirectory() {
        return __awaiter(this, void 0, void 0, function* () {
            let uploadFolder = document.createElement('input');
            uploadFolder.type = "file";
            uploadFolder.setAttribute("webkitdirectory", "");
            uploadFolder.click();
            return new Promise((resolve, reject) => {
                uploadFolder.onchange = (event) => __awaiter(this, void 0, void 0, function* () {
                    let files = event.target.files;
                    if (files) {
                        resolve(files);
                    }
                    else {
                        reject(new Error("no files selected"));
                    }
                });
            });
        });
    }
}
export default FileHandler;
