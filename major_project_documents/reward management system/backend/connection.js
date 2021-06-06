var mysql = require('mysql');

var connection      =   mysql.createPool({
    host     : 'localhost',
    user     : 'cert',
    password : 'password',
    database : 'certificates',
    port:3306,
    connectionLimit : 10,
    debug    :  false
});


connection.getConnection(function(err) {
    if (err) throw err;
    else 
    console.log("success");
    connection.on('error', function(err) {      
        if(err) throw err;
        else
        console.log("connectioon on");
        return;     
  });
});

module.exports = connection;


