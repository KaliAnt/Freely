import os 
import sys
import sqlite3
import time

from flask import jsonify
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash
from flask_cors import CORS, cross_origin

#create app instance
app = Flask(__name__)
CORS(app)
app.config.from_object(__name__)



app.config.update(dict(
    FLASK_DEBUG = True,
    SECRET_KEY = 'development key',
    USERNAME = 'admin',
    DATABASE=os.path.join(app.root_path, 'history.db'),
    PASSWORD = 'default'
))

app.config.from_envvar('FLASKR_SETTINGS', silent = True)

def init_db():
    db = get_db()
    with app.open_resource('schema.sql',mode = 'r') as f:
        db.cursor().executescript(f.read())
    db.commit()

def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

# METHODS

@app.route('/loginTest', methods=['POST'])
def login_test():
        request_dict = request.get_json()
        if request_dict == None:
            print("Invalid data", sys.stderr)
            return '{"status":"ERROR"}'
        # print(request_dict, sys.stderr)

        try:
            values = [request_dict['username'],
                    request_dict['password']]
        except KeyError:
            print("Invalid data", sys.stderr)
            return '{"status":"ERROR"}'

        print("[ INFO ] Test user login: {}").format(values[0])
        
        return '{"status":"OK"}'

@app.route('/login', methods=['POST'])
def login():
    request_dict = request.get_json()
    if request_dict == None:
        print("[ ERROR ] Invalid data", sys.stderr)
        return '{"status":"ERROR"}'
    
    try:
        if request_dict['email'] == "" or request_dict['password']== "":
            print("[ ERROR ] Invalid data", sys.stderr)
            return '{"status":"ERROR"}'
        values = [request_dict['email'],
        request_dict['password']]
    
    except KeyError:
        print("Invalid data", sys.stderr)
        return '{"status":"ERROR"}'

    try:
        db = get_db()
        
        query = 'select FirstName, LastName, Birthdate, Rating, Email, Description from Users where Email=\'' + values[0] + '\' and Password=\'' + values[1] + '\''
        query2 = 'select name, Rating, Email, Description from Organisations where Email=\'' + values[0] + '\' and Password=\'' + values[1] + '\''
        
        try:
            for row in db.execute(query):
                user = {
                    "firstName" : row[0],
                    "lastName" : row[1],
                    "birthdate" : row[2],
                    "rating" : row[3],
                    "email" : row[4],
                    "description" : row[5]
                }

            result = {
                "type" : "volunteer",
                "data" : user,
                "status" : "OK"
            }
                  
            res = jsonify(result)
            print(res)
            return res
        except:
            try:
                for row in db.execute(query2):
                    org = {
                        "name" : row[0],
                        "rating" : row[1],
                        "email" : row[2],
                        "description" : row[3]
                    }

                result2 = {
                    "type" : "organisation",
                    "data" : org,
                    "status" : "OK"
                }

                res2 = jsonify(result2)
                print(res2)
                return res2
            except:
                print("[ ERROR ] No organisation or user", sys.stderr)
                return '{"status":"ERROR"}'    

    except:
        print("[ ERROR ] No organisation or user", sys.stderr)
        return '{"status":"ERROR"}'    


@app.route('/registerUser', methods=['POST'])
def registerUser():
    request_dict = request.get_json()
    if request_dict == None:
        print("[ ERROR ] Invalid data", sys.stderr)
        return '{"status":"ERROR"}'
    
    try:
        values = [request_dict['email'],
        request_dict['password'],
        request_dict['firstname'],
        request_dict['lastname'],
        request_dict['birthdate'],
        request_dict['description'],
        "5.0"]

        #TO-DO description can be null
        for element in values:
            if element == "":
                print("[ ERROR ] Invalid data", sys.stderr)
                return '{"status":"ERROR"}'

    except KeyError:
        print("[ ERROR ] Invalid data", sys.stderr)
        return '{"status":"ERROR"}'
    try:
        db = get_db()
        db.execute('insert into Users (email, password, firstname, lastname, birthdate, description, rating) values (?,?,?,?,?,?,?)', values)
        db.commit()
        return '{"status":"OK"}'
    except:
        print("[ ERROR ] Can't insert data in db", sys.stderr)
        return '{"status":"ERROR"}'

    

