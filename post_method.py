from fastapi import FastAPI,Path,Query,HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal,Optional
import json

app = FastAPI()


class Patient(BaseModel):
    id: Annotated[str,Field(...,description="Id of patient",examples=['P001'])]
    name:Annotated[str , Field(...,description='Name of patient')]
    city:Annotated[str , Field(...,description='City Where Patient lives')]
    age:Annotated[int,Field(...,gt = 0 , lt = 120 , description=" PATIENT AGE")]
    gender:Annotated[Literal['male','Female','Others'],Field(...,description="ENTER GENDER")]
    height:Annotated[float,Field(...,gt = 0 ,description=" PATIENT HEIGHT in meters ")]
    weight:Annotated[float,Field(...,gt = 0 ,description=" PATIENT Weight in Kgs ")]
    
    
@computed_field
@property
def bmi(self)-> float:
    bmi = round((self.weight)/(self.height),2)
    return bmi

@computed_field
@property
def verdict(self)-> str :
    if self.bmi < 18.5:
        return "UNDERWEIGHT"
    elif self.bmi < 25:
        return "Normal"
    elif self.bmi < 30:
        return "Perfect"
    else :
        return "OVERWEIGHT"
    
class PatientUpdate(BaseModel):
    name:Annotated[Optional[str] , Field(default = None)]
    city:Annotated[Optional[str] , Field(default = None)]
    age:Annotated[Optional[int] , Field(default = None,gt = 0)]
    gender:Annotated[Optional[Literal['male','Female','Others']],Field(default=None)]
    height:Annotated[Optional[float],Field(default=None,gt = 0)]
    weight:Annotated[Optional[float],Field(default=None,gt = 0)]
    
def load_data():
    with open("patients.json",'r') as f:
        data = json.load(f)
    return data
def save_data(data):
    with open('patients.json','w') as f:
        json.dump(data,f)
        


@app.get("/")
def hello():
    return {"Message":"HELLO"}

@app.get("/about")
def about():
    return {"Message":"FULLY FUNCTIONAL API TO MANAGE YOUR PATIENT RECORDS"}

@app.get("/view")
def view():
    data = load_data()
    return data

@app.get("/patients/{patient_id}")
def view_patient(patient_id : str = Path(...,description = 'ID OF THE PATEINT IN THE DB',examples = "P001")):
    # load all the patients
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code= 404 , detail="Patient not found")


@app.get("/sort")
def sort_patients(sort_by:str = Query(...,description="SORT ON BASIS OF HEIGHT,WEIGHT,BMI"),order:str = Query('asc',description='Sort on asc or desc')):
    valid_fields = ['height','weight','bmi']
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400,detail=f"INVALID FIELD SELECT FROM {valid_fields}")
    if order not in ['asc','desc'] :
        raise HTTPException(status_code=400,detail="SELECT BETWEEN asc or desc")
    data = load_data()
    sorted_order = True if order=='desc' else False
    sorted_data = sorted(data.values(),key = lambda x:x.get(sort_by,0),reverse=sorted_order)
    

    return sorted_data


@app.post('/create')
def create_patient(patient: Patient):
    data = load_data()
    if patient.id in data:
        raise HTTPException(status_code= 400 , detail = 'ALREADY EXIST')
    
    data[patient.id] = patient.model_dump(exclude=['id'])# CONVERTS A PYDANTIC OBJECT IN TO DICTIONARY 
    save_data(data)
    
    return JSONResponse(status_code= 201,content = {'message':"PATIENT CREATED SUCCESFULLY"})
    
    
@app.put('/edit/{patient_id}')
def Update_patient(patient_id : str, patient_update : PatientUpdate):
        data = load_data()
        
        if patient_id not in data:
            raise HTTPException(status_code= 404 , detail = 'Patient Not Found')
        
        existing_info = data[patient_id]
        
        updated_patient_info = patient_update.model_dump(exclude_unset=True)
        
        for key , value in updated_patient_info.items():
            existing_info[key] = value
            
        existing_info['id'] = patient_id
        patient_pydantic_obj = Patient(**existing_info)
        
        existing_info = patient_pydantic_obj.model_dump(exclude='id')
        
        data[patient_id] = existing_info
        
        save_data(data)
        
        return JSONResponse(status_code= 200 , content={'message':'Patient Updated'})
    
@app.delete('/delete/{patient_id}')
def delete_patient(patient_id : str):
    data = load_data()
    
    if patient_id not in data:
        raise HTTPException(status_code= 404 , detail="PATIENT NOT FOUND ")
    
    del data[patient_id]
    
    return JSONResponse(status_code= 200 ,content={"message":"DELETED SUCCESFULLY"})
