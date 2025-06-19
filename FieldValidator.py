from pydantic import BaseModel,EmailStr,AnyUrl,Field,field_validator
from typing import List,Dict,Optional,Annotated

class Patient(BaseModel):
    name : str
    email: EmailStr
    age : int
    weight : float
    married : bool
    allergies : List[str]
    contact_details : Dict[str,str]
    
    @field_validator("email")
    @classmethod
    def email_validator(cls, value):
        valid_domains = ['hdfc.com','icici.com']
        domain_name = value.split('@')[-1]
        if domain_name not in valid_domains:
            raise ValueError("NOT A VALID DOMAIN ")
        
        return value
    @field_validator('name')
    @classmethod
    def Transform_name(cls , value):
        return value.upper()
        
    
    
def update_patient_data(patient : Patient):
    print(patient.name)
    print(patient.age)
    print(patient.email)
    print(patient.weight)
    print(patient.married)
    print(patient.allergies)
    print(patient.contact_details)
    
patient_info = {"name":'nitish','age': 30 ,'email':'xyz@hdfc.com','weight':70,"married":1,"allergies":["Dust","Milk"],"contact_details":{"Phone":"084045903"}}
# OBJECT OF A CLASS - UNPACKING THE DICTIONARY
patient1 = Patient(**patient_info)
# USE THE RETURNED OBJECT
update_patient_data(patient1)
    
    