@app.route('/registerOrganisation', methods=['POST'])
def registerOrganisation():
    request_dict = request.get_json()
    if request_dict == None:
        print("[ ERROR ] Invalid data", sys.stderr)
        return '{"status":"ERROR"}'
    
    try:
        values = [request_dict['email'],
        request_dict['password'],
        request_dict['name'],
        request_dict['description'],
        "5.0"]

        #TO-DO description can be null
        for element in values:
            if element == "":
                print("[ ERROR ] Invalid data", sys.stderr)
                return '{"status":"ERROR"}'

    except KeyError:
        print("Invalid data", sys.stderr)
        return '{"status":"ERROR"}'
    try:
        db = get_db()
        db.execute('insert into Organisations (email, password, name, description, rating) values (?,?,?,?,?)', values)
        db.commit()
        return '{"status":"OK"}'
    except:
        print("[ ERROR ] Can't insert data in db", sys.stderr)
        return '{"status":"ERROR"}'

@app.route('/createEvent', methods=['POST'])
def createEvent():
    request_dict = request.get_json()
    print(request_dict, sys.stderr)
    if request_dict == None:
        print("[ ERROR ] Invalid data: dict is null", sys.stderr)
        return '{"status":"ERROR"}'
    
    #TO-DO return category
    try:
        values = [request_dict['name'],
        request_dict['date'],
        request_dict['description'],
        request_dict['organisation'],
        request_dict['category'],
        request_dict['location']]

        #TO-DO description can be null
        for element in values:
            if element == "":
                print("[ ERROR ] Invalid data", sys.stderr)
                return '{"status":"ERROR"}'

    except KeyError:
        print("Invalid data", sys.stderr)
        return '{"status":"ERROR"}'

    try:
        db = get_db()
        cur = db.cursor()

        query = 'select organisationId from Organisations where name=\'' + values[3] + '\''
        query2 = 'select categoryId from Categories where name=\'' + values[4] + '\''
        query3 = 'select eventId from Events where name=\'' + values[0] + '\''
        
        for row in db.execute(query):
            organisationId = row[0]
            break
        
        event = [request_dict['name'],
        request_dict['description'],
        request_dict['date'],
        organisationId,
        request_dict['location']]

        db.execute('insert into events (name, description, date, organisationId, location) values (?,?,?,?,?)', event)
        db.commit()
        #TO-Do fix this mess. only one value expected!!
        
        cur.execute('select categoryId from categories where name=?', (values[4],))
        categoryId = cur.fetchone()

        if categoryId == None:
            print("No such category", sys.stderr)
            return '{"status":"ERROR"}'

        for row2 in db.execute(query3):
            eventId = row2[0]
            break
        
        eventValues = [organisationId, eventId]

        db.execute('insert into OrganisationEvents (organisationid, eventid) values (?,?)', eventValues)
        db.commit()

        for row3 in db.execute(query3):
            eventId = row3[0]
            break

        eventCategories = [eventId, categoryId[0]]
        
        db.execute('insert into eventCategories (eventid, categoryid) values (?,?)', eventCategories)

        db.commit()

        return '{"status":"OK"}'
    except KeyError:
        print("[ ERROR ] Can't insert data in db", sys.stderr)
        return '{"status":"ERROR"}'

