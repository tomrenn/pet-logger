'''
All the Object Relational Models (ORMs) 
'''

from google.appengine.ext import db
from google.appengine.ext.blobstore import blobstore

# represents a pet group
class PetGroup(db.Model):
	name = db.StringProperty(required = True, default='My Pet Family')
	created = db.DateTimeProperty(auto_now_add = True)
	shortCodeInteger = db.IntegerProperty(indexed = True)


# represents a pet linked to a pet group
class Pet(db.Model):
	name = db.StringProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)
	photoKey = blobstore.BlobReferenceProperty()
	petGroup = db.IntegerProperty(required = True)
