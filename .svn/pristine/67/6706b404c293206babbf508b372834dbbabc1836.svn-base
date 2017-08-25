
@app.route("/")
@login_required
def home():
    #return "Hello World!"
    g.search_form = SearchForm()
    user = app_users.query.filter_by(email = current_user.email).first()
    course = courses.query.filter_by(instructor_user_id = user.id).all()
    return render_template('index.html', current_user=current_user, course=course)

@app.route("/welcome")
def welcome():
    return render_template("welcome.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
	error = None
	login_form = LoginForm()
	reg_form = RegistrationForm()
	if request.method == 'POST':
		login_form.email.data = request.form['email']
		login_form.password.data = request.form['password']
		if login_form.validate_on_submit() != False:
			session['logged_in'] = True
			user = app_users.query.filter_by(email = login_form.email.data).first()
			login_user(user)
			flash('You were just logged in!')
			return redirect(url_for('home'))
	elif request.method == 'GET':
		return render_template('login.html', login_form=login_form, reg_form=reg_form,)
  	return render_template('login.html', error=login_form.errors, reg_form=reg_form, login_form=login_form)

@app.route("/logout")
@login_required
def logout():
	session.pop('logged_in', None)
	flash('You were just logged out!')
	return redirect(url_for('welcome'))

@app.route('/register', methods=['GET', 'POST'])
def register():
	error = None
	login_form = LoginForm()
	reg_form = RegistrationForm()
	if request.method == 'POST' and reg_form.validate_on_submit() != False:
		user = app_users(email=reg_form.email.data, pw=reg_form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('Thanks for registering')
		return redirect(url_for('login'))
	elif request.method == 'POST' and reg_form.validate_on_submit() == False:
		return render_template('login.html', login_form=login_form, reg_form=reg_form, error=reg_form.errors)
	elif request.method == 'GET':
		return render_template('login.html', reg_form=reg_form, error=error)

@app.route('/search', methods=['POST'])
# @login_required
def search():
	g.search_form = SearchForm()
	if not g.search_form.validate_on_submit():
		return redirect(url_for('index'))
	return redirect(url_for('search_results', query=g.search_form.search.data))

@app.route('/search_results/<query>')
@login_required
def search_results(query):
	_query = '*' + query + '*'
	course_results = courses.query.whoosh_search(_query, MAX_SEARCH_RESULTS).all()
	return render_template('search_results.html', query=query, cresult=course_results)


@app.route('/reset_email', methods=['GET', 'POST'])
@login_required
def reset_email():
	g.reset_email_form = ResetEmailForm()
	if request.method == 'POST' and g.reset_email_form.validate_on_submit() != False:
		user = app_users.query.filter_by(email=current_user.email).first()
		user.email = g.reset_email_form.new_email.data
		db.session.commit()
		flash("Your email address is updated")
		return redirect(url_for('home'))
	elif request.method == 'POST' and g.reset_email_form.validate_on_submit() == False:
		return render_template('user/reset_email.html', error=g.reset_email_form.errors)
	return render_template("user/reset_email.html", form=g.reset_email_form)
	
@app.route('/reset_pwd', methods=['GET', 'POST'])
@login_required
def reset_pwd():
	g.reset_pwd_form = ResetPasswordForm()
	if request.method == 'POST' and g.reset_pwd_form.validate_on_submit() != False:
		user = app_users.query.filter_by(email=current_user.email).first()
		
		user.pw = g.reset_pwd_form.new_password.data
		db.session.commit()
	
		flash("Your password is updated!")
		
		return redirect(url_for('home'))
	elif request.method == 'POST' and g.reset_pwd_form.validate_on_submit() == False:
		return render_template('user/reset_pwd.html', error=g.reset_pwd_form.errors)
	return render_template("user/reset_pwd.html", form=g.reset_pwd_form)
