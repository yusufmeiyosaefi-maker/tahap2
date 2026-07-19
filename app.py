from flask import Flask, render_template, redirect, url_for, request, session
from config import Config
from models import db
from routes import main_routes, admin_routes, api_routes
import cloudinary
import cloudinary.uploader
import os
from functools import wraps

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize Database
    db.init_app(app)
    
    # Configure Cloudinary
    cloudinary.config(
        cloud_name=app.config['CLOUDINARY_CLOUD_NAME'],
        api_key=app.config['CLOUDINARY_API_KEY'],
        api_secret=app.config['CLOUDINARY_API_SECRET']
    )
    
    # Register Blueprints
    app.register_blueprint(main_routes.bp)
    app.register_blueprint(admin_routes.bp, url_prefix='/admin')
    app.register_blueprint(api_routes.bp, url_prefix='/api')
    
    # Login route for admin
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            
            if username == app.config['ADMIN_USERNAME'] and password == app.config['ADMIN_PASSWORD']:
                session['logged_in'] = True
                return redirect(url_for('admin.dashboard'))
            else:
                return render_template('login.html', error='Username atau password salah!')
        
        return render_template('login.html')
    
    @app.route('/logout')
    def logout():
        session.pop('logged_in', None)
        return redirect(url_for('login'))
    
    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
        print("✓ Database tables created successfully!")
    
    print(f"✓ Server running at http://localhost:5000")
    print(f"✓ Admin panel at http://localhost:5000/admin")
    print(f"✓ Login at http://localhost:5000/login")
    print(f"✓ Default admin: {app.config['ADMIN_USERNAME']} / {app.config['ADMIN_PASSWORD']}")
    
    app.run(debug=app.config['DEBUG'], host='0.0.0.0', port=5000)