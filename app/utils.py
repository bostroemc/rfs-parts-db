import os
import sys
import signal
import time
import sqlite3
from sqlite3 import Error
import json

# part format:  {"description":"", "profile":{"dist":[75], "vel":[75], "accel":[75], "qty":[0]}}


# initialize database connection, adding tables queue and history if required
def initialize(db):
    conn = None
    try:
        conn = sqlite3.connect(db, uri=True)
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS parts (id integer PRIMARY KEY AUTOINCREMENT, description text, profile text, timestamp text);") # profile as json, timestamp = time of last edit

        return conn

    except Error as e:
        print(e)

    return conn

# add part to parts table
def add_part(conn, description, profile):
    temp = normalize(profile)  # filter unwanted fields + add defaults

    try:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        c = conn.cursor()
        c.execute("INSERT INTO parts(description, profile, timestamp) VALUES(?, ?, ?);", (description, json.dumps(temp), timestamp))
        conn.commit()

        return c.lastrowid

    except Error as e:
       print(e)

# return parts count
def count(conn):
    c = conn.cursor()
    parts = c.execute("SELECT * FROM parts")
    return len(parts.fetchall())

#fetch parts
def fetch(conn, limit, offset):
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM parts LIMIT ? OFFSET ?", [limit, offset])
    result = c.fetchall()

    if result:
        #r = [dict((c.description[i][0], value) for i, value in enumerate(row)) for row in result]
        r = []
        for row in result:
            _temp = dict((c.description[i][0], value) for i, value in enumerate(row))
            _temp["profile"] = json.loads(_temp["profile"])

            r.append(_temp)
        return r

#dump parts table
def dump(conn):
    c = conn.cursor()
    c.execute("DELETE FROM parts")
    c.execute("DELETE FROM SQLITE_SEQUENCE where name='parts'")
    conn.commit()

#update profile of item in parts table  TODO determine whether this is needed; not currently used
def update_profile(conn, id, profile):
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    c.execute("SELECT * FROM parts WHERE id = ?", [id])
    result = c.fetchone()
    if result:
       r = dict((c.description[i][0], value) for i, value in enumerate(result))
       temp = json.loads(r["profile"])
       temp.update(filter(profile))  #incomplete profiles such as {"dist": [12.5]} are allowed and will be merged with other existing fields; filter removes unwanted fields

       c.execute("UPDATE parts SET profile = ?, timestamp = ? WHERE id = ?", [json.dumps(temp), timestamp, id])
       conn.commit()

       r.update({"profile":temp, "timestamp": timestamp})

       return r

#update item in parts table incl. description
def update_part(conn, id, description, profile):
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    c.execute("SELECT * FROM parts WHERE id = ?", [id])
    result = c.fetchone()
    if result:
        r = dict((c.description[i][0], value) for i, value in enumerate(result))
        if profile:
            r = dict((c.description[i][0], value) for i, value in enumerate(result))
            temp = json.loads(r["profile"])
            temp.update(filter(profile))  #incomplete profiles such as {"dist": [12.5]} are allowed and will be merged with other existing fields; filter removes unwanted fields
       
            if description:
                c.execute("UPDATE parts SET description = ?, profile = ?, timestamp = ? WHERE id = ?", [description, json.dumps(temp), timestamp, id])
                conn.commit()
            else:
                c.execute("UPDATE parts SET profile = ?, timestamp = ? WHERE id = ?", [json.dumps(temp), timestamp, id])
                conn.commit()
        elif description:
            c.execute("UPDATE parts SET description = ?, timestamp = ? WHERE id = ?", [description, timestamp, id])
            conn.commit()    

        return True

def archive(conn, filename):
    c = conn.cursor()

    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    c.execute("SELECT * FROM parts")
    result = c.fetchall()

    if result:
        parts = [dict((c.description[i][0], value) for i, value in enumerate(row)) for row in result]

        f = open(filename, "w")

        if f:
            f.write(f"IndraMotion Rollfeed Standard (CTRLX RFS) recipe backup: {timestamp}\n")
            for part in parts:
                profile = json.loads(part['profile'])

                f.write(f"Part: {part['id']}\n")
                f.write(f"\tDescription: {part['description']}\n")
                f.write(f"\tDistance: {profile['dist']}\n")
                f.write(f"\tVelocity: {profile['vel']}\n")
                f.write(f"\tAcceleration: {profile['accel']}\n")
                f.write(f"\tQuantity: {profile['qty']}\n")
                f.write(f"\tLast edited: {part['timestamp']}\n")

            f.close()
            return True
        else:
            print("rfs-parts-db unable to open file")
            return False

def restore(conn, filename):
    c = conn.cursor()

    f = open(filename, "r")

    if f:
        c.execute("DELETE FROM parts")    
        c.execute("DELETE FROM SQLITE_SEQUENCE where name='parts'")
        conn.commit()

        for x in f:
            temp = x.strip().split(': ')
            if temp[0] == 'Part':
                id = temp[1]

            if temp[0] == 'Description':
                description = temp[1]

            if temp[0] == 'Distance':
                dist = [float(x) for x in temp[1].strip("[]").split(', ')]

            if temp[0] == 'Velocity':
                vel = [float(x) for x in temp[1].strip("[]").split(', ')]

            if temp[0] == 'Acceleration':
                accel = [float(x) for x in temp[1].strip("[]").split(', ')]

            if temp[0] == 'Quantity':
                qty = [int(x) for x in temp[1].strip("[]").split(', ')]

            if temp[0] == 'Last edited':
                timestamp = temp[1]        

                #
                # add error checking here
                #
                
                profile = json.dumps({"dist": dist, "vel": vel, "accel": accel, "qty": qty})

                c.execute("INSERT INTO parts(description, profile, timestamp) VALUES(?, ?, ?);", (description, profile, timestamp))
                conn.commit() 

        f.close()
        return True


    else:
        print("rfs-parts-db unable to open file")
        return False                           

# filter out unwanted fields; profile passed as dictionary
def filter(profile): 
    default = {"dist": [], "vel": [], "accel": [], "qty": []} 
    
    try:
        common_keys = profile.keys() & default.keys()

        return {k: profile[k] for k in common_keys}    

    except ValueError:
        return  proto  

# filter out unwanted fields and add default values for any missing fields; profile passed as dictionary
def normalize(profile):   
    default = {"dist": [12], "vel": [75], "accel": [75], "qty": [0]} 
    
    try:
        common_keys = profile.keys() & default.keys()
        a ={k: profile[k] for k in common_keys} 

        return {**default, **a}     

    except ValueError:
        return  default  