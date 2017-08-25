import os
from flask import Flask, abort, render_template, redirect, url_for, request, \
    session, flash, g
from flask_login import login_user, logout_user, current_user, \
    login_required
from functools import wraps
from app import app, db, lm
from flask_wtf import Form
from forms import *
from models import *
from config import MAX_SEARCH_RESULTS
from itertools import permutations
from werkzeug import secure_filename
from  sqlalchemy.sql.expression import func
from sqlalchemy import desc
import datetime
import re
import random
import string
from sqlalchemy import asc
from sqlalchemy import and_
from sqlalchemy import or_

GOOGLE_API_KEY = ''
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


@lm.user_loader
def load_user(id):
    return app_users.query.get(int(id))


@app.before_request
def load_user():
    g.user = current_user


# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            kwargs["logged_in"] = True
            return f(*args, **kwargs)
        else:
            kwargs["logged_in"] = False
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap


@app.route("/home")
def home():
    g.search_form = SearchForm()
    space_data = spaces.query.order_by(func.random()).limit(3)

    spaces_recomend = []
    for result in space_data:
        p_url = space_photos.query.filter_by(space_id=result.space_id).first()
        d = {'space_url': "/spaces/" + str(result.space_id) + "/description",
            'space_name': result.space_name,
            'description': result.description,
            'photo_url': p_url.photo_url}
        spaces_recomend.append(d)
    return render_template('index.html', home=True, current_user=current_user, spaces_recomend=spaces_recomend)


@app.route("/")
def landing():
    space_data = spaces.query.order_by(func.random()).limit(3)
    spaces_recomend = []
    for result in space_data:
        p_url = space_photos.query.filter_by(space_id=result.space_id).first()
        d = {'space_url': "/spaces/" + str(result.space_id) + "/description",
            'space_name': result.space_name,
            'description': result.description,
            'photo_url': p_url.photo_url}
        spaces_recomend.append(d)
    return render_template("index.html", home=True, current_user=current_user, spaces_recomend=spaces_recomend)


