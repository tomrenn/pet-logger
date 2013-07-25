#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
from handlers.SignupGroupHandler import SignupGroupHandler
import util
import json
from entities import PetGroup, SingletonCounter, db

class MainHandler(webapp2.RequestHandler):
    def get(self):
      self.response.headers['Content-Type'] = "application/json; charset=utf-8"
      number = self.request.get("code")
      name = self.request.get("groupname")

      if name == "":
        self.response.write( util.createErrorJSON("Must have a group name") )
        return

      # get allocated id counter (there should only ever be one)
      counter = SingletonCounter.all().get()
      if counter is None:
        handmade_key = db.Key.from_path('PetGroup', 1)
        allocIds = db.allocate_ids(handmade_key, 100000000) # 100 million
        self.response.write("lower: %d , upper: %d" % (allocIds[0], allocIds[1]))
        counter = SingletonCounter(count = allocIds[0], upperLimit=allocIds[1])

      # create new PetGroup using the current count id for a key
      new_key = db.Key.from_path('PetGroup', counter.count)
      shortcode = util.generateShortCode(counter.count)
      new_instance = PetGroup(key=new_key, shortcode=shortcode, name=name)
      new_instance.put()
      counter.count = counter.count + 1
      counter.put()

      # now return json of the new PetGroup
      jsonDictionary = {"name": name,
                        "shortcode": shortcode}
      self.response.write( util.createJSON(jsonDictionary) )




app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/error', SignupGroupHandler)
], debug=True)
