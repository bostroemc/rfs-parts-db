import os
import sys
import signal
import time
import sqlite3
from sqlite3 import Error
import json

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
def add_part(conn, profile):
    try:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        c = conn.cursor()
        c.execute("INSERT INTO parts(profile, timestamp) VALUES(?, ?, ?);", (profile, timestamp))
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
        r = [dict((c.description[i][0], value) for i, value in enumerate(row)) for row in result]
        return r

#dump parts table
def dump(conn):
    c = conn.cursor()
    c.execute("DELETE FROM parts")
    c.execute("DELETE FROM SQLITE_SEQUENCE where name='parts'")
    conn.commit()

#update item in parts table
def update_profile(conn, id, profile):
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    c.execute("SELECT * FROM parts WHERE id = ?", [id])
    result = c.fetchone()
    if result:
       r = [dict((c.description[i][0], value) for i, value in enumerate(result))]

       c.execute("UPDATE parts SET profile = ?, timestamp = ? WHERE id = ?", [profile, timestamp, id])
       conn.commit()

       return r

#update item in parts table incl. description
def update_part(conn, id, description, profile):
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    c.execute("SELECT * FROM parts WHERE id = ?", [id])
    result = c.fetchone()
    if result:
       r = [dict((c.description[i][0], value) for i, value in enumerate(result))]

       c.execute("UPDATE parts SET description = ?, profile = ?, timestamp = ? WHERE id = ?", [description, profile, timestamp, id])
       conn.commit()

       return r

def archive(conn, filename):
    c = conn.cursor()

    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    c.execute("SELECT * FROM parts")
    result = c.fetchall()

    if result:
        parts = [dict((c.description[i][0], value) for i, value in enumerate(row)) for row in result]

        f = open(filename, "w")

        if f:
            f.write(f"IndraMotion Rollfeed Standard (XM RFS) recipe backup: {timestamp}\n")
            for part in parts:
                profile = json.loads(part['profile'])

                f.write(f"Part: {part['id']}\n")
                f.write(f"\tDescription: {part['description']}\n")
                f.write(f"\tDistance: {profile['dist']}\n")
                f.write(f"\tVelocity: {profile['vel']}\n")
                f.write(f"\tAcceleration: {profile['accel']}\n")
                f.write(f"\tLast edited: {part['timestamp']}\n")

            f.close()

        else:
            print("rfs-parts-db unable to open file")

        return

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

            if temp[0] == 'Last edited':
                timestamp = temp[1]        

                #
                # add error checking here
                #
                
                profile = json.dumps({"dist": dist, "vel": vel, "accel": accel})

                c.execute("INSERT INTO parts(description, profile, timestamp) VALUES(?, ?, ?);", (description, profile, timestamp))
                conn.commit() 
                 
                              

        f.close()
        return   