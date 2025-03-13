from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(400), nullable=False)
    image_link = db.Column(db.String(400), nullable=False)
    project_link = db.Column(db.String(400), nullable=False)
    catagory = db.Column(db.String(100), nullable=False)
    catagory_show = db.Column(db.String(100), nullable=False)
class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    complete = db.Column(db.String(50), nullable=False)
    
class Certificate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    image_link = db.Column(db.String(400), nullable=False)
    credential_link = db.Column(db.String(400), nullable=False)

class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    link = db.Column(db.String(400), nullable=False)
    category = db.Column(db.String(100), nullable=False)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        form_type = request.form.get('form_type')
        
        if form_type == 'project':
            new_project = Project(
                title=request.form['title'],
                description=request.form['description'],
                image_link=request.form['image_link'],
                project_link=request.form['project_link'],
                catagory=request.form['catagory'],
                catagory_show=request.form['catagory_show']
            )
            db.session.add(new_project)
        
        elif form_type == 'certificate':
            new_certificate = Certificate(
                name=request.form['name'],
                image_link=request.form['image_link'],
                credential_link=request.form['credential_link']
            )
            db.session.add(new_certificate)
        
        elif form_type == 'resource':
            new_resource = Resource(
                name=request.form['name'],
                link=request.form['link'],
                category=request.form['category']
            )
            db.session.add(new_resource)
        elif form_type == 'skill':
            new_resource = Skill(
                title=request.form['title'],
                complete=request.form['complete'],
                
            )
            db.session.add(new_resource)
        db.session.commit()
        return redirect(url_for('admin'))
    
    projects = Project.query.all()
    certificates = Certificate.query.all()
    resources = Resource.query.all()
    skill = Skill.query.all()
    return render_template('admin.html', projects=projects, certificates=certificates, resources=resources,skill=skill)

@app.route('/delete/<table>/<int:id>', methods=['POST'])
def delete_entry(table, id):
    if table == 'project':
        entry = Project.query.get_or_404(id)
    elif table == 'certificate':
        entry = Certificate.query.get_or_404(id)
    elif table == 'resource':
        entry = Resource.query.get_or_404(id)
    elif table == 'skill':
        entry = Skill.query.get_or_404(id)
    else:
        return redirect(url_for('admin'))
    
    if entry:
        db.session.delete(entry)
        db.session.commit()
    return redirect(url_for('admin'))

@app.route('/update/<table>/<int:id>', methods=['GET', 'POST'])
def update_entry(table, id):
    if table == 'project':
        entry = Project.query.get_or_404(id)
    elif table == 'certificate':
        entry = Certificate.query.get_or_404(id)
    elif table == 'resource':
        entry = Resource.query.get_or_404(id)
    elif table == 'skill':
        entry = Skill.query.get_or_404(id)
    else:
        return redirect(url_for('admin'))
    
    if request.method == 'POST':
        for key, value in request.form.items():
            setattr(entry, key, value)
        db.session.commit()
        return redirect(url_for('admin'))
    
    return render_template('update.html', item=entry, item_type=table)


@app.route('/')
def home():
    return render_template('home.html')
@app.route('/about')
def about():
    skill = Skill.query.all()
    return render_template('about.html',skill= skill)
@app.route('/project')
def project():
    projects = Project.query.all()
    return render_template('project.html' ,proj = projects)
@app.route('/resource')
def resource():
    resources = Resource.query.all()
    return render_template('resource.html' , res = resources)
@app.route('/certificate')
def certificate():
    certificates = Certificate.query.all()
    return render_template('certificate.html', cer = certificates)

if __name__ == '__main__':
    # with app.app_context():
    #     db.create_all()
    # print("Database created successfully!")
    app.run(debug=True)