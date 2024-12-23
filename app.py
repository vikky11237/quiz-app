from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from datetime import datetime
from questions import quiz_questions
from models import db, User, QuizScore, Question, Category
import os
from sqlalchemy import func
from functools import wraps
from random import sample
from contextlib import contextmanager
from sqlalchemy.exc import OperationalError

app = Flask(__name__)
# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'quiz.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key_here'
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
}

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Create database tables
with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('register'))
        
        user = User(username=username, name=name)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login.')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    # Get user's quiz history
    quiz_history = QuizScore.query.filter_by(user_id=current_user.id)\
                                 .order_by(QuizScore.date.desc())\
                                 .limit(5)\
                                 .all()
    return render_template('index.html', quiz_history=quiz_history)

# Add this context manager for database operations
@contextmanager
def safe_db_session():
    try:
        yield db.session
        db.session.commit()
    except OperationalError as e:
        db.session.rollback()
        # Wait and retry once
        import time
        time.sleep(1)
        try:
            yield db.session
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash('Error saving score. Please try again.', 'error')
            raise e
    except Exception as e:
        db.session.rollback()
        flash('Error saving score. Please try again.', 'error')
        raise e

@app.route('/quiz', methods=['GET', 'POST'])
@login_required
def quiz():
    if 'questions' not in session:
        # Get all questions from database
        all_questions = Question.query.all()
        
        if not all_questions:
            flash('No questions available.')
            return redirect(url_for('index'))
        
        # Select exactly 5 random questions from all categories
        selected_questions = sample(all_questions, 5)
        
        # Store questions in session
        session['questions'] = [
            {
                'id': q.id,
                'question': q.question_text,
                'options': [q.option_1, q.option_2, q.option_3, q.option_4],
                'correct_answer': q.correct_answer,
                'category': q.category.name
            }
            for q in selected_questions
        ]
        session['score'] = 0
        session['question_index'] = 0

    current_questions = session.get('questions', [])
    
    if request.method == 'POST':
        session['question_index'] += 1
        
        if session['question_index'] >= len(current_questions):
            # Calculate percentage score
            percentage = (session['score'] / len(current_questions)) * 100
            final_score = session['score']
            total_questions = len(current_questions)
            
            # Save quiz score with retry mechanism
            try:
                with safe_db_session() as db_session:
                    score = QuizScore(
                        score=final_score,
                        user_id=current_user.id,
                        date=datetime.now()
                    )
                    db_session.add(score)
            except Exception as e:
                app.logger.error(f"Error saving score: {str(e)}")
                # Even if save fails, show the score to user
                
            # Clear session data
            session.pop('questions', None)
            session.pop('score', None)
            session.pop('question_index', None)
            
            return render_template('index.html', 
                                 score=final_score, 
                                 total=total_questions,
                                 percentage=percentage)
    
    if session.get('question_index', 0) < len(current_questions):
        progress_percentage = (session['question_index'] / len(current_questions)) * 100
        return render_template('quiz.html',
                             question=current_questions[session['question_index']],
                             question_number=session['question_index'] + 1,
                             total_questions=len(current_questions),
                             progress_percentage=progress_percentage)

    return redirect(url_for('index'))

@app.route('/profile')
@login_required
def profile():
    # Get user's quiz history
    quiz_history = QuizScore.query.filter_by(user_id=current_user.id)\
                                 .order_by(QuizScore.date.desc())\
                                 .all()
    
    # Calculate statistics
    stats = db.session.query(
        func.count(QuizScore.id).label('total_attempts'),
        func.avg(QuizScore.score * 100.0 / len(quiz_questions)).label('average_score'),
        func.max(QuizScore.score * 100.0 / len(quiz_questions)).label('highest_score')
    ).filter_by(user_id=current_user.id).first()
    
    quiz_stats = {
        'total_attempts': stats.total_attempts or 0,
        'average_score': stats.average_score or 0,
        'highest_score': stats.highest_score or 0
    }
    
    # Prepare data for the chart
    dates = [score.date.strftime('%Y-%m-%d %H:%M') for score in reversed(quiz_history)]
    scores = [(score.score / len(quiz_questions) * 100) for score in reversed(quiz_history)]
    
    return render_template('profile.html',
                         quiz_history=quiz_history,
                         quiz_stats=quiz_stats,
                         total_questions=len(quiz_questions),
                         dates=dates,
                         scores=scores)

@app.template_filter('format_date')
def format_date(value):
    user = User.query.get(value)
    if user:
        return user.created_at.strftime('%Y-%m-%d')
    return ''

@app.route('/categories')
@login_required
def categories():
    categories = Category.query.all()
    return render_template('categories.html', categories=categories)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('You need to be an admin to access this page.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/admin/questions')
@login_required
@admin_required
def admin_questions():
    questions = Question.query.all()
    categories = Category.query.all()
    return render_template('admin/manage_questions.html', 
                         questions=questions,
                         categories=categories)

@app.route('/admin/question/add', methods=['POST'])
@login_required
@admin_required
def admin_add_question():
    try:
        question = Question(
            category_id=request.form['category_id'],
            question_text=request.form['question_text'],
            option_1=request.form['option_1'],
            option_2=request.form['option_2'],
            option_3=request.form['option_3'],
            option_4=request.form['option_4'],
            correct_answer=request.form['correct_answer']
        )
        db.session.add(question)
        db.session.commit()
        flash('Question added successfully!', 'success')
    except Exception as e:
        flash('Error adding question: ' + str(e), 'danger')
    
    return redirect(url_for('admin_questions'))

@app.route('/admin/question/<int:question_id>/delete', methods=['POST'])
@login_required
@admin_required
def admin_delete_question(question_id):
    question = Question.query.get_or_404(question_id)
    db.session.delete(question)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/check_answer', methods=['POST'])
@login_required
def check_answer():
    data = request.get_json()
    answer = data.get('answer')
    question_id = data.get('question_id')
    
    # Get current question from session
    current_question = session['questions'][session['question_index']]
    
    is_correct = answer == current_question['correct_answer']
    
    if is_correct:
        session['score'] += 1
    
    return jsonify({
        'correct': is_correct,
        'correct_answer': current_question['correct_answer']
    })

if __name__ == '__main__':
    app.run(debug=True) 