'''
Base web handler with conviencence functions
'''
import webapp2
import json

errorTag = 'error'

# Base Handler with tailored functions
class AppHandler(webapp2.RequestHandler):
  def write(self, *a, **kw):
    self.response.out.write(*a, **kw)

  def writeError(self, errorString):
  	str = '{"%s":"%s"}' % (errorTag, errorString)
  	self.write(str)

  def writeJSON(self, jsonDict):
  	self.response.headers['Content-Type'] = 'application/json; charset=utf-8'
  	self.write(json.dumps(jsonDict))
