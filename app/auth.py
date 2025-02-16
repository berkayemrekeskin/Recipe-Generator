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
                if bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):
                    session['user'] = user
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
        check_password = request.form.get('check_password')
        
        if password != check_password:
            return render_template('register.html', error='Passwords do not match')
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM users WHERE email='{email}'")
            user = cursor.fetchone()
            if user:
                return render_template('register.html', error='Email already registered')
            cursor.execute(f"SELECET * FROM users WHERE username='{username}'")
            user = cursor.fetchone()
            if user:
                return render_template('register.html', error='Username already taken')
            password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            cursor.execute(f"INSERT INTO users (username, email, password) VALUES ('{username}', '{email}', '{password}')")
            connection.commit()
            
            return redirect(url_for('auth_bp.login'))
        else:
            return render_template('register.html', error='Database connection failed')
    return render_template('register.html')
            
            
@auth_bp.route('/logout') 
def logout():
    return redirect(url_for('auth_bp.login'))
            
            
            
            
        
        