@app.route('/modifyEvent', methods=['POST'])
def modifyEvent():
    request_dict = request.get_json()
    if request_dict == None:
        print("[ ERROR ] Invalid data", sys.stderr)
        return '{"status":"ERROR"}'

    event = request_dict["name"]
    email = request_dict["organisation"]
    
    if event == "" or email == "":
        print("[ ERROR ] Invalid event and email data", sys.stderr)
        return '{"status":"ERROR"}'

    try:
        db = get_db()
        cur = db.cursor()

        query = 'select organisationId from Organisations where email = \'' + email + '\''
        cur.execute(query)
        row = cur.fetchone()

        if row == None:
            print("[ ERROR ] No such organisation exists", sys.stderr)
            return '{"status":"ERROR"}'

        organisationId = row[0]

        query1 = 'select eventId from Events where organisationId=\'' + str(organisationId) + '\' and name = \'' + event + '\''

        cur.execute(query1)
        row = cur.fetchone()

        if row == None:
            print("[ ERROR ] No such event exists", sys.stderr)
            return '{"status":"ERROR"}' 

        eventId = row[0]

        db.execute('update events set name=?, description=?, date=?, location=?  where eventid=?', (request_dict["name"], request_dict["description"], request_dict["date"], request_dict["location"], str(eventId)))
        db.commit()

        return '{"status":"OK"}'
    
    except KeyError:
        print("Invalid data", sys.stderr)
        return '{"status":"ERROR"}'

@app.route('/getOneEvent', methods=['GET'])
def getOneEvent():
    pass


@app.route('/searchEvent', methods=['GET'])
def searchEvent():
    request_dict = request.get_json()
    if request_dict == None:
        print("[ ERROR ] Invalid data", sys.stderr)
        return '{"status":"ERROR"}'

    name = request_dict["name"]

    try:
        db = get_db()
        cur = db.cursor()

        query = 'select name, description, date, location, organisationId from Events where name like \'' + name + '%\''
        events = []
        for row in db.execute(query):
            cur.execute('select email, name from Organisations where organisationId = ?', (row[4],))
            curRow = cur.fetchone()

            evt = {
                "name" : row[0],
                "description" : row[1],
                "date" : row[2],
                "location": row[3],
                "organisation": curRow[1],
                "organisationEmail": curRow[0]
            }
            events.append(evt)
        res = jsonify(events)
        print(res)
        return res


    
    except KeyError:
        print("Invalid data", sys.stderr)
        return '{"status":"ERROR"}'
    


@app.route('/createApplication', methods=['POST'])
def createApplication():
    request_dict = request.get_json()
    if request_dict == None:
        print("[ ERROR ] Invalid data", sys.stderr)
        return '{"status":"ERROR"}'
    
    try:
        values = [request_dict['email'],
        request_dict['event'],
        request_dict['type']]

        #type can be interested or pending if user applied

        for element in values:
            if element == "":
                print("[ ERROR ] Invalid data", sys.stderr)
                return '{"status":"ERROR"}'

    except KeyError:
        print("[ ERROR ] Invalid data", sys.stderr)
        return '{"status":"ERROR"}'

    try:
        db = get_db()
        query = 'select userId from Users where email=\'' + values[0] +'\''
        query2 = 'select eventId from Events where name=\'' + values[1] + '\''

        for row in db.execute(query):
            userId = row[0]
            break

        for row2 in db.execute(query2):
            eventId = row2[0]
            break
        
        if values[2] == "pending":
            appType = "2"
        else:
            appType = "1"
        applicationValues = [userId, eventId, appType]
        db.execute('insert into Applications (userid, eventid, statusid) values (?,?,?)', applicationValues)
        db.commit()
        return '{"status":"OK"}'

    except:
        print("[ ERROR ] Invalid data", sys.stderr)
        return '{"status":"ERROR"}'

