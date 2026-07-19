from flask import Blueprint, request, jsonify
from models import db, Skill, Experience, Project, Contact
import cloudinary.uploader
import json
from datetime import datetime

bp = Blueprint('api', __name__)

# Skills API
@bp.route('/skills', methods=['GET', 'POST'])
def handle_skills():
    if request.method == 'GET':
        skills = Skill.query.order_by(Skill.order).all()
        return jsonify([{
            'id': s.id,
            'name': s.name,
            'category': s.category,
            'proficiency': s.proficiency,
            'order': s.order
        } for s in skills])
    
    elif request.method == 'POST':
        data = request.json
        skill = Skill(
            name=data['name'],
            category=data.get('category'),
            proficiency=data.get('proficiency', 0),
            order=data.get('order', 0)
        )
        db.session.add(skill)
        db.session.commit()
        return jsonify({'success': True, 'id': skill.id})

@bp.route('/skills/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handle_skill(id):
    skill = Skill.query.get_or_404(id)
    
    if request.method == 'GET':
        return jsonify({
            'id': skill.id,
            'name': skill.name,
            'category': skill.category,
            'proficiency': skill.proficiency,
            'order': skill.order
        })
    
    elif request.method == 'PUT':
        data = request.json
        skill.name = data.get('name', skill.name)
        skill.category = data.get('category', skill.category)
        skill.proficiency = data.get('proficiency', skill.proficiency)
        skill.order = data.get('order', skill.order)
        db.session.commit()
        return jsonify({'success': True})
    
    elif request.method == 'DELETE':
        db.session.delete(skill)
        db.session.commit()
        return jsonify({'success': True})

# Experiences API
@bp.route('/experiences', methods=['GET', 'POST'])
def handle_experiences():
    if request.method == 'GET':
        experiences = Experience.query.order_by(Experience.order).all()
        return jsonify([{
            'id': e.id,
            'company': e.company,
            'position': e.position,
            'location': e.location,
            'start_date': e.start_date.isoformat() if e.start_date else None,
            'end_date': e.end_date.isoformat() if e.end_date else None,
            'is_current': e.is_current,
            'description': e.description,
            'order': e.order
        } for e in experiences])
    
    elif request.method == 'POST':
        data = request.json
        experience = Experience(
            company=data['company'],
            position=data['position'],
            location=data.get('location'),
            start_date=datetime.strptime(data['start_date'], '%Y-%m-%d').date() if data.get('start_date') else None,
            end_date=datetime.strptime(data['end_date'], '%Y-%m-%d').date() if data.get('end_date') else None,
            is_current=data.get('is_current', False),
            description=data.get('description'),
            order=data.get('order', 0)
        )
        db.session.add(experience)
        db.session.commit()
        return jsonify({'success': True, 'id': experience.id})

@bp.route('/experiences/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handle_experience(id):
    experience = Experience.query.get_or_404(id)
    
    if request.method == 'GET':
        return jsonify({
            'id': experience.id,
            'company': experience.company,
            'position': experience.position,
            'location': experience.location,
            'start_date': experience.start_date.isoformat() if experience.start_date else None,
            'end_date': experience.end_date.isoformat() if experience.end_date else None,
            'is_current': experience.is_current,
            'description': experience.description,
            'order': experience.order
        })
    
    elif request.method == 'PUT':
        data = request.json
        experience.company = data.get('company', experience.company)
        experience.position = data.get('position', experience.position)
        experience.location = data.get('location', experience.location)
        experience.start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date() if data.get('start_date') else None
        experience.end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date() if data.get('end_date') else None
        experience.is_current = data.get('is_current', experience.is_current)
        experience.description = data.get('description', experience.description)
        experience.order = data.get('order', experience.order)
        db.session.commit()
        return jsonify({'success': True})
    
    elif request.method == 'DELETE':
        db.session.delete(experience)
        db.session.commit()
        return jsonify({'success': True})

# Projects API
@bp.route('/projects', methods=['GET', 'POST'])
def handle_projects():
    if request.method == 'GET':
        projects = Project.query.order_by(Project.order).all()
        return jsonify([{
            'id': p.id,
            'title': p.title,
            'description': p.description,
            'category': p.category,
            'image_url': p.image_url,
            'project_url': p.project_url,
            'github_url': p.github_url,
            'technologies': p.technologies,
            'order': p.order
        } for p in projects])
    
    elif request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        category = request.form.get('category')
        project_url = request.form.get('project_url')
        github_url = request.form.get('github_url')
        technologies = request.form.get('technologies')
        order = request.form.get('order', 0)
        
        # Handle image upload
        image_url = None
        if 'projectImage' in request.files:
            file = request.files['projectImage']
            if file.filename:
                result = cloudinary.uploader.upload(file)
                image_url = result['secure_url']
        
        project = Project(
            title=title,
            description=description,
            category=category,
            image_url=image_url,
            project_url=project_url,
            github_url=github_url,
            technologies=technologies,
            order=int(order) if order else 0
        )
        db.session.add(project)
        db.session.commit()
        return jsonify({'success': True, 'id': project.id})

@bp.route('/projects/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handle_project(id):
    project = Project.query.get_or_404(id)
    
    if request.method == 'GET':
        return jsonify({
            'id': project.id,
            'title': project.title,
            'description': project.description,
            'category': project.category,
            'image_url': project.image_url,
            'project_url': project.project_url,
            'github_url': project.github_url,
            'technologies': project.technologies,
            'order': project.order
        })
    
    elif request.method == 'PUT':
        project.title = request.form.get('title', project.title)
        project.description = request.form.get('description', project.description)
        project.category = request.form.get('category', project.category)
        project.project_url = request.form.get('project_url', project.project_url)
        project.github_url = request.form.get('github_url', project.github_url)
        project.technologies = request.form.get('technologies', project.technologies)
        project.order = int(request.form.get('order', project.order))
        
        # Handle image upload
        if 'projectImage' in request.files:
            file = request.files['projectImage']
            if file.filename:
                result = cloudinary.uploader.upload(file)
                project.image_url = result['secure_url']
        
        db.session.commit()
        return jsonify({'success': True})
    
    elif request.method == 'DELETE':
        db.session.delete(project)
        db.session.commit()
        return jsonify({'success': True})

# Contacts API
@bp.route('/contacts', methods=['GET'])
def get_contacts():
    contacts = Contact.query.order_by(Contact.created_at.desc()).all()
    return jsonify([{
        'id': c.id,
        'name': c.name,
        'email': c.email,
        'subject': c.subject,
        'message': c.message,
        'is_read': c.is_read,
        'created_at': c.created_at.isoformat()
    } for c in contacts])

@bp.route('/contacts/<int:id>', methods=['GET'])
def get_contact(id):
    contact = Contact.query.get_or_404(id)
    return jsonify({
        'id': contact.id,
        'name': contact.name,
        'email': contact.email,
        'subject': contact.subject,
        'message': contact.message,
        'is_read': contact.is_read,
        'created_at': contact.created_at.isoformat()
    })

@bp.route('/contacts/<int:id>/read', methods=['PUT'])
def mark_contact_read(id):
    contact = Contact.query.get_or_404(id)
    contact.is_read = True
    db.session.commit()
    return jsonify({'success': True})

@bp.route('/contacts/<int:id>', methods=['DELETE'])
def delete_contact(id):
    contact = Contact.query.get_or_404(id)
    db.session.delete(contact)
    db.session.commit()
    return jsonify({'success': True})