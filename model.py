import json
from json import JSONEncoder
import os
####################################### subclass JSONEncoder
class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj,'reprJSON'):
            return obj.reprJSON()
        else:
            return json.JSONEncoder.default(self, obj)
########################################
class Properties:
    def __init__(self, name, type):
        self.name = name
        self.type = type

    def reprJSON(self):
        return dict(name=self.name, type=self.type) 
########################################
class Relations:
    def __init__(self, parent, child, type, parameters):
        self.parent = parent
        self.child = child
	self.type = child
	self.parameters = parameters

    def reprJSON(self):
        return dict(parent=self.parent, child=self.child,type=self.type,parameters=self.parameters) 

#######################################
class Model(object):
    def __init__(self,location):
	self.location = os.path.expanduser(location)
        self.load(self.location)

    def load(self , location):
       if os.path.exists(location):
           self._load()
       else:
	   self.db = {}
      	   self.properties = []  
           self.relations = []
       	   return True

    def _load(self):
        self.db = json.load(open(self.location , "r"))
        self.properties = self.db["properties"]
        self.relations = self.db["relations"]

    def dumpdb(self):
        try:
            json.dump(self.reprJSON(), open(self.location, "w+"), indent=4, cls=ComplexEncoder)
            return True
        except:
            return False

    def get(self , key):
        try:
            return self.db[key]
        except KeyError:
            print("No Value Can Be Found for " + str(key))
            return False

    def delete(self , key):
        if not key in self.db:
            return False
        del self.db[key]
        self.dumpdb()
        return True
    
    def add_prop(self, key, value):
	prop_item = Properties(key, value)
	self.properties.append(prop_item)
    	self.dumpdb()

    def add_relation(self, parent, child, type, parameters):
	relate_item = Relations(parent, child, type, parameters)
	self.relations.append(relate_item)
    	self.dumpdb()

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def reprJSON(self):
        return dict(properties=self.properties, relations=self.relations) 