@app.route("/login", methods=['GET', 'POST'])
def login():
    error = None
    login_form = LoginForm()
    if request.method == 'POST':
        login_form.email.data = request.form['email']
        login_form.password.data = request.form['password']
        if login_form.validate_on_submit() != False:
            session['logged_in'] = True
            user = app_users.query.filter_by(
                email=login_form.email.data).first()
            login_user(user)
            flash('You were just logged in!')
            return redirect(url_for('home'))

    elif request.method == 'GET':
        return render_template(
            'login.html', login_form=login_form)

    return render_template(
        'login.html', error=login_form.errors, login_form=login_form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    reg_form = RegistrationForm()
    if request.method == 'POST' and reg_form.validate_on_submit() != False:
        user = app_users(
            email=reg_form.email.data,
            password=reg_form.password.data,
            sur_name=reg_form.lname.data,
            first_name=reg_form.fname.data)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering')
        return redirect(url_for('login'))

    elif request.method == 'POST' and reg_form.validate_on_submit() == False:
        return render_template(
            'register.html', reg_form=reg_form, error=reg_form.errors)

    elif request.method == 'GET':
        return render_template('register.html', reg_form=reg_form, error=error)


@app.route("/u/<int:query>", methods=["GET", "POST"])
@login_required
def user_search(query, **kwargs):
    write_oreview = ""
    write_treview = ""
    active_tab = "owner"
    reviewer_id = current_user.user_id
    editable = ""
    if (current_user.user_id == query):
        editable = "t"
    if request.method == "POST":
        oreview = request.form.get('oreview', '')
        treview = request.form.get('treview', '')
        rating = 0
        if oreview:
            rating = request.form.get('orating', '')
            review = owner_ratings(query, reviewer_id, oreview, rating)
        if treview:
            rating = request.form.get('trating', '')
            review = tenant_ratings(query, reviewer_id, treview, rating)
        if int(rating) > 0:
            if treview or request.form.get('trating', ''):
                active_tab = "tenant"
            db.session.add(review)
            db.session.commit()
        else:
            if oreview:
                write_oreview = "Error: Must enter a rating"
            if treview:
                write_treview = "Error: Must enter a rating"
                active_tab = "tenant"

    temp_user = app_users.query.filter(app_users.user_id == query).first()

    if not temp_user:
        return render_template('object_not_found.html', type='user',
                               title='User Not Found',
                               logged_in=kwargs.get('logged_in', False))

    owner_reviews = owner_ratings.query.filter(
        owner_ratings.owner_id == query).all()
    tenant_reviews = tenant_ratings.query.filter(
        tenant_ratings.tenant_id == query).all()
    output_vars = {
        'first_name': temp_user.first_name,
        'sur_name': temp_user.sur_name,
        'blurb': temp_user.blurb,
        'title': temp_user.first_name + " " + temp_user.sur_name
    }
    o_reviews = []
    t_reviews = []
    o_reviewable = "t" if spaces.query.filter(
        spaces.owner_id==temp_user.user_id).first() else ""
    t_reviewable = "t"

    if o_reviewable:
        for review in owner_reviews:
            temp_reviewer = app_users.query.filter(
                app_users.user_id == review.reviewer_id).first()
            name = temp_reviewer.first_name + " " + temp_reviewer.sur_name
            temp_entry = {
                'reviewer': name,
                'userlink': str(review.reviewer_id),
                'score': review.rating,
                'comment': review.comment,
                'datetime': str(review.date)[:str(review.date).index(":") + 3]
            }
            o_reviews.append(temp_entry)

            if (review.reviewer_id == int(reviewer_id)):
                o_reviewable = ""

    for review in tenant_reviews:
        temp_reviewer = app_users.query.filter(
            app_users.user_id == review.reviewer_id).first()
        name = temp_reviewer.first_name + " " + temp_reviewer.sur_name
        temp_entry = {
            'reviewer': name,
            'userlink': str(review.reviewer_id),
            'score': review.rating,
            'comment': review.comment,
            'datetime': str(review.date)[:str(review.date).index(":") + 3]
        }
        t_reviews.append(temp_entry)

        if (review.reviewer_id == int(reviewer_id)):
            t_reviewable = ""

    output_vars['owner_reviews'] = sorted(
        o_reviews,
        key=lambda entry: entry['datetime'])

    output_vars['tenant_reviews'] = sorted(
        t_reviews,
        key=lambda entry: entry['datetime'])

    if query != current_user.user_id:
        output_vars['reviewable'] = 'true'

    output_vars['write_oreview'] = write_oreview
    output_vars['write_treview'] = write_treview
    output_vars['active_tab'] = active_tab
    output_vars['o_reviewable'] = o_reviewable
    output_vars['t_reviewable'] = t_reviewable
    output_vars['editable'] = editable
    return render_template('user.html', **output_vars)


@app.route("/user")
@login_required
def user(**kwargs):
    return user_search(current_user.user_id, **kwargs)

@app.route("/user/edit", methods=["GET", "POST"])
@login_required
def edit_user(**kwargs):
    error=None
    user = app_users.query.filter_by(user_id=current_user.user_id).first()
    edit_form = EditForm()
    edit_form.validate_on_submit()
    success=""
    if (request.method == "POST"):
        if (edit_form.email.data and edit_form.fname.data and
            edit_form.lname.data):
            user.email = edit_form.email.data
            user.first_name = edit_form.fname.data
            user.sur_name = edit_form.lname.data
            user.blurb = edit_form.blurb.data
            db.session.commit()
            success="Successfully updated!"
    if (user):
        edit_form.email.data = user.email
        edit_form.fname.data = user.first_name
        edit_form.lname.data = user.sur_name
        edit_form.blurb.data = user.blurb

        return render_template('edit.html', user=user, edit_form=edit_form, error=error, success=success)
    else:
        return render_template(
            'object_not_found.html', type='Edit User', title='Page Not Found',
            **output_vars)

@app.route("/search")
def search(**kwargs):
    output_vars = {
        "search_type": "Space",
        "search_term": "jam",
        "results": [
            {
                'name': 'Space Jam',
                'info': '123 Fake Street<br/>At your place<br/>Toronto<br/>Canada'
            },
            {
                'name': 'Space Land',
                'info': '124 Fake Street<br/>At your place<br/>Toronto<br/>Canada'
            }
        ]
    }
    return render_template('search.html', **output_vars)


@app.route("/search_users", methods=["GET", "POST"])
@login_required
def search_users(**kwargs):
    output_vars = kwargs
    output_vars["search_type"] = "users"
    output_vars["error"] = ""

    if request.method == "POST":
        query = request.form.get('query', '').split(" ")
        query = map(lambda a: a.capitalize(), query)

        if (len(query) > 1):
            temp_results = set()
            [temp_results.update(set(app_users.query.filter(
                app_users.first_name == temp_query[0]).filter(
                app_users.sur_name == temp_query[1]).all()))
                for temp_query in permutations(query, 2)]
        else:
            temp_results = app_users.query.filter(
                app_users.sur_name == query[0]).all()

        output_vars = {
            "search_type": "User",
            "results": [
                {
                    'user_id': "u/" + str(user.user_id),
                    'name': user.first_name + " " + user.sur_name,
                    'info': user.blurb + "<br/>"
                } for user in sorted(temp_results, key=lambda user: (
                    user.sur_name, user.first_name))
            ]
        }

        if (len(temp_results) == 0):
            output_vars["error"] = "User does not exist"

    return render_template('search_users.html', **output_vars)


@app.route("/logout")
@login_required
def logout(**kwargs):
    logout_user()
    session.pop('logged_in', None)
    flash('You were just logged out!')
    return redirect(url_for('home'))

# check that filename is of appropriate image type
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/space/add', methods=["GET", "POST"])
@login_required
def space_add(**kwargs):
    output_vars = kwargs

    if request.method == "POST":
        errors = []
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        address = request.form.get('address', '').strip()
        city = request.form.get('city', '').strip()
        province = request.form.get('province', '').strip()
        country = request.form.get('country', '').strip()
        price = request.form.get('price', '').strip()
        units = request.form.get('units', '').strip()
        lat = request.form.get('lat', '').strip()
        lon = request.form.get('lon', '').strip()
        tags = request.form.get('tags', '').strip()

        
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = (
                ''.join(
                    random.SystemRandom().choice(
                        string.ascii_uppercase + string.digits) for _ in range(25))) + os.path.splitext(
                file.filename)[1]
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            errors.append("The field 'Photo' was not submitted.")

        if not name:
            errors.append("The field 'name' was not submitted.")
        if not description:
            errors.append("The field 'description' was not submitted.")
        if not address:
            errors.append("The field 'address' was not submitted.")
        if not city:
            errors.append("The field 'city' was not submitted.")
        if not country:
            errors.append("The field 'country' was not submitted.")
        if not price:
            errors.append("The field 'price' was not submitted.")
        if not units:
            errors.append("The field 'units' was not submitted.")
        if not lat or not lon:
            errors.append("The location was not pinned on the map.")

        if errors:
            return render_template(
                'add_space.html', GOOGLE_API_KEY=GOOGLE_API_KEY, errors=errors,
                **output_vars)

        try:
            units = int(units)
            if units < 1:
                errors.append("The number of units not filled properly.")
        except:
            errors.append("The number of units not filled properly.")

        try:
            price = float(price)
            if price < 0:
                errors.append("The price was not filled properly.")
        except:
            errors.append("The price was not filled properly.")

        try:
            lat = float(lat)
            lon = float(lon)
            if lat > 90 or lat < -90 or lon > 180 or lon < -180:
                errors.append(
                    "The location was not pinned correctly on the map.")
        except:
            errors.append("The location was not pinned correctly on the map.")

        if errors:
            return render_template(
                'add_space.html', GOOGLE_API_KEY=GOOGLE_API_KEY, errors=errors,
                **output_vars)
        else:
            try:
                s = spaces(owner_id=current_user.user_id,
                           space_name=name,
                           description=description,
                           street=address,
                           province=province,
                           city=city,
                           country=country,
                           max_capacity=units,
                           latitude=lat,
                           longitude=lon,
                           price_monthly=price,
                           price_yearly=(price * 12),
                           tags=tags)
                db.session.add(s)
                db.session.commit()

                s.space_tens.append(current_user)
                db.session.commit()

                photo = space_photos(s.space_id, filename, "static/photos/uploads/" + filename)
                db.session.add(photo)
                db.session.commit()

                return render_template(
                    'created.html', title="Created Space", type="space",
                    **output_vars)
            except:
                return render_template('add_space.html',
                    GOOGLE_API_KEY=GOOGLE_API_KEY, errors=["An error occurred "
                    "during the creation of your space."], **output_vars)

    return render_template(
        'add_space.html', GOOGLE_API_KEY=GOOGLE_API_KEY, **output_vars)


@app.route("/search_spaces", methods=["GET", "POST"])
@login_required
def search_spaces(**kwargs):
    output_vars = {"search_type": "Spaces"}
    output_vars["spaces"] = spaces.query.all()
    return render_template("search_spaces.html", **output_vars)


@app.route("/spaces/explore")
def explore_spaces(**kwargs):
    order_table_name="Order By"
    owner_filer="Created By"
    start_at_index=0

    #   filter by current user
    show_my_spaces = request.args.get('owner_spaces')
    if current_user.is_authenticated() and show_my_spaces and show_my_spaces.lower() == "true":
        owner_filer="Created By Me"
        space_query = spaces.query.filter_by(owner_id=current_user.user_id)
    elif show_my_spaces:
        owner_filer="Created By Anyone"
        space_query = spaces.query
    else:
        space_query = spaces.query

    #   filter by assending of descending order
    order = request.args.get('order')
    if order and order.lower() == 'desc':
        descn = True
    else:
        descn = False

    #   filter by title or date
    order_type = request.args.get('order_type')
    if order_type and order_type.lower() == "name":
        if descn:
            order_table_name="Name (Z-A)"
            space_query = space_query.order_by(desc(spaces.space_name))
        else:
            order_table_name="Name (A-Z)"
            space_query = space_query.order_by(spaces.space_name)
    else:
        if descn:
            order_table_name="Date (Older-Newer)"
            space_query = space_query.order_by(desc(spaces.creation_date))
        else:
            order_table_name="Date (Newer-Older)"
            space_query = space_query.order_by(spaces.creation_date)

    tag = request.args.get('tags')
    if tag:
        print "Tag!!! " + str(tag)
        space_query = space_query.filter(spaces.tags.contains(str(tag)))
    page = request.args.get('page')
    if page and int(page):
        start_at_index = 10 * int(page)

    space_query = space_query.offset(start_at_index).limit(10);

    #   check for empty list
    if not space_query.all():
        return render_template("explore-spaces.html", no_spaces=True,
                                order_table_name=order_table_name,
                                owner_filer=owner_filer)

    spaces_list = []
    for space in space_query.all():
        p_url = space_photos.query.filter_by(space_id=space.space_id).first()
        tags_list =[]
        for tag in space.tags.split():
            tags_list.append(tag);
        s = {'space_id': space.space_id,
            'owner_id': space.owner_id,
            'space_name': space.space_name,
            'description': space.description[0:300] + " ...",
            'street': space.street,
            'province': space.province,
            'city': space.city,
            'country': space.country,
            'max_capacity': space.max_capacity,
            'latitude': space.latitude,
            'longitude': space.longitude,
            'price_monthly': space.price_monthly,
            'price_yearly': space.price_yearly,
            'creation_date': space.creation_date.strftime("%Y-%m-%d"),
            'photo': p_url.photo_url,
            'interests':tags_list}
        spaces_list.append(s)

    return render_template("explore-spaces.html", order_table_name=order_table_name,
                            owner_filer=owner_filer, spaces_list=spaces_list)


@app.route('/spaces/<int:spaceId>/description')
def view_space(spaceId, **kwargs):
    space_query = spaces.query.get(spaceId)

    if not space_query:
        return render_template('404page.html')

    rating_query = space_ratings.query.filter_by(space_id=spaceId).filter(space_ratings.rating != None).all()
    average_stars = 0
    for rt in rating_query:
        average_stars = average_stars + rt.rating
    if len(rating_query) != 0:
        average_stars = average_stars / len(rating_query)
    else:
        average_stars = None
    ratings_number = len(rating_query)

    photo_query = space_photos.query.filter_by(space_id=spaceId).first()
    space = {'space_id': space_query.space_id,
            'owner_id': space_query.owner_id,
            'space_name': space_query.space_name,
            'description': space_query.description,
            'street': space_query.street,
            'province': space_query.province,
            'city': space_query.city,
            'country': space_query.country,
            'max_capacity': space_query.max_capacity,
            'latitude': space_query.latitude,
            'longitude': space_query.longitude,
            'price_monthly': space_query.price_monthly,
            'price_yearly': space_query.price_yearly,
            'creation_date': space_query.creation_date.strftime("%Y-%m-%d"),
            'photo_name': photo_query.photo_url,
            'tags': space_query.tags,
            'average_stars':average_stars,
            'ratings_number':ratings_number}

    


    comments = []
    comments_query = space_ratings.query.filter_by(space_id=spaceId).filter(space_ratings.comment != None).order_by(desc(space_ratings.date)).all()
    for comment in comments_query:
        rating = None
        stars = space_ratings.query.filter_by(space_id=spaceId, reviewer_id=comment.reviewer_id).filter(space_ratings.rating != None).order_by(space_ratings.date).first()
        if stars:
            rating = stars.rating
        name = app_users.query.get(comment.reviewer_id).first_name
        c = {'space_rating_id':comment.space_rating_id,
            'user_id':comment.reviewer_id,
            'date':comment.date.strftime("%Y-%m-%d"),
            'comment':comment.comment,
            'rating': rating,
            'name':name}
        comments.append(c)

    rating=0
    if current_user.is_authenticated():
        # get star rating if there is any by this user
        existing_rating = space_ratings.query.filter_by(space_id=spaceId, reviewer_id=current_user.user_id).filter(space_ratings.rating != None).first()
        if existing_rating:
            rating=int(existing_rating.rating)

        # case of owner of space
        if current_user.user_id == space_query.owner_id:
            return render_template(
                'space-description.html', GOOGLE_API_KEY=GOOGLE_API_KEY, 
                space=space, space_owner=True, comments=comments)

        

        # check if user applied
        if space_applications.query.filter_by(space_id=spaceId, user_applied_id=current_user.user_id).first():
            return render_template(
                'space-description.html', GOOGLE_API_KEY=GOOGLE_API_KEY, 
                space=space, applied_pending=True, comments=comments, rating=rating)

        # check if user is not already part of this space
        if current_user not in space_query.space_tens:
            return render_template(
                'space-description.html', GOOGLE_API_KEY=GOOGLE_API_KEY, 
                space=space, not_applied=True, comments=comments, rating=rating)

    return render_template(
        'space-description.html', GOOGLE_API_KEY=GOOGLE_API_KEY, space=space, 
        comments=comments, rating=rating)

@app.route('/spaces/<int:spaceId>/apply')
@login_required
def apply_to_space(spaceId, **kwargs):
    space_query = spaces.query.get(spaceId)

    if not space_query:
        return render_template('404page.html')

    if current_user not in space_query.space_tens and \
    not space_applications.query.filter_by(space_id=spaceId, user_applied_id=current_user.user_id).first():  
        db.session.add(space_applications(space_query.space_id, current_user.user_id, space_query.owner_id))
        db.session.commit()
        return redirect(url_for('view_space', spaceId=spaceId))
    else:
        return render_template('404page.html') 

@app.route('/spaces/<int:spaceId>/remove-apply')
@login_required
def unapply_to_space(spaceId, **kwargs):
    space_query = spaces.query.get(spaceId)

    if not space_query:
        return render_template('404page.html')

    application =space_applications.query.filter_by(space_id=spaceId, user_applied_id=current_user.user_id).first()

    if application:
        db.session.delete(application)
        db.session.commit()

    return redirect(url_for('view_space', spaceId=spaceId))

@app.route('/spaces/<int:spaceId>/add-comment', methods=["POST"])
@login_required
def add_coment_to_space(spaceId, **kwargs):
    space_query = spaces.query.get(spaceId)
    comment = request.form.get('comment').strip()

    if not space_query or not comment:
        return render_template('404page.html')

    db.session.add(space_ratings(space_id=spaceId,reviewer_id=current_user.user_id,comment=comment,rating=None))
    db.session.commit()

    return redirect(url_for('view_space', spaceId=spaceId))

@app.route('/spaces/<int:spaceId>/delete')
@login_required
def delete_space(spaceId, **kwargs):
    space_query = spaces.query.get(spaceId)

    if not space_query:
        return render_template('404page.html')

    if space_query.owner_id == current_user.user_id:
        
        for photo in space_photos.query.filter_by(space_id=spaceId).all():
            db.session.delete(photo)
        db.session.commit()

        for message in messages.query.filter(messages.to_user_id==spaceId).all():
            db.session.delete(message)
        db.session.commit()

        for interest in space_interests.query.filter_by(space_id=spaceId).all():
            db.session.delete(interest)
        db.session.commit()

        for rating in space_ratings.query.filter_by(space_id=spaceId).all():
            db.session.delete(rating)
        db.session.commit()

        for application in space_applications.query.filter_by(space_id=spaceId).all():
            db.session.delete(application)
        db.session.commit()

        db.session.delete(space_query)
        db.session.commit()
        return redirect(url_for('explore_spaces'))

@app.route('/spaces/<int:spaceId>/rate')
@login_required
def rate_space(spaceId, **kwargs):
    space_query = spaces.query.get(spaceId)
    stars = request.args.get('stars')

    if not space_query or not stars:
        abort(400)

    for old_rating in space_ratings.query.filter_by(space_id=spaceId, reviewer_id=current_user.user_id).filter(space_ratings.rating != None).all():
        db.session.delete(old_rating)
    db.session.commit()

    db.session.add(space_ratings(space_id=spaceId,reviewer_id=current_user.user_id,comment=None,rating=int(stars)))
    db.session.commit()

    return "OK"

@app.route('/requests')
@login_required
def sapce_requests(**kwargs):
    application_query = space_applications.query.filter_by(owner_id=current_user.user_id).all()

    application_list = []
    if application_query:
        for application in application_query:
            p_url = space_photos.query.filter_by(space_id=application.space_id).first()
            name_user = app_users.query.get(application.user_applied_id).first_name
            name_space = spaces.query.get(application.space_id).space_name
            a = {'space_id':application.space_id,
                'user_applied_id':application.user_applied_id,
                'name_user':name_user,
                'application_id':application.application_id,
                'name_space':name_space,
                'photo_url': p_url.photo_url}
            application_list.append(a)

    if application_list:
        return render_template('view-messages.html', applications=application_list)

    return render_template('view-messages.html')

@app.route('/requests/<int:applicationId>/accept')
@login_required
def accept_request(applicationId, **kwargs):
    application_query = space_applications.query.get(applicationId)
    if not application_query or int(application_query.owner_id) != int(current_user.user_id):
        return render_template('404page.html')

    user_to_add = app_users.query.get(application_query.user_applied_id)
    space = spaces.query.get(application_query.space_id)
    space.space_tens.append(user_to_add)
    db.session.commit()
    db.session.delete(application_query)
    db.session.commit()
    return redirect(url_for('sapce_requests'))

@app.route('/requests/<int:applicationId>/reject')
@login_required
def reject_request(**kwargs):
    application_query = space_applications.query.get(applicationId)

    if not application_query or application_query.owner_id != current_user.user_id:
        return render_template('404page.html')

    db.session.delete(application_query)
    db.session.commit()
    return redirect(url_for('sapce_requests'))

@app.route("/message/<int:group_id>", methods=["GET", "POST"])
@login_required
def pick_message(group_id, **kwargs):
    if request.method=="POST":
        print group_id
        if request.form['message_id']:
            temp_message = request.form['message_id']
            temp_mess = messages(current_user.user_id, int(group_id), temp_message)
            db.session.add(temp_mess)
            db.session.commit()
    all_users = app_users.query.all()
    all_spaces = spaces.query.all()
    user_ids = [user.user_id for user in all_users]
    empty_spaces = 0
    groups = set()
    
    for space in all_spaces:
        if space.space_tens:
            for user in space.space_tens:
                if user.user_id == current_user.user_id:
                    groups.add(space.space_id)
                    break

    out_messages = []
    default_messages = []
    default_id = group_id
    names = {}
    for group in groups:
        temp_space = spaces.query.filter(spaces.space_id==group).first()
        space_messages = messages.query.filter(messages.to_user_id==group).order_by(messages.date).all()
        for m in space_messages:
            if m.from_user_id not in names.keys():
                temp_user = app_users.query.filter(app_users.user_id==m.from_user_id).first()
                names[m.from_user_id] = temp_user.first_name + " " + temp_user.sur_name
            m.name = names[m.from_user_id]
            m.date = str(m.date)[0:16]
        group_message = {'name': temp_space.space_name,
            'messages': space_messages,
            'group_id': group
        }
        if group == group_id:
            default_messages = space_messages
        out_messages.append(group_message)
    
    return render_template('message.html', out_messages=out_messages, default_messages=default_messages, default_id=default_id)

@app.route("/message", methods=["GET", "POST"])
@login_required
def social(**kwargs):
    all_spaces = spaces.query.all()
    
    for space in all_spaces:
        if space.space_tens:
            for user in space.space_tens:
                if user.user_id == current_user.user_id:
                    return pick_message(space.space_id, **kwargs)

   
    return render_template('message.html', out_messages=[])

@app.route('/admin')
@login_required
def admin(**kwargs):
    temp_user = app_users.query.filter(app_users.user_id==current_user.user_id).first()
    output = {}
    if temp_user and temp_user.admin:
        all_users = app_users.query.all()
        all_spaces = spaces.query.all()
        user_ids = [user.user_id for user in all_users]
        empty_spaces = 0
        tenants = set()
        for space in all_spaces:
            if (not space.space_tens):
                empty_spaces += 1
            for user_id in user_ids:
                if space.space_tens:
                    for user in space.space_tens:
                        if user.user_id == user_id:
                            tenants.add(user_id)
                
        output['non_tenants'] = len(all_users)-len(tenants)
        output['tenants'] = len(tenants)
        output['empty_spaces'] = empty_spaces
        output['rented_spaces'] = len(all_spaces)-empty_spaces
        output['num_spaces'] = len(all_spaces)
        output['num_users'] = len(all_users)
        return render_template('admin.html', current_user=current_user, **output)
    return render_template(
            'object_not_found.html', type='page', title='Page Not Found',
             current_user=current_user)



