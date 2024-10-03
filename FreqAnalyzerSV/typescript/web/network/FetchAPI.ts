import JSONObject from "../../utils/type/JSONObject";

class FetchAPI{
    static async getJSON(url:string):Promise<JSONObject>{

        return new Promise((resolve, reject)=>{
            fetch(url)
                .then((response)=>response.json()
                )
                .then((data)=>{
                    if(data instanceof Object){
                        resolve(data as JSONObject);
                    }else{
                        reject({"resMsg":"reponse is not JSON Object"});
                    }
                });
        });

    }
}


export default FetchAPI;