from flask_mysqldb import MySQL

def init_db(app):
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'       
    app.config['MYSQL_PASSWORD'] = 'berkay123'
    app.config['MYSQL_DB'] = 'recipe_generator'
    mysql = MySQL(app)
    return mysql
    
    
