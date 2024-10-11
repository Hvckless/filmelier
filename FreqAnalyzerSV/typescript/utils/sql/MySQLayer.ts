import MovieJSON from "../type/MovieJSON";

interface MySQLayer{
    searchDataList(context:string):MovieJSON;
}

export default MySQLayer;