@app.route('/modifyStatusForApplication', methods=['POST'])
def modifyStatusForApplication():
    request_dict = request.get_json()
    if request_dict == None:
        print("[ ERROR ] Invalid data", sys.stderr)
        return '{"status":"ERROR"}'

    try:
        email = request_dict['email']
        eventname = request_dict['event']
        statusType = request_dict['status']

        if email == "" or eventname == "" or statusType == "":
            print("[ ERROR ] Invalid email or eventname or status", sys.stderr)
            return '{"status":"ERROR"}'

        db = get_db()
        cur = db.cursor()

        cur.execute('select statusId from status where name=?', (statusType, ))
        statusId = cur.fetchone()

        if statusId == None:
            print("[ ERROR ] Invalid status type", sys.stderr)
            return '{"status":"ERROR"}'

        query = 'select userId from Users where email=\'' + email + '\''
        cur.execute(query)
        userId = cur.fetchone()

        if userId == None:
            print("[ ERROR ] Invalid user email", sys.stderr)
            return '{"status":"ERROR"}'

        query4 = 'select eventId from Events where name=\'' + eventname + '\''
        cur.execute(query4)
        eventId = cur.fetchone()

        if eventId == None:
            print("[ ERROR ] Invalid user email", sys.stderr)
            return '{"status":"ERROR"}'

        cur.execute('select applicationId from applications where userId=? and eventId=?', (userId[0], eventId[0],))
        applicationId = cur.fetchone()
        if applicationId == None:
            print("[ ERROR ] No such application exists", sys.stderr)
            return '{"status":"ERROR"}'

        cur.execute('select statusId from applications where applicationId=?', (applicationId[0],))
        oldStatusId = cur.fetchone()

        if oldStatusId[0] == 2:
            db.execute('update applications set statusId=? where applicationId=?', (statusId[0], applicationId[0],))
            db.commit()
        db.close()
        return '{"status":"OK"}' 

    except KeyError:
        print("[ ERROR ] Invalid data", sys.stderr)
        return '{"status":"ERROR"}'

#set a max events list
#also return picture
@app.route('/getEvents', methods=['GET'])
def getEvents():
    try:
        db = get_db()
        cur = db.cursor()
     
        query = 'select name, description, date, location, organisationId from Events'
        events = []
        for row in db.execute(query):
            cur.execute('select email, name from Organisations where organisationId = ?', (row[4],))
            curRow = cur.fetchone()
            evt = {
                "name" : row[0],
                "description" : row[1],
                "date" : row[2],
                "location": row[3],
                "organisation": curRow[1],
                "organisationEmail": curRow[0]
            }
            events.append(evt)
        
        temp = {
                "events": events,
                "status": "OK"
        }
        res = jsonify(temp)
        print(res)
        return res
    except:
        print("[ ERROR ]Error at getting events")
        return '{"status":"ERROR"}'

@app.route('/getEventsOrganization', methods=['POST'])
def getEventsOrganization():
    request_dict = request.get_json()
    if request_dict == None:
        print("[ ERROR ] Invalid data", sys.stderr)
        return '{"status":"ERROR"}'

    organization = request_dict['email']
    if organization == "":
        print("[ ERROR ] Invalid data", sys.stderr)
        return '{"status":"ERROR"}'
    try:
        db = get_db()
        cur = db.cursor()
        
        query1 = 'select organisationId from Organisations where email=\'' + organization + '\''
        
        cur.execute(query1)
        
        org = cur.fetchone()
        
        if org[0] == None:
            return '{"status":"ERROR"}'
        
        
        events = []
        for row in db.execute('select name, description, date, location from Events where organisationId = ?', (org[0],)):
            cur.execute('select name from Organisations where organisationId = ?', (org[0],))
            curRow = cur.fetchone()
            evt = {
                "name" : row[0],
                "description" : row[1],
                "date" : row[2],
                "location": row[3],
                "organisation": curRow[0],
                "organisationEmail": organization
            }
            events.append(evt)
        
        temp = {
                "events": events,
                "status": "OK"
        }
        res = jsonify(temp)
        print(res)
        return res
    except KeyError:
        print("[ ERROR ] Error at getting events")
        return '{"status":"ERROR"}'

