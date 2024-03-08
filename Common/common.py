import pymysql

class DBConnector(object):
    def __init__(self):
        self.host = "fininfocom-database.cte4444icnot.ap-southeast-2.rds.amazonaws.com"
        self.user = "admin"
        self.password = "_AWS_123456"
        self.db = "fininfo_employees_db"

    #create a new connection
    def createDBConnection(self):
        print('--createDBConnection')
        try:
            return pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                db=self.db
            )
        except Exception as e:
            print(f'ERROR:: createDBConnection function failed | Exception: {e}')
    

class DBConnection(object):
    connection = None

    @classmethod
    def getDBConnection(cls, new=False):
        print('--getDBConnection')
        if new or not cls.connection:
            cls.connection = DBConnector().createDBConnection()
        return cls.connection
    
    @classmethod
    def getQuery(cls, query, params=None):
        print('--getQuery')
        try:
            connection = cls.getDBConnection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            if params:
                cursor.execute(query, (params))
            else:
                cursor.execute(query)

            result = cursor.fetchone()
            connection.commit()
            cursor.close()
            return result
        except Exception as e:
            print(f'Exception occured while fetching getQuery | Exception:: {e}')
            raise Exception('Exception occured while getQuery')
        
    @classmethod
    def insertUpdateQuery(cls, query, params):
        print("--insertUpdateQuery")
        try:
            connection = cls.getDBConnection()
            cursor = connection.cursor()
            cursor.execute(query, (params))
            connection.commit()
            last_row_id = cursor.lastrowid
            print("Inserted ID:", last_row_id)
            
            success_response = {
                "message": "employee created successfully",
                "regid": last_row_id, 
                "success": True 
            }
            cursor.close()
            return success_response
            
        except pymysql.IntegrityError as e:
            # Handle duplicate key error
            if e.args[0] == 1062:
                response = { 
                    "message": "employe already exist",
                    "success": False
                }
                return response
            # Handle other integrity error
            else:
                return { 
                    "message": "Invalid body request",
                    "success": False
                }
            
        except Exception as e:
            # Handle other exceptions
            print(f'Exception occured while insertUpdateQuery:: {e}')
            return { 
                "message": "Employee creation failed",
                "success": False
            }
            
    @classmethod
    def executeQuery(cls, query, params=None):
        print("--executeQuery")
        try:
            connection = cls.getDBConnection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            if params:
                cursor.execute(query, (params))
            else:
                cursor.execute(query)
            #print("query :: ", cursor._last_executed)
            result = cursor.fetchall()
            connection.commit()
            cursor.close()
            return result
        except Exception as ex:
            print(f"Exception occured while executeQuery | Exception: {ex}")
            raise Exception(f"Error occured while fetching records{ex}")
            
    @classmethod
    def deleteQuery(cls, query, params=None):
        print("--deleteQuery")
        try:
            connection = cls.getDBConnection()
            cursor = connection.cursor()
            if params:
                cursor.execute(query, (params))
            else:
                cursor.execute(query)
                
            connection.commit()
            cursor.close()
            return True
        except Exception as ex:
            print(f"Exception occured while deleteQuery | Exception: {ex}")
            raise Exception(f"Error while deleting record{ex}")


#schemas
from marshmallow import Schema, fields, validate

class ProjectSchema(Schema):
    title = fields.String(required=True)
    description = fields.String(required=True)

class QualificationSchema(Schema):
    qualificationName = fields.String(required=True)
    fromDate = fields.String(required=True)
    toDate = fields.String(required=True)
    percentage = fields.Float(validate=validate.Range(min=0, max=100), required=True)

class WorkExperienceSchema(Schema):
    companyName = fields.String(required=True)
    fromDate = fields.String(required=True)
    toDate = fields.String(required=True)
    address = fields.String(required=True)

class AddressDetailsSchema(Schema):
    hno = fields.String(required=True)
    street = fields.String(required=True)
    city = fields.String(required=True)
    state = fields.String(required=True)

class EmployeeSchema(Schema):
    id = fields.Integer(required=False)
    name = fields.String(required=True)
    email = fields.Email(required=True)
    age = fields.Integer(validate=validate.Range(min=0))
    gender = fields.String()
    phoneNo = fields.String()
    addressDetails = fields.Nested(AddressDetailsSchema, required=True)
    workExperience = fields.List(fields.Nested(WorkExperienceSchema), required=True)
    qualifications = fields.List(fields.Nested(QualificationSchema), required=True)
    projects = fields.List(fields.Nested(ProjectSchema), required=True)
    photo = fields.String()


class EmployeeID(Schema):
    empID = fields.Integer(required=True)