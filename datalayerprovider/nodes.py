# MIT License
#
# Copyright (c) 2020, Bosch Rexroth AG
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import datalayer.clib
from datalayer.provider_node import ProviderNodeCallbacks, NodeCallback
from datalayer.variant import Result, Variant

import json
# import time
import os
# import sqlite3
from sqlite3 import Error
#from jsonschema import validate

import datalayerprovider.utils

# add part to database; required format:  {"description": "", "profile":{"dist": [], "vel": [], "accel":[]}}
class Push:
    _value: str = ""
    id : int = 0

    schema = {
        "type" : "object",
        "properties" : {
            "description" : {"type" : "string"},
            "profile" : {"type" : "string"},
        },
        "required" : ["profile"]
    }
    
    def __init__(self, db):
        self.cbs = ProviderNodeCallbacks(
        self.__on_create,
        self.__on_remove,
        self.__on_browse,
        self.__on_read,
        self.__on_write,
        self.__on_metadata
        )
        self.db = db

    def __on_create(self, userdata: datalayer.clib.userData_c_void_p, address: str, data: Variant, cb: NodeCallback):
        self._value
        cb(Result(Result.OK), None)

    def __on_remove(self, userdata: datalayer.clib.userData_c_void_p, address: str, cb: NodeCallback):
        # Not implemented because no wildcard is registered
        cb(Result(Result.UNSUPPORTED), None)

    def __on_browse(self, userdata: datalayer.clib.userData_c_void_p, address: str, cb: NodeCallback):
        _data = Variant()
        _data.set_array_string([])
        cb(Result(Result.OK), _data)

    def __on_read(self, userdata: datalayer.clib.userData_c_void_p, address: str, data: Variant, cb: NodeCallback):
        _data = Variant()

        conn = datalayerprovider.utils.initialize(self.db)
        if conn:
            _data.set_string(json.dumps(datalayerprovider.utils.fetch(conn, 20, 0))) 
            conn.close()

        cb(Result(Result.OK), _data)
    
    def __on_write(self, userdata: datalayer.clib.userData_c_void_p, address: str, data: Variant, cb: NodeCallback):
        _description = ""
        _profile = {}

        _test = json.loads(data.get_string())

        if "description" in _test:
            _description = _test["description"]

        if "profile" in _test:    
            _profile = _test["profile"]

        # _isValid = validate(_test, self.schema)
 
        conn = datalayerprovider.utils.initialize(self.db)
        if conn: # and _isValid:
            datalayerprovider.utils.add_part(conn, _description, _profile)
            conn.close()

        cb(Result(Result.OK), None)        

    def __on_metadata(self, userdata: datalayer.clib.userData_c_void_p, address: str, cb: NodeCallback):
        print("__on_metadata")
        cb(Result(Result.OK), None)

# update part in database; required format:  {"id": 1, "description": "", "profile":{"dist": [], "vel": [], "accel":[]}}
class Update:
    _value: str = ""
    id : int = 0

    schema = {
        "type" : "object",
        "properties" : {
            "description" : {"type" : "string"},
            "profile" : {"type" : "string"},
        },
        "required" : ["profile"]
    }
    
    def __init__(self, db):
        self.cbs = ProviderNodeCallbacks(
        self.__on_create,
        self.__on_remove,
        self.__on_browse,
        self.__on_read,
        self.__on_write,
        self.__on_metadata
        )
        self.db = db

    def __on_create(self, userdata: datalayer.clib.userData_c_void_p, address: str, data: Variant, cb: NodeCallback):
        self._value
        cb(Result(Result.OK), None)

    def __on_remove(self, userdata: datalayer.clib.userData_c_void_p, address: str, cb: NodeCallback):
        # Not implemented because no wildcard is registered
        cb(Result(Result.UNSUPPORTED), None)

    def __on_browse(self, userdata: datalayer.clib.userData_c_void_p, address: str, cb: NodeCallback):
        _data = Variant()
        _data.set_array_string([])
        cb(Result(Result.OK), _data)

    def __on_read(self, userdata: datalayer.clib.userData_c_void_p, address: str, data: Variant, cb: NodeCallback):
        _data = Variant()

        conn = datalayerprovider.utils.initialize(self.db)
        if conn:
            _data.set_string(json.dumps(datalayerprovider.utils.fetch(conn, 20, 0))) 
            conn.close()

        cb(Result(Result.OK), _data)
    
    def __on_write(self, userdata: datalayer.clib.userData_c_void_p, address: str, data: Variant, cb: NodeCallback):
        _id = 0
        _description = ""
        _profile = {}

        _test = json.loads(data.get_string())
        if "id" in _test:
            _id = _test["id"]

        if "description" in _test:
            _description = _test["description"]

        if "profile" in _test:    
            _profile = _test["profile"]

        conn = datalayerprovider.utils.initialize(self.db)
        if conn and _id: 
            datalayerprovider.utils.update_part(conn, _id, _description, _profile)
            conn.close()

        cb(Result(Result.OK), None)        

    def __on_metadata(self, userdata: datalayer.clib.userData_c_void_p, address: str, cb: NodeCallback):
        print("__on_metadata")
        cb(Result(Result.OK), None)        

