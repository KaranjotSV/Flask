from flask import Flask, request, jsonify
from mongoengine import *
from flask_sqlalchemy import *
import MySQLdb
import json

project_dir = os.path.dirname(os.path.abspath('test'))
database_file = 'mysql://vilkhu:root@localhost/{}'.format(os.path.join(project_dir, "test.db"))

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
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)

# MySQL
class StudentMySQL(db.Model):
    ID = db.Column(db.String(80), unique=True, nullable=False, primary_key = True)
    Name = db.Column(db.String(200), unique=False, nullable=False)
    LastName = db.Column(db.String(200), unique=False, nullable=False)
    Year = db.Column(db.String(20), unique=False, nullable=False)
    Major = db.Column(db.String(100), unique=False, nullable=False)

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
            post_sql = StudentMySQL(ID = JSON['id'], Name = JSON['name'], LastName = JSON['lname'], Year = JSON['year'], Major = JSON['major'])
            ID = JSON['id']
            post_mongo.save()           # for Mongo
            db.session.add(post_sql)    # for MySQL
            db.session.commit()
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
            studentmysql = StudentMySQL.query.filter_by(ID = id)
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

            studentmysql.Name = name                                                          # for MySQL
            studentmysql.LastName = lastname
            studentmysql.Year = year
            studentmysql.Major = major

            db.session.commit()


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

            studentmysql = StudentMySQL.query.filter_by(ID = id) # for MySQL
            db.session.delete(studentmysql)
            db.session.commit()

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
