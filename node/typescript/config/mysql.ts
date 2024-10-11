//let mysql = require("mysql");

import * as mysql from "mysql";

let db_info = {
    host     : 'localhost',
    user     : 'root',
    password : '3131',
    database : 'movie_db'
};

class MySQL{
    public init(){
        return mysql.createConnection(db_info);
    }
    public connect(conn:any){
        conn.connect((err:any)=>{
            if (err) console.error("mysql connection error : " + err);
            else console.log("mysql is  connected successfully");
        });
    }
}

export default MySQL;

// module.exports = {
//     init: () =>{
//         return mysql.createConnection(db_info);
//     },
//     connect: (conn)=>{
//         conn.connect((err)=>{
//             if (err) console.error("mysql connection error : " + err);
//             else console.log("mysql is connected successfully");
//         });
//     },
// };