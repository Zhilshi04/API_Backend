from pymongo.mongo_client import MongoClient
from flask import request,Flask,jsonify
from flask_jwt_extended import JWTManager,jwt_required,create_access_token
from flask_basicauth import BasicAuth

app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = 'username'
app.config['BASIC_AUTH_PASSWORD'] = 'password'


# app.config['JWT_SECRET_KEY'] = 'pannet6483'
basic_auth = BasicAuth(app)
jwt = JWTManager(app)

# uri = "mongodb+srv://mongo:mongo@cluster0.2owdljr.mongodb.net/?retryWrites=true&w=majority"
uri = "mongodb+srv://pannet6483:TFQx7iQeJsx4DswO@cluster0.4x4ccde.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri)
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    # print("Pinged your deployment. You successfully connected to MongoDB!")
    db = client["students"]
    collection = db["std_info"]
    @app.route("/")
    def Greet():
        return "<p> Welcome to Student Management API </p>"

    # @app.route("/login",methods = ["POST"])
    # def login():
    #     data = request.get_json()
    #     username = data.get("username",None)
    #     password = data.get("password",None)

    #     if(username == 'user' and password == 'pass'):
    #         access_token = create_access_token(identity = username)
    #         return jsonify(access_token = access_token),200
    #     else:
    #         return jsonify({"error":"Invalid credentials"}),404

    @app.route("/students/" ,  methods = ["GET"])
    @basic_auth.required
    def GetAllStudents():
        all_students = list(collection.find())
        return jsonify(all_students)

    @app.route("/students/<student_id>" , methods = ["GET"])
    @basic_auth.required
    def GetStudents(student_id):
        # students = []
        all_students = list(collection.find())
        # Use a list comprehension to filter students based on the given student_id
        student = next((b for b in all_students if b["_id"] == student_id), None)

        if student:
            return jsonify(student)
        else:
            return jsonify({"error": "Student not found"}), 404
        
    @app.route("/students/",methods=["POST"])
    @basic_auth.required
    def create_student():
        data = request.get_json()
        print(data)
        new_student = {
            "_id":data["_id"],
            "fullname":data["fullname"],
            "gpa":data["gpa"],
            "major":data["major"]
        }
        # books.append(new_book)
        try:
            collection.insert_one(new_student)
        except Exception as e:
                print(e)
                return jsonify({"error":"Cannot create new student"}),500
        return jsonify(new_student),201
        
    @app.route("/students/<student_id>" , methods = ["DELETE"])
    @basic_auth.required 
    def delete_student(student_id):
        # global books
        # books = ((b for b in books if b["id"] != book_id))
        try:
            collection.delete_one({"_id": student_id})
            # print(f"Record with student id {student_id} deleted successfully.")
            return jsonify({"message":"Student deleted successfully"}),200
        except Exception as e:
            print(e)
            return jsonify({"error":"Student not found"}),404

    @app.route("/students/<student_id>", methods = ["PUT"])
    @basic_auth.required
    def update_student(student_id):
        all_students = list(collection.find())
        print(all_students)
        student = next((b for b in all_students if b["_id"] == student_id), None)
        print(student)
        if student:
            try:
                data = request.get_json()
                # Update the student information
                collection.update_one({"_id": student_id}, {"$set": data})
                print(f"Record with student id {student_id} updated successfully.")
                # Retrieve the updated student
                updated_student = collection.find_one({"_id": student_id})
                return jsonify(updated_student),202
            except Exception as e:
                print(e)
                return jsonify({"error": "Failed to update student"}), 500  # Internal Server Error
        else:
            return jsonify({"error": "Student not found"}), 404
    if __name__ == "__main__":
        app.run(host="0.0.0.0" , port=5000 , debug=True)

except Exception as e:
    print(e)
finally:
    client.close()