#for users
#gets email of a user as a parameter
@app.route('/getUserApplications', methods=['POST'])
def getUserApplications():
    request_dict = request.get_json()
    if request_dict == None:
        print("[ ERROR ] Invalid data", sys.stderr)
        return '{"status":"ERROR"}'
    try:
        email = request_dict["email"]

        if email == "":
            print("[ ERROR ] Invalid email", sys.stderr)
            return '{"status":"ERROR"}'

        db = get_db()
        cur = db.cursor()

        cur.execute('select userId from Users where email=?',(email,))
        userId = cur.fetchone()

        if userId == None:
            print("[ ERROR ] No such user exists", sys.stderr)
            return '{"status":"ERROR"}'

        applications = []
        for app in db.execute('select eventId, statusId from Applications where userId=?', (userId[0],)):
            eventId = app[0]
            statusId = app[1]

            cur.execute('select name, description from status where statusId=?', (statusId,))
            statusType = cur.fetchone()

            cur.execute('select name, description, date, location, organisationId from Events where eventId=?', (eventId,))
            eventData = cur.fetchone()

            eventName = eventData[0]
            eventDescription = eventData[1]
            eventDate = eventData[2]
            eventLocation = eventData[3]
            organisationId = eventData[4]

            cur.execute('select name, email, description, rating from Organisations where organisationId=?', (organisationId,))
            orgData = cur.fetchone()

            organizationData = {
                "name" : orgData[0],
                "email" : orgData[1],
                "description" : orgData[2],
                "rating" : orgData[3]
            }

            eventData = {
                "name" : eventName,
                "date" : eventDate,
                "description" : eventDescription,
                "location" : eventLocation,
                "organization" : organizationData
            }

            appElement = {
                "event" : eventData,
                "appStatus" : statusType[0]
            }

            applications.append(appElement)
            print(appElement)
        
        result = {
            "applications" : applications,
            "status" : "OK"
        }
        res = jsonify(result)
        print(res, sys.stderr)
        db.close()
        return res


    except KeyError:
        print("Invalid data", sys.stderr)
        return '{"status":"ERROR"}'

#for organisation
#gets name of event and type of status as params
@app.route('/getUsersForEvent', methods=['POST'])
def getUsersForEvent():
    request_dict = request.get_json()
    if request_dict == None:
        print("[ ERROR ] Invalid json", sys.stderr)
        return '{"status":"ERROR"}'
    
    try:
        eventName = request_dict['name']
        statusType = request_dict['status']

        #TO-DO description can be null
        if eventName == "" or statusType == "":
            print("[ ERROR ] Invalid data", sys.stderr)
            return '{"status":"ERROR"}'
        
        db = get_db()
        cur = db.cursor()

        query = 'select eventid from Events where name=\'' + eventName + '\''
        cur.execute(query)
        eventId = cur.fetchone()
        
        if eventId == None:
            print("No such event exists", sys.stderr)
            return '{"status":"ERROR"}'

        
        if statusType == "*":
            userIds = []
            for row2 in db.execute('select userId from Applications where eventId=?',(eventId[0],)):
                userIds.append(row2[0])
            
            users=[]
            for userId in userIds:
                #query2 = 'select firstname, lastname, email, birthdate, rating, description from Users where userid=3' 
                #query3 = 'select statusId from Applications where userId=?' + userId
                cur.execute('select statusId from Applications where userId=? and eventId=?', (userId,eventId[0],))
                tempStatusId = cur.fetchone()
                
                cur.execute('select name from Status where statusId=?', (tempStatusId[0],))
                tempStatusType = cur.fetchone()
                

                cur.execute('select firstname, lastname, email, birthdate, rating, description from Users where userid=%s' %userId)
                row3 = cur.fetchone()
                tmp = {
                    "firstName" : row3[0],
                    "lastName" : row3[1],
                    "email" : row3[2],
                    "birthdate" : row3[3],
                    "rating" : row3[4],
                    "description" : row3[5],
                    "appStatus" : tempStatusType[0]
                }
                users.append(tmp)
            result = {
                "users" : users,
                "status" : "OK"
            }
            res = jsonify(result)
            print(res, sys.stderr)
            return res

        cur.execute('select statusId from Status where name=?', (statusType,))
        statusId = cur.fetchone()
       
        if statusId == None:
            print("No such status exists", sys.stderr)
            return '{"status":"ERROR"}'

        userIds = []
        
        #query1 = 'select userId from applications where eventId=\'' + eventId + '\''
        #print(query1)
        
        
        for row2 in db.execute('select userId from Applications where eventId=? and statusId=?',(eventId[0], statusId[0],)):
            userIds.append(row2[0])
            
        users=[]
        for userId in userIds:
            #query2 = 'select firstname, lastname, email, birthdate, rating, description from Users where userid=3' 
            #query3 = 'select statusId from Applications where userId=?' + userId
            for row3 in db.execute('select firstname, lastname, email, birthdate, rating, description from Users where userid=%s' %userId):
                tmp = {
                    "firstName" : row3[0],
                    "lastName" : row3[1],
                    "email" : row3[2],
                    "birthdate" : row3[3],
                    "rating" : row3[4],
                    "description" : row3[5],
                    "status" : statusType
                }
                print(tmp, sys.stderr)
                users.append(tmp)
        result = {
            "users" : users,
            "status" : "OK"
        }
        res = jsonify(result)
        print(res, sys.stderr)
        return res
    except KeyError:
        print("Invalid data", sys.stderr)
        return '{"status":"ERROR"}'

