from fastapi import FastAPI,Path,HTTPException,Query
import json
app = FastAPI()

def load_data():
    with open('patients.json','r') as f:
        data = json.load(f)
    return data

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
def view_patient(patient_id : str = Path(...,description = 'ID OF THE PATEINT IN THE DB',example = "P001")):
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
