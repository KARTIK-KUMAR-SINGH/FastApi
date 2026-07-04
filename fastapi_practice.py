from fastapi import FastAPI , Path , HTTPException , Query
import json

app = FastAPI()

def load_data() :
    with open('patients.json') as f :
        data = json.load(f)
        return data
    
@app.get("/")
def hello() :
    return {'This is the Hello Page'}

@app.get("/about")
def about() :
    return {'This is the about Page'}

@app.get("/all_patient_data")
def all_patient_data() :
    data = load_data()
    return data

@app.get("/individual_patient_id/{patient_id}")
def individual_patient_data(patient_id : str = Path(..., description = "Id of the Patient" , example = 'P001')) :
    data = load_data()
    if patient_id not in data :
        raise HTTPException (status_code = 404 , detail = "Patient Id not found in database")
    return data[patient_id]

@app.get("/sort")
def sort(sort_by : str = Query(..., description = 'Enter the type by which you wnat to sort :- height , weight , bmi') , order : str = Query('asc' ,  description = 'Enter the order in which data should be there ascending(asc) , decending(desc)')) : 
    valid_fields = ['height' , 'weight' , 'bmi']

    if sort_by not in valid_fields : 
        raise HTTPException(status_code = 400 , detail = 'Invalid sorting request {sort_by} among {valid_fields}')
    if order not in ['asc' , 'desc'] :
        raise HTTPException(status_code = 400 , detail = 'Invalid order request {order} among :- asc , desc')
    
    data = load_data()
    sort_order = True if order == 'desc' else False
    sorted_data = sorted(data.values() , key=lambda x: x.get(sort_by , 0) , reverse = sort_order)
    return sorted_data