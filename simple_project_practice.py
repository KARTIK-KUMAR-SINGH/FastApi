from fastapi import FastAPI , Path , HTTPException ,Query
import json


app = FastAPI()

def load_data() :
    with open("patients.json") as f :
        data = json.load(f)
        return data
    
@app.get("/")
def hello() :
    return {"Thus is the intro page"}

@app.get("/about")
def about() :
    return {"The is the about page"}


@app.get("/all_patients")
def all_patients() :
    data = load_data()
    return data

# @app.get("/indivisual_patient_id/{patient_id}")
# def patient_id(patient_id : str = Path(..., description = 'Id of the patient is required here' , example = 'P001')) :
#     data = load_data()
#     if patient_id in data :
#         return {'The patien data is' : data[patient_id]}
#     raise HTTPException(status_code = 404 , detail = 'Patient id not found')

# @app.get('/sort') 
# def sort_patients(sort_by : str = Query(..., description = 'Sort on the basis of height , weight , bmi') , order : str = Query('asc' , description = 'sort in asc or desc order')):
#     valid_fields = ['height' , 'weight' , 'bmi']

#     if sort_by not in valid_fields:
#         raise HTTPException(status_code = 400 , detail = f'Invalid field select from {valid_fields}')
    
#     if order not in ['asc' , 'desc'] :
#         raise HTTPException(status_code = 400 , detail = 'Invalid order selection between asc and desc')
    
#     data = load_data()

#     sort_order = True if order == 'desc' else False

#     sorted_data = sorted(data.values() , key=lambda x: x.get(sort_by , 0) , reverse = sort_order)

#     return sorted_data

@app.get('/indivisual_patient/{patient_id}')
def patient_id(patient_id : str = Path(..., description = 'Id of the patient' , example = 'P001')):
    data = load_data() 
    if patient_id in data :
        return{'The patient data is :' : data[patient_id]}
    raise HTTPException(status_code = 404 , detail = 'Id not found in database')

@app.get('/sort')
def sort_patients(sort_by : str = Query(..., description = 'enter how you want to sort height , weight , bmi') , order : str = Query('asc' , description = 'sort in asc or desc order')) :
    valid_fields = ['height' , 'weight' , 'bmi']

    if sort_by not in valid_fields :
        raise HTTPException(status_code = 400 , detail = f'Invalid sort type selected among {valid_fields}')
    if order not in ['asc' , 'desc'] :
        raise HTTPException(status_code = 400 , detail = 'Invalid order selection between asc and desc')
    
    data = load_data()
    sort_order = True if order == 'desc' else False
    sorted_data = sorted(data.values() , key=lambda x: x.get(sort_by , 0) , reverse = sort_order)
    return sorted_data

