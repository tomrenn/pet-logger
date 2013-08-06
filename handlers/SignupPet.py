'''
Create new pet using a given pet group id

'''
from BaseHandler import AppHandler
from entities import Pet, PetGroup
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import images
from google.appengine.ext import db
from google.appengine.ext import blobstore
from google.appengine.ext import ndb
import urllib


PET_NAME = 'name'
			

# Serve the pet image saved for the given blobstore key
class ServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
  def get(self, resource):
    resource = str(urllib.unquote(resource))
    blob_info = blobstore.BlobInfo.get(resource)
    self.send_blob(blob_info)

# Called after file is uploaded
# If file is not an image, show error 
class UploadHandler(blobstore_handlers.BlobstoreUploadHandler, AppHandler):
	def post(self):
		upload_files = self.get_uploads('photo')  # 'file' is file upload field in the form



		# if the user uploaded a file
		if upload_files:
			blob_info = upload_files[0]
			imageKey = blob_info.key()

			# Check valid image file
			image_types = ('image/bmp', 'image/jpeg', 'image/png')
			if blob_info.content_type not in image_types:
				blob_info.delete()
				self.redirect('/pet/error?msg=invalid%20file%20type')
				return
			else:
				# resize image to prevent storing too much data
				pass
		else:
			imageKey = None

		petName = self.request.get('petName')
		# provide a default pet group name if one is not provided
		# for some absolutely bazare reason, the default value is not working..
		groupName = self.request.get('groupName', default_value = 'My Pet Family')
		# force default value
		if not groupName:
			groupName = 'My Pet Family'

		groupCode = self.getNextPetGroupCode()
		newGroup = PetGroup(name=groupName, shortCodeInteger=groupCode)
		import util
		shortCode = util.encode(groupCode)

		if not petName:
			self.writeError("Sorry, please give your pet a name!")
			return

		newGroup.put()
		groupId = newGroup.key().id()
		newPet = Pet(name=petName, photoKey=imageKey, petGroup=groupId)
		newPet.put()
		# output json
		self.writeJSON( {'pet' : {'name': petName,
								  'id': str(newPet.key().id()),
								  'parentGroup': groupId,
								  'photoUrl': self.request.host_url+'/pet/img/'+str(imageKey)
								 },
						 'group': {'name': groupName,
						 		   'id': groupId,
						 		   'shortCode': shortCode,
						 		  }
		})


	# get the most recently added pet group (one with highest shortCodeInteger)
	# return highest shortCodeInteger + 1
	def getNextPetGroupCode(self):
		q = PetGroup.all()
		q.order('-shortCodeInteger')
		group = q.get()

		if group:
			updatedPos = group.shortCodeInteger + 1
			return updatedPos
		else:
			return 0

# Upload handler received file properly, now attempt creating pet
# class SuccessHandler(AppHandler):

# 	def get(self, imageKey):

		# petName = self.request.get('petName')
		# # provide a default pet group name if one is not provided
		# groupName = self.request.get('groupName', 'My Pet Family')


		# groupCode = getNextPetGroupCode(self)
		# newGroup = PetGroup(name=groupName, shortCodeInteger=groupCode)
		# import util
		# shortCode = util.encode(groupCode)

		# if not petName:
		# 	self.writeError("Sorry, please give your pet a name!")
		# 	return

		# newGroup.put()
		# groupId = newGroup.key().id()
		# newPet = Pet(name=petName, photoKey=imageKey, petGroup=groupId)
		# newPet.put()
		# # output json
		# self.writeJSON( {'pet' : {},
		# 				 'group': {}
		# 	})

	

# Show error message
class ErrorHandler(AppHandler):
	def get(self):
		message = self.request.get("msg")
		self.writeJSON({"error": message})

# Provides a new url if a petID is not given
# Otherwise provide pet information in JSON
class UploadURL(AppHandler):
	def get(self, petID=None):
		if petID:
			pet = Pet.get_by_id(int(petID))
			if pet.photoKey:
				key = self.request.host_url+'/pet/img/'+str(pet.photoKey.key())
			else:
				key = ''
			self.writeJSON({"pet": petID,
							"name": pet.name,
							"photoURL": key
						})
		else:
			uploadURL = blobstore.create_upload_url('/pet/upload')
			self.write("<html> <body> ")
			self.write('<form method="POST" enctype="multipart/form-data" action="%s">' % uploadURL)
			self.write('Name: <input type="text" name="petName"> <br>')
			self.write('Group Name: <input type="text" name="groupName" placeholder="optional"> <br> ')
			self.write('Picture: <input type="file" name="photo"> <br>')
			self.write('<input type="submit"> </form> </body> </html>')



		