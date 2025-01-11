import * as mysql from "mysql2";
class MySQL {
    constructor() {
        this.connection = null;
        this.db_info = {
            host: '192.168.0.11',
            port: 3306,
            user: 'root',
            password: '1234',
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
