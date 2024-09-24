const mysql = require('mysql');



let connection = mysql.createConnection({
    host     : 'localhost',
    user     : 'root',
    password : '3131',
    database : 'movie_db'
});

connection.connect();

connection.query('SELECT movie_name from movie_info' , function (error, results, fields) {
    if (error) throw error;
    console.log('The solution is: ', results);
});

connection.end();