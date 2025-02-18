from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session
from app.db import create_connection
import bcrypt

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM users WHERE email='{email}'")
            user = cursor.fetchone()
            if user:
                decrypted_password = bcrypt.checkpw(password.encode('utf-8'), user[3].encode('utf-8'))
                if decrypted_password:
                    session['user'] = user
                    session['user_id'] = user[0]
                    return redirect(url_for('recipe_bp.recipe'))
                else:
                    return render_template('login.html', error='Invalid password')
            else:
                return render_template('login.html', error='User with this email does not exist')
        else:
            return render_template('login.html', error='Database connection failed')
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        check_password = request.form.get('confirm_password')
        
        if password != check_password:
            return jsonify("Passwords do not match", password, check_password)
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            
            cursor.execute(f"SELECT * FROM users WHERE email= %s", (email,))
            user = cursor.fetchone()
            if user:
                return jsonify('User with this email already exists')
            
            cursor.execute(f"SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()


            if user:
                return jsonify('User with this username already exists')
            password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            cursor.execute(f"INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
            connection.commit()
            
            return redirect(url_for('auth_bp.login'))
        else:
            return render_template('register.html', error='Database connection failed')
    return render_template('register.html')
            
            
@auth_bp.route('/logout') 
def logout():
    session.pop('user', None)
    return redirect('/')
            
            
            
            
        
        