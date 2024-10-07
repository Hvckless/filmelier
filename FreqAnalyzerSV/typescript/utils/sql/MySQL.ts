import * as mysql from "mysql";

class MySQL{
    public static instance:MySQL = new MySQL();

    

    private connection:mysql.Connection = null;

    private db_info = {
        host        : '192.168.0.61',
        user        : 'root',
        password    : '3131',
        database    : 'movie_db'
    }






    
    private constructor(){
        this.connection = mysql.createConnection(this.db_info);

        this.connection.connect((err:any)=>{
            if(err)
                console.error("mysql connection error : " + err);
            else
                console.log("mysql is connected successfully");
        });
    }

    public getConnection():mysql.Connection{
        return MySQL.instance.connection;
    }
}

export default MySQL;