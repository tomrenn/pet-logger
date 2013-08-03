'''
Web Handle to create new pet groups

'''
from BaseHandler import AppHandler
from entities import PetGroup
GROUP_NAME = 'name'


# get the most recently added pet group (one with highest shortCodeInteger)
# return highest shortCodeInteger + 1
def getNextPetGroupCode():
	q = PetGroup.all()
	q.order('shortCodeInteger')
	group = q.get()

	if group:
		return (group.shortCodeInteger + 1)
	else:
		return 0

class SignupGroupHandler(AppHandler):
	def post(self):
		name = self.request.get(GROUP_NAME)




	def get(self):
		
		name = self.request.get(GROUP_NAME)
		if not name:
			self.writeError('Sorry, you must have a group name')
		else:
			from util import *
			sci = getNextPetGroupCode()
			newPetGroup = PetGroup(name = name, shortCodeInteger = sci)
			
			newPetGroup.put()

			shortcode = encode(sci)

			self.writeJSON( {
					GROUP_NAME : newPetGroup.name,
					'id' : newPetGroup.key().id(),
					'shortcode' : shortcode
				}
			)

	
