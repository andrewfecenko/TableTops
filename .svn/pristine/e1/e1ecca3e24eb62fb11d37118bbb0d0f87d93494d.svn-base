from app import db, bcrypt
from app import app
import datetime
from sqlalchemy import UniqueConstraint
from sqlalchemy import CheckConstraint
from sqlalchemy import Enum
from sqlalchemy import exc
import sys
if sys.version_info >= (3, 0):
	enable_search = False
else:
	enable_search = True
	import flask.ext.whooshalchemy as whooshalchemy

space_tens = db.Table('space_tenants',
	db.Column('space_id', db.Integer,db.ForeignKey('spaces.space_id')),
	db.Column('user_id', db.Integer,db.ForeignKey('app_users.user_id'))
)

class app_users(db.Model):
	"""docstring for app_users"""
	__table_args__ = {'extend_existing': True}
	__tablename__ = 'app_users'
	__searchable__ = ['first_name', 'sur_name']

	user_id=db.Column(db.Integer, primary_key=True,nullable=False)
	sur_name=db.Column(db.String(50),nullable=False)
	first_name=db.Column(db.String(50),nullable=False)
	email=db.Column(db.String(50),nullable=False)
	blurb=db.Column(db.Text,nullable=True)
	activated=db.Column(db.Boolean)
	password=db.Column(db.String(1000),nullable=False)
	admin=db.Column(db.Boolean)
	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False
		
	def get_id(self):
		return unicode(self.user_id)

	def __init__(self, password, email, sur_name, first_name, blurb="", admin=False):
		self.password=bcrypt.generate_password_hash(password)
		self.email=email
		self.sur_name=sur_name.capitalize()
		self.first_name=first_name.capitalize()
		self.blurb=blurb
		self.admin=admin

if enable_search:
	whooshalchemy.whoosh_index(app, app_users)

class spaces(db.Model):
	__tablename__ = 'spaces'

	"""docstring for spaces"""
	space_id=db.Column(db.Integer,primary_key=True,nullable=False)
	owner_id=db.Column(db.Integer,db.ForeignKey('app_users.user_id'))
	space_name=db.Column(db.String(50),nullable=False)
	description=db.Column(db.Text,nullable=False)
	street=db.Column(db.String(70),nullable=False)
	province=db.Column(db.String(70),nullable=False)
	city=db.Column(db.String(50),nullable=False)
	country=db.Column(db.String(50),nullable=False)
	max_capacity=db.Column(db.Integer,CheckConstraint('max_capacity >= 1'),nullable=False)
	latitude=db.Column(db.Float,CheckConstraint('latitude>=-90'),CheckConstraint('latitude <= 90'),nullable=False)
	longitude=db.Column(db.Float,CheckConstraint('longitude>=-180'),CheckConstraint('longitude<=180'),nullable=False)
	price_monthly=db.Column(db.Float,nullable=False)
	price_yearly=db.Column(db.Float,nullable=False)
	owner=db.relationship("app_users")
	creation_date=db.Column(db.DateTime, default=db.func.now())
	space_tens = db.relationship('app_users', secondary=space_tens, backref=db.backref('spaces', lazy='dynamic'))
	tags=db.Column(db.String(500),nullable=False)

	def __init__(self,owner_id,space_name,description,street,province,city,country,max_capacity,latitude,longitude,price_monthly,price_yearly,tags):

		self.owner_id=owner_id
		self.space_name=space_name
		self.description=description
		self.street=street
		self.province=province
		self.city=city
		self.country=country
		self.max_capacity=max_capacity
		self.latitude=latitude
		self.longitude=longitude
		self.price_monthly=price_monthly
		self.price_yearly=price_yearly
		self.tags = tags


class space_applications(db.Model):
	__tablename__ = 'space_applications'

	application_id = db.Column(db.Integer,primary_key=True,nullable=False)
	space_id=db.Column(db.Integer,db.ForeignKey('spaces.space_id'))
	user_applied_id=db.Column(db.Integer,db.ForeignKey('app_users.user_id'))
	owner_id=db.Column(db.Integer,db.ForeignKey('app_users.user_id'))

	def __init__(self,space_id,user_applied_id,owner_id):
		self.space_id=space_id
		self.user_applied_id=user_applied_id
		self.owner_id=owner_id


class space_ratings(db.Model):
	"""docstring for space_ratings"""

	__tablename__='space_ratings'

	space_rating_id = db.Column(db.Integer,primary_key=True,nullable=False)
	space_id=db.Column(db.Integer,db.ForeignKey('spaces.space_id'))
	reviewer_id=db.Column(db.Integer,db.ForeignKey('app_users.user_id'))
	date=db.Column(db.DateTime, default=db.func.now())
	comment=db.Column(db.Text)
	rating=db.Column(db.Integer,CheckConstraint('rating >= 1 AND rating <= 5'))
	reviews=db.relationship("spaces", backref=db.backref('reviews', order_by=date))
	reviewer=db.relationship("app_users")
	#__table_args__ = (UniqueConstraint("space_id", "reviewer_id"), )

	def __init__(self,space_id,reviewer_id,comment,rating):
		self.space_id=space_id
		self.reviewer_id=reviewer_id
		self.rating=rating
		self.comment=comment
		

