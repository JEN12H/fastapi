from pydantic import BaseModel,EmailStr,AnyUrl,Field ,model_validator # FELDS ARE USED FOR CUSTOM DATA VALIDATION 
from typing import List,Dict,Optional,Annotated
# DEFINE OUR SCHEMA USING CLASS( ALL MENTIONED FIELDS ARE REQUIRED)
class Patient(BaseModel):
    Name : Annotated[str , Field(max_length= 50,title='Name of Patient',description = 'Give THe name of patient in less than 50 letters',examples=['Jenish','Name'] )]
    Age : int
    Linked_url : AnyUrl
    Email :EmailStr
    Weight : float = Field(gt= 0,lt = 120)
    Married : Annotated[bool,Field(default=None,description='Is the patient married or not ')]
    Allergies : Annotated[Optional[List[str]], Field(default = None, max_length=5)]
    Contact_details : Dict[str,str] # KEY,VALUE
    @model_validator(mode='after')
    def validate_emergency_contact(cls, model):
        if model.Age >= 60 and 'emergency' not in model.Contact_details:
            raise ValueError("PLEASE PROVIDE EMERGENCY CONTACT NUMBER")
        return model
    
# PASSING A PYDANTIC OBJECT TO THE FUNCTION
def insert_patient(patient : Patient):
    print(patient.Name)
    print(patient.Age)
    print(patient.Email)
    print(patient.Linked_url)
    print(patient.Weight)
    print(patient.Married)
    print(patient.Allergies)
    print(patient.Contact_details)
    
    print("Inserted")
    
patient_info = {"Name":'nitish','Age': 67 ,'Linked_url':'http:linkedin.com/1234','Email':'xyz@hotmail.com','Weight':70,"Married":1,"Allergies":["Dust","Milk"],"Contact_details":{"email":"XYZ@gmial.com","Phone":"084045903",'emergency':'209829829'}}
# OBJECT OF A CLASS - UNPACKING THE DICTIONARY
patient1 = Patient(**patient_info)
# USE THE RETURNED OBJECT
insert_patient(patient1)
