'''
All the Object Relational Models (ORMs) 
'''

from google.appengine.ext import db

# represents a pet group
class PetGroup(db.Model):
	name = db.StringProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)
	shortCodeInteger = db.IntegerProperty(indexed = True)


# represents a pet linked to a pet group
class Pet(db.Model):
	petGroupId = db.IntegerProperty(required = True)
	name = db.StringProperty(required = True)
	#image
