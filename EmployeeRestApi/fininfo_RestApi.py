import json
from common import DBConnection as db_connection
from marshmallow import ValidationError
from common import EmployeeSchema, EmployeeID
import pymysql

INSERT_EMPLOYEE_INFO = """
    INSERT INTO fininfo_employees_db.employees (name, email, age, gender, phoneNo, addressDetails, workExperience, qualifications, projects, photo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""
UPDATE_EMPLOYEE_INFO = """
    UPDATE fininfo_employees_db.employees
    SET name=%s, email=%s, age=%s, gender=%s, phoneNo=%s, addressDetails=%s, workExperience=%s, qualifications=%s, projects=%s, photo=%s 
    WHERE id=%s
"""
GET_EMPLOYEE_INFO = "SELECT * FROM fininfo_employees_db.employees WHERE id=%s"
LIST_ALL_EMPLOYEES = "SELECT * FROM fininfo_employees_db.employees"
DELETE_EMPLOYEE = "DELETE FROM fininfo_employees_db.employees WHERE id=%s"


#sample json
payload = {
    "id": 4,
    "name": "Kaveri medhari",
    "email": "xyz11313@gmail.com",
    "age": 23,
    "gender": "female",
    "phoneNo": "7995032168",
    "addressDetails": {
        "hno": "123",
        "street": "xyz",
        "city": "xyz",
        "state": "xyz"
    },
    "workExperience": [
        {
            "companyName": "xyz",
            "fromDate": "20-05-2019",
            "toDate": "20-09-2021",
            "address": "xyz"
        }
    ],
    "qualifications": [
        {
            "qualificationName": "ssc",
            "fromDate": "20-05-2012",
            "toDate": "20-05-2013",
            "percentage": 85
        }
    ],
    "projects": [
        {
            "title": "xyz",
            "description": "description of the project"
        }
    ],
    "photo": ""
}


#Update employee record in the database
def updateEmployeeInfo(payload):
    print('--updateEmployee')
    try:
        empID = payload.get('id')
        
        # Convert the dictionary values to JSON strings before insertion
        addressDetailsJson = json.dumps(payload["addressDetails"])
        workExperienceJson = json.dumps(payload["workExperience"])
        qualificationsJson = json.dumps(payload["qualifications"])
        projectsJson = json.dumps(payload["projects"])
        
        values = (
            payload["name"],
            payload["email"],
            payload["age"],
            payload["gender"],
            payload["phoneNo"],
            addressDetailsJson,
            workExperienceJson,
            qualificationsJson,
            projectsJson,
            payload["photo"],
            empID
            
        )
        print('updating employee record...')
        db_connection.insertUpdateQuery(UPDATE_EMPLOYEE_INFO, values)
        print('updated employee record...')
        return {
            "statusCode": 200,
            "body": {
                "message": "Employee details updated successfully",
                "success": True
            }
        }
        
    except Exception as e:
        # Handle other exceptions
        print(f"ERROR:: Exception occured while adding the employee| Exception: {e}")
        return {
            "statusCode": 500,
            "body": { 
                "message": "Employee details updation failed",
                "success": False
            }
        }

#Delete Employee record from database.
def deleteEmployee(empID):
    print('--deleteEmployee')
    try:
        print('deleting employee record')
        db_connection.deleteQuery(DELETE_EMPLOYEE, empID)
        print('deleted employee record')
        return {
            "statusCode": 200,
            "message": "Employee deleted successfully",
            "regid": empID, 
            "success": True 
        }
    except Exception as e:
        return {
            "statusCode": 200,
            "message": "Employee deletion failed",
            "regid": empID, 
            "success": False 
        }

def getEmployeeById(empID):
    print("--getEmployee")
    try:
        print('fetching employee record')
        employeeData = db_connection.getQuery(GET_EMPLOYEE_INFO, empID)
        print(f'employee Data: {employeeData}')
        
        response = {
            "statusCode": 200,
            "body": employeeData
        }
        if employeeData:
            response["message"] = "Employee details found"
        else:
            response["message"] = "Employee details not found with this regid"
        return response
        
    except Exception as e:
        print(f"ERROR:: Exception occured while fetching employe | Exception: {e}")
        return {
            "statusCode": 500,
            "message": "Employee details not found with this regid",
            "success": False 
        }

#List all employees
def getEmployeesList():
    print('--getEmployeesList')
    try:
        print('fetching employees records')
        employesData = db_connection.executeQuery(LIST_ALL_EMPLOYEES)
        print(f'employesData: {employesData}')
        return {
            "statusCode": 200,
            "message": "Employees details found",
            "body": employesData
        }
    except Exception as e:
        print(f"ERROR:: Exception occured while fetching employees | Exception: {e}")
        return {
            "statusCode": 500,
            "message": "Employees details not found",
            "success": False
        }
        
#Create a employee record in the database
def createEmployee(request):
    print('--addEmployee')
    try:
        #validate payload
        payload = EmployeeSchema().load(request)
        
        # Convert the dictionary values to JSON strings before insertion
        addressDetailsJson = json.dumps(payload["addressDetails"])
        workExperienceJson = json.dumps(payload["workExperience"])
        qualificationsJson = json.dumps(payload["qualifications"])
        projectsJson = json.dumps(payload["projects"])
        
        values = (
            payload["name"],
            payload["email"],
            payload["age"],
            payload["gender"],
            payload["phoneNo"],
            addressDetailsJson,
            workExperienceJson,
            qualificationsJson,
            projectsJson,
            payload["photo"]
        )
        print('inserting employee record...')
        response = db_connection.insertUpdateQuery(INSERT_EMPLOYEE_INFO, values)
        print('inserted employee record')
        return {
            "statusCode": 200,
            "body": response
        }
        
    except Exception as e:
        # Handle other exceptions
        print(f"ERROR:: Exception occured while adding employee | Exception: {e}")
        return {
            "statusCode": 500,
            "body": { 
                "message": "Invalid body request",
                "success": False
            }
        }

#Handle API Gateway response
def wrapResponse(code, body):
    headers = {
        "Access-Control-Allow-Headers": "Content-Type,Authorization,X-Amz-Date,X-Api-Key,X-Amz-Security-Token",
        "Access-Control-Allow-Methods": "DELETE,GET,HEAD,OPTIONS,PATCH,POST,PUT",
        "Access-Control-Allow-Origin": "*",
    }
    return {
        "headers": headers,
        "statusCode": code,
        "body": json.dumps(body)
    }
    
    
allowedMethods = ['GET', 'POST', 'PUT', 'DELETE']

def lambda_handler_local_test(event, context):
    print("adding employee")
    result = addEmployee(payload)
    print("result", result)
    print("successfully added employee")
    
    
def lambda_handler(event, context):
    print(f"lambda_handler event:: {event}")
    response = {}
    try:
        #check if http method in allowed methods
        method = event["httpMethod"]
        if method not in allowedMethods:
            raise Exception("Operation not supported")
            
        
        if method == 'POST':
            request = json.loads(event["body"])
            print(f"request:: {request}")
    
            #validate payload
            payload = EmployeeSchema().load(request)
            response = createEmployee(payload)
            
        elif method == "PUT":
            request = json.loads(event["body"])
            print(f"request:: {request}")
    
            #validate payload
            payload = EmployeeSchema().load(request)
            response = updateEmployeeInfo(payload)
            
        elif method == "GET":
            body = event["body"]
            if body:
                request = json.loads(event["body"])
                print(f"request:: {request}")
                
                #validate payload
                payload = EmployeeID().load(request)
                empID = request.get('empID')
                response = getEmployeeById(empID)
            else:
                response = getEmployeesList()
            print(f'response:: {response}')
            
        elif method == "DELETE":
            request = json.loads(event["body"])
            print(f"request:: {request}")
            
            #validate payload
            payload = EmployeeID().load(request)
            empID = request.get('empID')
            response = deleteEmployee(empID)
        
        return wrapResponse(200, response)
        
    except Exception as e:
        print(f'ERROR: {e}')
        response = {
            "statusCode": 400,
            "message": "Internal server error",
            "error": str(e),
            "success": False
        }
        return wrapResponse(500, response)

