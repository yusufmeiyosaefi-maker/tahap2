from flask import Blueprint, render_template, request, jsonify
from models import db, Profile, Skill, Experience, Project, Contact
from config import Config
import cloudinary.uploader
import requests
import json

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    profile = Profile.query.first()
    skills = Skill.query.order_by(Skill.order).all()
    experiences = Experience.query.order_by(Experience.order).all()
    projects = Project.query.order_by(Project.order).all()
    
    # Group skills by category
    skill_categories = {}
    for skill in skills:
        if skill.category not in skill_categories:
            skill_categories[skill.category] = []
        skill_categories[skill.category].append(skill)
    
    return render_template('index.html', 
                         profile=profile, 
                         skill_categories=skill_categories,
                         experiences=experiences,
                         projects=projects)

@bp.route('/contact', methods=['POST'])
def contact():
    try:
        data = request.form
        name = data.get('name')
        email = data.get('email')
        subject = data.get('subject')
        message = data.get('message')
        
        # Save to database
        contact = Contact(name=name, email=email, subject=subject, message=message)
        db.session.add(contact)
        db.session.commit()
        
        # Send email via Resend
        send_email_via_resend(name, email, subject, message)
        
        return jsonify({'success': True, 'message': 'Message sent successfully!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

def send_email_via_resend(name, email, subject, message):
    api_key = Config.RESEND_API_KEY
    from_email = Config.RESEND_FROM_EMAIL
    
    html_content = f"""
    <h2>New Contact Message</h2>
    <p><strong>Name:</strong> {name}</p>
    <p><strong>Email:</strong> {email}</p>
    <p><strong>Subject:</strong> {subject}</p>
    <p><strong>Message:</strong></p>
    <p>{message}</p>
    """
    
    response = requests.post(
        'https://api.resend.com/emails',
        headers={
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        },
        json={
            'from': from_email,
            'to': ['your-email@domain.com'],  # Your admin email
            'subject': f'Portfolio Contact: {subject}',
            'html': html_content,
            'reply_to': email
        }
    )
    return response.json()