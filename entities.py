'''
All the Object Relational Models (ORMs) 
'''

from google.appengine.ext import db

# represents a pet group
class PetGroup(db.Model):
	name = db.StringProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)
	shortCode = db.StringProperty()

# App engine does not provide a sequential, numeric, low value IDs to new database models by default.  
# Instead, this Model will be created to keep an index position of the next ID to assign (for groups)
#
# Allocate IDs for the Group model, https://developers.google.com/appengine/docs/python/datastore/functions#allocate_ids
# Then this model will hold the current index position and the upper range limit
class GroupIndexerSingleton(db.Model):
	index = db.IntegerProperty(required = True)
	upperLimit = db.IntegerProperty(required = True)

# represents a pet linked to a pet group
class Pet(db.Model):
	petGroupId = db.IntegerProperty(required = True)
	name = db.StringProperty(required = True)
	#image
