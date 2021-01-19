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
	self.measurements = []  
	self.object_id = object_id
	self.location = os.path.expanduser(location)
        self.load(self.location)

    def load(self , location):
       if os.path.exists(location):
           self._load()
       else:
	   self.db = []
       	   return True

    def _load(self):
	self.db = json.load(open(self.location , "r"))
	if int(self.object_id) <= len(self.db):
	   self.measurements = self.db[int(self.object_id)-1]["measurements"]
	else:
	   self.measurements = []

    def dumpdb(self):
        try:
            json.dump(self.db, open(self.location, "w+"), indent=4, cls=ComplexEncoder)
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
        # else:
        meas_item = Measurements(key, value)
        self.measurements.append(meas_item)

    def update(self):
        self.db.append(self.reprJSON())
        self.dumpdb()

    def modify(self,key,value):
        if any(dict_item['name'] == key for dict_item in self.measurements):
            print("Key exists. New value is updated")
            next(dict_item for dict_item in self.measurements if dict_item["name"] == key)["value"] = value
        else:
            meas_item = Measurements(key, value)
            self.measurements.append(meas_item)
            print("New value is added to the objects")

            
        json.dump(self.db, open(self.location, "w+"), indent=4, cls=ComplexEncoder)
        self._load()

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def reprJSON(self):
        return dict(object_id=self.object_id,measurements=self.measurements) 



