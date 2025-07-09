from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user, current_user
from . import db
from .models import User, Question, Answer, Comment, Tag, Vote
from .forms import RegistrationForm, LoginForm, QuestionForm, AnswerForm, CommentForm

main_bp = Blueprint('main', __name__)
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful. Please log in.')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('main.index'))
        else:
            flash('Invalid credentials')
    return render_template('login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@main_bp.route('/')
def index():
    questions = Question.query.order_by(Question.timestamp.desc()).all()
    return render_template('index.html', questions=questions)

@main_bp.route('/ask', methods=['GET', 'POST'])
@login_required
def ask_question():
    form = QuestionForm()
    if form.validate_on_submit():
        question = Question(title=form.title.data, body=form.body.data, author=current_user)
        if form.tags.data:
            for name in [t.strip() for t in form.tags.data.split(',') if t.strip()]:
                tag = Tag.query.filter_by(name=name).first()
                if not tag:
                    tag = Tag(name=name)
                    db.session.add(tag)
                question.tags.append(tag)
        db.session.add(question)
        db.session.commit()
        flash('Question posted')
        return redirect(url_for('main.index'))
    return render_template('ask.html', form=form)

@main_bp.route('/question/<int:question_id>', methods=['GET', 'POST'])
def question_detail(question_id):
    question = Question.query.get_or_404(question_id)
    form = AnswerForm()
    if form.validate_on_submit() and current_user.is_authenticated:
        answer = Answer(body=form.body.data, question=question, author=current_user)
        db.session.add(answer)
        db.session.commit()
        flash('Answer posted')
        return redirect(url_for('main.question_detail', question_id=question_id))
    return render_template('question.html', question=question, form=form)

@main_bp.route('/answer/<int:answer_id>/comment', methods=['POST'])
@login_required
def comment_answer(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data, answer=answer, author=current_user)
        db.session.add(comment)
        db.session.commit()
    return redirect(url_for('main.question_detail', question_id=answer.question_id))

@main_bp.route('/search')
def search():
    q = request.args.get('q', '')
    tag_name = request.args.get('tag', '')
    results = Question.query
    if q:
        results = results.filter(Question.title.contains(q) | Question.body.contains(q))
    if tag_name:
        results = results.join(Question.tags).filter(Tag.name == tag_name)
    results = results.all()
    return render_template('search.html', questions=results, query=q, tag=tag_name)

@main_bp.route('/like/<int:answer_id>', methods=['POST'])
@login_required
def like_answer(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    if not any(v.user_id == current_user.id for v in answer.votes):
        vote = Vote(user_id=current_user.id, answer_id=answer.id)
        db.session.add(vote)
        answer.question.author.points += 1
        db.session.commit()
    return redirect(url_for('main.question_detail', question_id=answer.question_id))