class owner_ratings(db.Model):
	"""docstring for owner_ratings"""

	__tablename__='owner_ratings'

	owner_rating_id = db.Column(db.Integer,primary_key=True,nullable=False)
	owner_id=db.Column(db.Integer,db.ForeignKey('app_users.user_id'))
	reviewer_id=db.Column(db.Integer,db.ForeignKey('app_users.user_id'))
	date=db.Column(db.DateTime, default=db.func.now())
	comment=db.Column(db.Text)
	rating=db.Column(db.Integer,CheckConstraint('rating >= 1 AND rating <= 5'),nullable=False)
	__table_args__ = (UniqueConstraint("owner_id", "reviewer_id"), )

	def __init__(self, owner_id,reviewer_id,comment,rating):
		self.owner_id=owner_id
		self.reviewer_id=reviewer_id
		self.comment=comment
		self.rating=rating

class tenant_ratings(db.Model):
	"""docstring for tenant_ratings"""

	__tablename__='tenant_ratings'

	tenant_rating_id = db.Column(db.Integer,primary_key=True,nullable=False)
	tenant_id=db.Column(db.Integer,db.ForeignKey('app_users.user_id'))
	reviewer_id=db.Column(db.Integer,db.ForeignKey('app_users.user_id'))
	rating=db.Column(db.Integer,CheckConstraint('rating >= 1 AND rating <= 5'),nullable=False)
	date=db.Column(db.DateTime, default=db.func.now())
	comment=db.Column(db.Text)
	__table_args__ = (UniqueConstraint("tenant_id", "reviewer_id"), )

	def __init__(self, tenant_id,reviewer_id,comment,rating):
		self.tenant_id=tenant_id
		self.reviewer_id=reviewer_id
		self.comment=comment
		self.rating=rating

class interests(db.Model):
	"""docstring for interest"""

	__tablename__='interests'
	interest_id = db.Column(db.Integer, primary_key=True,nullable=False)
	interest_name = db.Column(db.String(40), nullable=False)
	interest_description = db.Column(db.Text, nullable=False)

	def __init__(self, interest_id, interest_name, interest_description):
		self.interest_id = interest_id
		self.interest_description = interest_description
		self.interest_name = self.interest_name

class user_interests(db.Model):
	__tablename__='user_interests'
	user_id = db.Column(db.Integer,db.ForeignKey('app_users.user_id'), primary_key=True, nullable=False)
	interest_id = db.Column(db.Integer,db.ForeignKey('interests.interest_id'), nullable=False)
	date = db.Column(db.DateTime, default=db.func.now())
	__table_args__ = (UniqueConstraint("user_id", "interest_id"), )

	def __init__(self, user_id, interest_id):
		self.user_id=user_id
		self.interest_id=interest_id

class space_interests(db.Model):
	__tablename__='space_interests'
	space_id = db.Column(db.Integer,db.ForeignKey('spaces.space_id'), primary_key=True,nullable=False)
	interest_id = db.Column(db.Integer,db.ForeignKey('interests.interest_id'), nullable=False)
	date = db.Column(db.DateTime, default=db.func.now())
	__table_args__ = (UniqueConstraint("space_id", "interest_id"), )

	def __init__(self, space_id, interest_id):
		self.space_id=space_id
		self.interest_id=interest_id

class messages(db.Model):
	message_id = db.Column(db.Integer,primary_key=True,nullable=False)
	from_user_id = db.Column(db.Integer,db.ForeignKey('app_users.user_id'),nullable=False)
	to_user_id = db.Column(db.Integer,db.ForeignKey('spaces.space_id'),nullable=False)
	date = db.Column(db.DateTime, default=db.func.now())
	message = db.Column(db.Text, nullable=False)
	#__table_args__ = (UniqueConstraint("from_user_id", "to_user_id"), )

	def __init__(self, from_user_id, to_user_id, message):
		self.message = message
		self.from_user_id = from_user_id
		self.to_user_id = to_user_id

class additional_contact_info(db.Model):
	user_id = db.Column(db.Integer,db.ForeignKey('app_users.user_id'), primary_key=True,nullable=False)
	contact_name = db.Column(db.String(40), nullable=False)
	contact_content = db.Column(db.Text, nullable=False)

	def __init__(self, user_id, contact_content, contact_name):
		self.user_id = user_id
		self.contact_name = contact_name
		self.contact_content = contact_content


class space_photos(db.Model):
	"""docstring for space_photos"""

	__tablename__='space_photos'

	space_photo_id = db.Column(db.Integer,primary_key=True,nullable=False)
	space_id=db.Column(db.Integer,db.ForeignKey('spaces.space_id'))
	date_added=db.Column(db.DateTime, default=db.func.now())
	photo_name=db.Column(db.Text)
	photo_url=db.Column(db.Text)
	__table_args__ = (UniqueConstraint("space_id", "photo_url"), )

	def __init__(self,space_id,photo_name,photo_url):
		self.space_id=space_id
		self.photo_name=photo_name
		self.photo_url=photo_url
