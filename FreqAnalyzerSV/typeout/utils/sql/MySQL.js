import * as mysql from "mysql";
class MySQL {
    constructor() {
        this.connection = null;
        this.db_info = {
            host: '192.168.0.61',
            user: 'root',
            password: '3131',
            database: 'movie_db'
        };
        this.connection = mysql.createConnection(this.db_info);
        this.connection.connect((err) => {
            if (err)
                console.error("mysql connection error : " + err);
            else
                console.log("mysql is connected successfully");
        });
    }
    getConnection() {
        return MySQL.instance.connection;
    }
}
MySQL.instance = new MySQL();
export default MySQL;