# retrieve database and write to file (verbose text format)
class Archive:
    _value: str = ""

    def __init__(self, db):
        self.cbs = ProviderNodeCallbacks(
        self.__on_create,
        self.__on_remove,
        self.__on_browse,
        self.__on_read,
        self.__on_write,
        self.__on_metadata
        )
        self.db = db

    def __on_create(self, userdata: datalayer.clib.userData_c_void_p, address: str, data: Variant, cb: NodeCallback):
        self.data
        cb(Result(Result.OK), None)

    def __on_remove(self, userdata: datalayer.clib.userData_c_void_p, address: str, cb: NodeCallback):
        # Not implemented because no wildcard is registered
        cb(Result(Result.UNSUPPORTED), None)

    def __on_browse(self, userdata: datalayer.clib.userData_c_void_p, address: str, cb: NodeCallback):
        _data = Variant()
        _data.set_array_string([])
        cb(Result(Result.OK), _data)

    def __on_read(self, userdata: datalayer.clib.userData_c_void_p, address: str, data: Variant, cb: NodeCallback):
        _data = Variant()  
        _data.set_string(self._value)
           
        cb(Result(Result.OK), _data)
    
    def __on_write(self, userdata: datalayer.clib.userData_c_void_p, address: str, data: Variant, cb: NodeCallback):
        _data = Variant()
        
        print("rfs-parts-db attempting to write file")
        
        conn = datalayerprovider.utils.initialize(self.db)
        if conn and int(data.get_string()) == 1: 
            self._value = json.dumps(datalayerprovider.utils.archive(conn, "/media/sda1/BACKUP_RFS.txt"))  # prev.   "/media/mmcblk1p1/BACKUP_RFS.txt"
            _data.set_string(self._value)
        
        if conn: 
            conn.close()

        cb(Result(Result.OK), _data)        

    def __on_metadata(self, userdata: datalayer.clib.userData_c_void_p, address: str, cb: NodeCallback):
        cb(Result(Result.OK), None)       

# read file in verbose text format and overwrite database
class Restore:
    _value: str = ""

    def __init__(self, db):
        self.cbs = ProviderNodeCallbacks(
        self.__on_create,
        self.__on_remove,
        self.__on_browse,
        self.__on_read,
        self.__on_write,
        self.__on_metadata
        )
        self.db = db

    def __on_create(self, userdata: datalayer.clib.userData_c_void_p, address: str, data: Variant, cb: NodeCallback):
        self.data
        cb(Result(Result.OK), None)

    def __on_remove(self, userdata: datalayer.clib.userData_c_void_p, address: str, cb: NodeCallback):
        # Not implemented because no wildcard is registered
        cb(Result(Result.UNSUPPORTED), None)

    def __on_browse(self, userdata: datalayer.clib.userData_c_void_p, address: str, cb: NodeCallback):
        _data = Variant()
        _data.set_array_string([])
        cb(Result(Result.OK), _data)

    def __on_read(self, userdata: datalayer.clib.userData_c_void_p, address: str, data: Variant, cb: NodeCallback):
        _data = Variant()  
        _data.set_string(self._value)
           
        cb(Result(Result.OK), _data)
    
    def __on_write(self, userdata: datalayer.clib.userData_c_void_p, address: str, data: Variant, cb: NodeCallback):
        _data = Variant()
   
        conn = datalayerprovider.utils.initialize(self.db)
        if conn and int(data.get_string()) == 1: 
            self._value = json.dumps(datalayerprovider.utils.restore(conn, "/media/sda1/BACKUP_RFS.txt"))  # prev.   "/media/mmcblk1p1/BACKUP_RFS.txt"
            _data.set_string(self._value)
        
        if conn: 
            conn.close()

        cb(Result(Result.OK), _data)        

    def __on_metadata(self, userdata: datalayer.clib.userData_c_void_p, address: str, cb: NodeCallback):
        cb(Result(Result.OK), None)                       