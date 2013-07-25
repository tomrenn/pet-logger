'''
Web Handle to create new pet groups

'''
from BaseHandler import AppHandler
from entities import PetGroup
GROUP_NAME = 'name'

class SignupGroupHandler(AppHandler):
	def post(self):
		name = self.request.get(GROUP_NAME)


	def get(self):
		name = self.request.get(GROUP_NAME)
		if name == '':
			self.writeError('Sorry, you must have a group name')
		else:
			newPetGroup = PetGroup(name = name)
			# TODO: generate a 5 character uqiune code to identify pet group
			
			newPetGroup.put()
			self.writeJSON( {newPetGroup.name : newPetGroup.key().id(), 'inner':{'inner': 'dictionarys'} } )

		