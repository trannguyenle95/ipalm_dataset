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
class Measurements:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def reprJSON(self):
        return dict(name=self.name, value=self.value) 

#######################################
class ObjectMeasurements(object):
    def __init__(self,location,object_id):
	self.object_id = object_id
	self.location = os.path.expanduser(location)
        self.load(self.location)
	self.measurements = []  
    def load(self , location):
       if os.path.exists(location):
           self._load()
       else:
	   self.db = {}
       	   return True

    def _load(self):
        self.db = json.load(open(self.location , "r"))
        #self.measurements = self.db["measurements"]
	self.measurements = []
    def dumpdb(self):
        try:
            json.dump(self.reprJSON(), open(self.location, "a"), indent=4, cls=ComplexEncoder)
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
    
    def add_meas(self, key, value):
	meas_item = Measurements(key, value)
	self.measurements.append(meas_item)
    	self.dumpdb()

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def reprJSON(self):
        return dict(object_id=self.object_id,measurements=self.measurements) 



