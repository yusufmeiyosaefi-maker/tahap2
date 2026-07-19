from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from functools import wraps
from models import db, Profile, Skill, Experience, Project, Contact
import cloudinary.uploader
import json
from datetime import datetime

bp = Blueprint('admin', __name__)

# Login decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/')
@login_required
def dashboard():
    project_count = Project.query.count()
    skill_count = Skill.query.count()
    experience_count = Experience.query.count()
    contact_count = Contact.query.count()
    
    return render_template('admin/dashboard.html', 
                         project_count=project_count,
                         skill_count=skill_count,
                         experience_count=experience_count,
                         contact_count=contact_count)

@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def manage_profile():
    if request.method == 'POST':
        profile = Profile.query.first()
        if not profile:
            profile = Profile()
        
        profile.name = request.form.get('name')
        profile.title = request.form.get('title')
        profile.bio = request.form.get('bio')
        profile.email = request.form.get('email')
        profile.phone = request.form.get('phone')
        profile.location = request.form.get('location')
        profile.github_url = request.form.get('github_url')
        profile.linkedin_url = request.form.get('linkedin_url')
        profile.instagram_url = request.form.get('instagram_url')
        
        if 'profile_image' in request.files:
            file = request.files['profile_image']
            if file and file.filename:
                result = cloudinary.uploader.upload(file)
                profile.profile_image = result['secure_url']
        
        db.session.add(profile)
        db.session.commit()
        return jsonify({'success': True})
    
    profile = Profile.query.first()
    return render_template('admin/profile.html', profile=profile)

@bp.route('/skills')
@login_required
def list_skills():
    skills = Skill.query.order_by(Skill.order).all()
    return render_template('admin/skills.html', skills=skills)

@bp.route('/experiences')
@login_required
def list_experiences():
    experiences = Experience.query.order_by(Experience.order).all()
    return render_template('admin/experiences.html', experiences=experiences)

@bp.route('/projects')
@login_required
def list_projects():
    projects = Project.query.order_by(Project.order).all()
    return render_template('admin/projects.html', projects=projects)

@bp.route('/contacts')
@login_required
def list_contacts():
    contacts = Contact.query.order_by(Contact.created_at.desc()).all()
    return render_template('admin/contacts.html', contacts=contacts)