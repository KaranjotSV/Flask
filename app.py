from flask import Flask, request, jsonify
from mongoengine import *
import json

def checkPrime(n):
    if n == 2 or n == 3:
        return("a prime number")

    elif ((n - 1) % 6) == 0 or ((n + 1) % 6) == 0:
        return("a prime number")

    else:
        return("not a prime number")

# Mongo
connect('test', host = 'localhost', port=27017)

class StudentMongo(Document):
    ID = StringField(required=True, max_length=50, unique = True)
    Name = StringField(required=True, max_length=200)
    LastName = StringField(required=True)
    Year = StringField(required=True, max_length=50)
    Major = StringField(required = True, max_length=50)

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def get_document():

    if request.method == 'GET':

        try:
            students_dict = {}
            students = StudentMongo.objects()
            for student in students:
                students_dict[student.ID] = {"Name" : student.Name, "LastName" : student.LastName, "Year" : student.Year, "Major" : student.Major}

            return jsonify(students_dict)
        except:
            return("Something went wrong!")


@app.route('/create', methods = ['POST'])
def create():
    id_dict = {}
    try:
        if request.method == 'POST':
            JSON = request.json
            post_mongo = StudentMongo(ID = JSON['id'], Name = JSON['name'], LastName = JSON['lname'], Year = JSON['year'], Major = JSON['major'])
            ID = JSON['id']
            post_mongo.save()           # for Mongo
            id_dict['id'] = ID
            return jsonify(id_dict)

        else:
            return("Send a POST request!")
    except NotUniqueError:
        return("ID already exists!")

@app.route('/update', methods = ['PUT'])
def update():

    if request.method == 'PUT':
        JSON = request.json
        id = JSON['id']
        try:
            studentmongo = StudentMongo.objects(ID = id).get()
            try:
                name = JSON['name']
            except:
                name = studentmongo.Name

            try:
                lastname = JSON['lname']
            except:
                lastname = studentmongo.LastName

            try:
                year = JSON['year']
            except:
                year = studentmongo.Year

            try:
                major = JSON['major']
            except:
                major = studentmongo.Major

            studentmongo.update(Name = name, LastName = lastname, Year = year, Major = major) # for Mongo
	
            return("Update Succesful")
        except DoesNotExist:
            return("ID not found")

@app.route('/delete', methods = ['DELETE'])
def delete():
    if request.method == 'DELETE':
        JSON = request.json
        id = JSON['id']
        try:
            studentmongo = StudentMongo.objects(ID = id).get() # for Mongo
            studentmongo.delete()

            return("Document deleted")
        except DoesNotExist:
            return("ID not found")

@app.route('/detect_prime', methods = ['POST'])
def detect():
    check = {}
    if request.method == 'POST':
        JSON = request.json
        num = int(JSON['number'])
        checkp = checkPrime(num)
        check[num] = checkp
        return jsonify(check)
    else:
        return("Send a POST request")

if __name__ == '__main__':
	app.run(port = 5500)
