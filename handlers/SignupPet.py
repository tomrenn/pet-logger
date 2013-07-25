'''
Create new pet using a given pet group id

'''
from BaseHandler import AppHandler
from entities import PetGroup
PET_NAME = 'name'

class SignupPetHandler(AppHandler):
	def post(self):
		name = self.request.get(PET_NAME)


	def get(self):
		name = self.request.get(PET_NAME)
		if name == '':
			self.writeError('Sorry, your pet must have a name')
		else:
			newPetGroup = PetGroup(name = name)
			newPetGroup.put()
			self.writeJSON( {newPetGroup.name : newPetGroup.key().id(), 'inner':{'inner': 'dictionarys'} } )

		