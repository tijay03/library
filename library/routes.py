from flask import render_template, url_for, flash, redirect, request, abort
from library import app, db, bcrypt
from library.forms import RegistrationForm, LoginForm, BookForm
from library.models import User, Book
from flask_login import login_user, current_user, logout_user, login_required

'''books = [
    {
        'genre': 'Fiction',
        'title': 'Sun also rises',
        'author': 'john dewy'
    },
    {
        'genre': 'Mystery',
        'title': 'Discover Haunted car',
        'author': 'mary rose'
    }
]'''

@app.route('/')
@login_required
def home():
    books = Book.query.all()
    return render_template('home.html', books=books)


@app.route('/about')
@login_required
def about():
    return render_template('about.html', title='About')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password,usertype=form.usertype.data)
        db.session.add(user)
        db.session.commit()
        flash('Your Account has been created. You are now able to login', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title="Register", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
       user = User.query.filter_by(email=form.email.data).first()
       if user and bcrypt.check_password_hash(user.password, form.password.data):
           login_user(user, remember=form.remember.data) 
           next_page = request.args.get('next')
           return redirect(next_page) if next_page else redirect(url_for('home'))
       else:
           flash('Login Unsuccessful, Please check email and password', 'danger')
        #else:
        #    flash('Login Unsuccessful, Please check email and password', 'danger')
    return render_template('login.html' ,title="Login", form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/account')
@login_required
def account():
    return render_template('account.html' ,title="Account")
    

@app.route('/book/new' , methods=['GET', 'POST'])
@login_required
def new_book():
    form = BookForm()
    if form.validate_on_submit():
        book = Book(genre=form.genre.data, title=form.title.data, author=form.author.data, user_id=current_user.username)
        db.session.add(book)
        db.session.commit()
        flash('Your book has been added', 'success')
        return redirect(url_for('home'))
    return render_template('create_book.html' ,title="New Book", form=form, legend="New Book")

@app.route('/book/<int:book_id>')
def book(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template('book.html', title=book.title, book=book)

@app.route('/book/<int:book_id>/update', methods=['GET', 'POST'])
@login_required
def update_book(book_id):
    book = Book.query.get_or_404(book_id)
    if book.user_id != current_user.username:
        #abort(403)
        flash('There is no rights to update the record', 'success')
        return redirect(url_for('home'))
    form = BookForm()
    if form.validate_on_submit():
        book.genre = form.genre.data
        book.title = form.title.data
        book.author = form.author.data
        db.session.commit()
        flash('Book updated successfully!', 'success')
        return redirect(url_for('book', book_id=book.id))
    elif request.method == 'GET':
        form.genre.data = book.genre
        form.title.data = book.title 
        form.author.data  = book.author 

    return render_template('create_book.html', title='Update Book', form=form, legend="Update Book")

app.route('/book/<int:book_id>/delete', methods=['POST'])
@login_required
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    if book.user_id != current_user.username:
        flash('Your book has been deleted', 'success')
        #abort(403)
    db.session.delete(book)
    db.session.commit()
    flash('Your book has been deleted', 'success')
    return redirect(url_for('home'))