@app.route('/uploadFile', methods=['POST'])
def uploadFile():
    request_dict = request.get_json()
    if request_dict == None:
        print("[ ERROR ] Invalid json", sys.stderr)
        return '{"status":"ERROR"}'

    try:
        values = [request_dict['type'],
        request_dict['extension'],
        request_dict['email']]

        fileblob = request_dict['file']

        if fileblob == "":
            print("[ ERROR ] Invalid file", sys.stderr)
            return '{"status":"ERROR"}' 

        for element in values:
            if element == "":
                print("[ ERROR ] Invalid val", sys.stderr)
                return '{"status":"ERROR"}'

        #profile picture
        if values[0] == "profile":
            
            if (values[1] != "jpg" and values[1] != "png"):
                print("[ ERROR ] Invalid file extension", sys.stderr)
                return '{"status":"ERROR"}'

            #database processing
            try:
                
                db = get_db()
                cur = db.cursor()
                query = 'select userId from Users where email=\'' + values[2] + '\''
                
                cur.execute(query)
                #db.commit()
                row = cur.fetchone()

                userId = row[0]

                query2 = 'select fileId from UserPicture where userId=\'' + str(userId) + '\''
                
                cur.execute(query2)
                #db.commit()
                row = cur.fetchone()
                if row != None:
                    fileId = str(row[0])
                    query3 = 'delete from File where Id=\'' + fileId + '\''
                    cur.execute(query3)
                    #db.commit()

                    query4 = 'delete from UserPicture where fileId=\'' + fileId + '\''
                    cur.execute(query4)
                    #db.commit()

                filename = "picture." + values[2] + "." + values[1]

                db.execute('insert into File (name, file, type) values (?,?,?)', (filename, fileblob, values[1]))

                db.commit()

                query5 = 'select id from File where name=\'' + filename + '\''
                cur.execute(query5)
                #db.commit()
                row = cur.fetchone()

                fileId = row[0]

                db.execute('insert into UserPicture (userId, fileId) values (?,?)', (userId, fileId))
                db.commit()

                db.close()
                return '{"status":"OK"}' 
              
            except KeyError:
                print("Database error", sys.stderr)
                return '{"status":"ERROR"}'

        #user CV
        elif values[0] == "cv":
            user = request_dict['email']

            if user == "":
                print("[ ERROR ] Invalid user name", sys.stderr)
                return '{"status":"ERROR"}'

            if values[1] != "pdf":
                print("[ ERROR ] Invalid file extension", sys.stderr)
                return '{"status":"ERROR"}'

            try:
                db = get_db()
                cur = db.cursor()
                query = 'select userId from Users where email=\'' + values[2] + '\''
                
                cur.execute(query)
                #db.commit()
                row = cur.fetchone()

                userId = row[0]

                query2 = 'select fileId from UserCV where userId=\'' + str(userId) + '\''
                
                cur.execute(query2)
                #db.commit()
                row = cur.fetchone()
                if row != None:
                    fileId = str(row[0])
                    query3 = 'delete from File where Id=\'' + fileId + '\''
                    cur.execute(query3)
                    #db.commit()

                    query4 = 'delete from UserCV where fileId=\'' + fileId + '\''
                    cur.execute(query4)
                    #db.commit()

                filename = "cv." + values[2] + "." + values[1]

                db.execute('insert into File (name, file, type) values (?,?,?)', (filename, fileblob, values[1]))

                db.commit()

                query5 = 'select id from File where name=\'' + filename + '\''
                cur.execute(query5)
                #db.commit()
                row = cur.fetchone()

                fileId = row[0]

                db.execute('insert into UserCV (userId, fileId) values (?,?)', (userId, fileId))
                db.commit()

                db.close()
                return '{"status":"OK"}' 

                
            except KeyError:
                print("Database error", sys.stderr)
                return '{"status":"ERROR"}'


        #cover for event
        elif values[0] == "cover":
            event = request_dict['event']

            if event == "":
                print("[ ERROR ] Invalid event name", sys.stderr)
                return '{"status":"ERROR"}'

            if values[2] == "":
                print("[ ERROR ] Invalid user name", sys.stderr)
                return '{"status":"ERROR"}'

            #database processing
            try:
                db = get_db()
                cur = db.cursor()
                
                query = 'select organisationId from Organisations where email=\'' + values[2] + '\''
                
                cur.execute(query)
                row = cur.fetchone()

                orgId = row[0]
                query1 = 'select eventId from Events where organisationId =\'' + str(orgId) + '\' and name=\'' + event + '\''
                cur.execute(query1)
                row = cur.fetchone()

                eventId = row[0]
                
                if eventId == None:
                    print("[ ERROR ] Event does not exist", sys.stderr)
                    return '{"status":"ERROR"}'


                query2 = 'select fileId from EventCover where eventId=\'' + str(eventId) + '\''
                cur.execute(query2)

                row = cur.fetchone()

                if row != None:
                    fileId = str(row[0])
                    query3 = 'delete from File where Id=\'' + fileId + '\''
                    db.execute(query3)
                    db.commit()


                    query4 = 'delete from EventCover where fileId=\'' + fileId + '\''
                    db.execute(query4)
                    db.commit()

                filename = "cover." + event + "." + values[2] + "." + values[1]

                db.execute('insert into File (name, file, type) values (?,?,?)', (filename, fileblob, values[1]))

                db.commit()

                query5 = 'select id from File where name=\'' + filename + '\''
                cur.execute(query5)
                #db.commit()
                row = cur.fetchone()

                fileId = row[0]

                db.execute('insert into EventCover (eventId, fileId) values (?,?)', (eventId, fileId))
                db.commit()

                db.close()
                return '{"status":"OK"}'

            except KeyError:
                print("Invalid data", sys.stderr)
                return '{"status":"ERROR"}'

        #invlaid data
        else:
            print("[ ERROR ] Invalid file type", sys.stderr)
            return '{"status":"ERROR"}'

        
    except KeyError:
        print("Invalid data", sys.stderr)
        return '{"status":"ERROR"}'


    

