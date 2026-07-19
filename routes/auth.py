from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from models import db, Admin, LoginHistory
from datetime import datetime
import re

auth_bp = Blueprint('auth', __name__, template_folder='../templates/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember') == 'on'
        
        # Get client info
        ip_address = request.remote_addr
        user_agent = request.headers.get('User-Agent', 'Unknown')
        
        admin = Admin.query.filter_by(username=username).first()
        
        if admin and admin.check_password(password):
            login_user(admin, remember=remember)
            admin.last_login = datetime.utcnow()
            
            # Log successful login
            login_history = LoginHistory(
                admin_id=admin.id,
                ip_address=ip_address,
                user_agent=user_agent,
                success=True
            )
            db.session.add(login_history)
            db.session.commit()
            
            flash('Login berhasil! Selamat datang, {}'.format(admin.username), 'success')
            
            # Redirect to admin dashboard or page user wanted to access
            next_page = request.args.get('next')
            if next_page and next_page.startswith('/admin'):
                return redirect(next_page)
            return redirect(url_for('admin.dashboard'))
        else:
            # Log failed login attempt
            login_history = LoginHistory(
                admin_id=admin.id if admin else None,
                ip_address=ip_address,
                user_agent=user_agent,
                success=False
            )
            db.session.add(login_history)
            db.session.commit()
            
            flash('Username atau password salah!', 'danger')
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Anda telah logout.', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        # Validate current password
        if not current_user.check_password(current_password):
            flash('Password saat ini salah!', 'danger')
            return render_template('auth/change_password.html')
        
        # Validate new password
        if len(new_password) < 6:
            flash('Password baru minimal 6 karakter!', 'danger')
            return render_template('auth/change_password.html')
        
        if new_password != confirm_password:
            flash('Konfirmasi password tidak cocok!', 'danger')
            return render_template('auth/change_password.html')
        
        # Update password
        current_user.set_password(new_password)
        db.session.commit()
        
        flash('Password berhasil diubah!', 'success')
        return redirect(url_for('admin.dashboard'))
    
    return render_template('auth/change_password.html')

@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        # Simple implementation - in production, use email verification
        flash('Fitur reset password akan segera hadir. Silakan hubungi administrator.', 'info')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/forgot_password.html')