@app.route('/downloadFile', methods=['GET'])
def downloadFile():
    request_dict = request.get_json()
    
    if request_dict == None:
        print("[ ERROR ] Invalid json", sys.stderr)
        return '{"status":"ERROR"}'

    email = request_dict["email"]
    requested = request_dict["type"]

    if (email == "" or requested == ""):
        print("[ ERROR ] Invalid requested data", sys.stderr)
        return '{"status":"ERROR"}'

    try:
        db = get_db()
        cur = db.cursor()

        if requested == "picture":
            query = 'select userId from Users where email=\'' + email + '\''
            
            cur.execute(query)
            row = cur.fetchone()

            if row == None:
                print("[ ERROR ] No such user exist", sys.stderr)
                return '{"status":"ERROR"}'

            userId = row[0]

            query1 = 'select fileId from UserPicture where userId=\'' + str(userId) + '\''
            cur.execute(query1)
            row = cur.fetchone()

            if row == None:
                print("[ ERROR ] No such file exists", sys.stderr)
                return '{"status":"ERROR"}'

            fileId = row[0]

        elif requested == "cover":
            event = request_dict["event"]
            
            if event == "":
                print("[ ERROR ] No such event exists", sys.stderr)
                return '{"status":"ERROR"}'

            query0 = 'select organisationId from Organisations where email=\'' + email + '\''
            cur.execute(query0)
            row = cur.fetchone()

            if row == None:
                print("[ ERROR ] No such organisation exists", sys.stderr)
                return '{"status":"ERROR"}'

            organisationId = row[0]

            query = 'select eventId from Events where name=\'' + event + '\' and organisationId=\'' + str(organisationId) + '\''
            
            cur.execute(query)
            row = cur.fetchone()

            if row == None:
                print("[ ERROR ] No such event exist", sys.stderr)
                return '{"status":"ERROR"}'

            eventId = row[0]


            query2 = 'select fileId from EventCover where eventId=\'' + str(eventId) + '\''
            cur.execute(query2)
            row = cur.fetchone()

            if row == None:
                print("[ ERROR ] No such file exists", sys.stderr)
                return '{"status":"ERROR"}'

            fileId = row[0]
            query3 = 'select file, type from File where id=\'' + str(fileId) + '\''
            cur.execute(query3)
            row = cur.fetchone()

            data = row[0]
            extension = row[1]

            result = {
                "event" : event,
                "extension": extension,
                "type" : requested,
                "data" : data,
                "status" : "OK"
            }
            res = jsonify(result)
            return res

        elif requested == "cv":
            query = 'select userId from Users where email=\'' + email + '\''
            
            cur.execute(query)
            row = cur.fetchone()

            if row == None:
                print("[ ERROR ] No such user exists", sys.stderr)
                return '{"status":"ERROR"}'

            userId = row[0]

            query1 = 'select fileId from UserCV where userId=\'' + str(userId) + '\''
            cur.execute(query1)
            row = cur.fetchone()

            if row == None:
                print("[ ERROR ] No such file exists", sys.stderr)
                return '{"status":"ERROR"}'

            fileId = row[0]

        else:
            print("Invalid requested data", sys.stderr)
            return '{"status":"ERROR"}'

        query2 = 'select file, type from File where id=\'' + str(fileId) + '\''
        cur.execute(query2)
        row = cur.fetchone()

        data = row[0]
        extension = row[1]

        result = {
                "extension": extension,
                "type" : requested,
                "data" : data,
                "status" : "OK"
        }
        res = jsonify(result)
        print(res)
        return res

    except KeyError:
        print("Invalid data", sys.stderr)
        return '{"status":"ERROR"}'
    

if __name__ == '__main__':
    
    try:
        if sys.argv[1] == 'run':
            print('[ INFO ] Running app...')
            app.run()
        elif sys.argv[1] == 'init':
            print('[ INFO ] Database init...')
            with app.app_context():
                init_db()
    except IndexError:
        print("[ ERROR ] Usage: python ./scriptname init/run")
