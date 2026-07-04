from fastapi import FastAPI , Path , HTTPException , Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel , Field , computed_field
from typing import Annotated , Literal , Optional
import json

app = FastAPI()

class Patient_update(BaseModel) :
    name :Annotated[Optional[str] , Field(default = None , description = 'Enter the name of the Patient')]
    city : Annotated[Optional[str] , Field(default = None, description = 'Enter the name of the city')]
    age : Annotated[Optional[int] , Field(default = None , gt = 0 , lt = 120 , description = 'Enter the age of the Patient')]
    gender : Annotated[Optional[Literal['male' , 'female' , 'neutral']] , Field(default = None , description = 'Enter the gender of the patient')]
    height : Annotated[Optional[float] , Field(default = None , description = 'Enter the height of the Patient')]
    weight : Annotated[Optional[float] , Field(default = None, description = 'Enter the weight of the Patient')]

class Patient(BaseModel):
    id :Annotated[str , Field(..., description = 'Enter the id of the Patient')]
    name :Annotated[str , Field(..., description = 'Enter the name of the Patient')]
    city : Annotated[str , Field(..., description = 'Enter the name of the city')]
    age : Annotated[int , Field(gt = 0 , lt = 120 , description = 'Enter the age of the Patient')]
    gender : Annotated[Literal['male' , 'female' , 'neutral'] , Field(..., description = 'Enter the gender of the patient')]
    height : Annotated[float , Field(..., description = 'Enter the height of the Patient')]
    weight : Annotated[float , Field(... , description = 'Enter the weight of the Patient')]

    @computed_field
    @property
    def bmi(self) -> float :
        bmi = (self.weight) / (self.height)**2
        return bmi
    
    @computed_field
    @property
    def verdict(self) -> str :
        if(self.bmi <= 18.4) :
            return ('Underweight')
        elif((self.bmi > 18.4) and (self.bmi <= 24.9)) :
            return ('Normal')
        elif((self.bmi > 24.9) and (self.bmi <= 39.9)) :
            return ('OverWeight')
        else :
            return ('Obese')
        
def save_data(data) :
    with open ('patients.json' , 'w') as f :
        json.dump(data , f)

def load_data() :
    with open ('patients.json' , 'r') as f :
        data = json.load(f)
        return data


@app.get('/')
def hello():
    return {'Hello user this is the first page.....Nice to see you here'}


@app.get('/about')
def about():
    return {'This website is created to perform 4 major operations on the PAtients data taht we have :- CURD operation'
            'C----------> Create a new Patient data with al the necesaary details'
            'U----------> Update the existing patients data'
            'R----------> Retrive The data of a particuar Patient or all the patients from the dataebase'
            'D----------> Delete a Particuar PAtient data if needed'}

@app.get('/all_patients_data')
def all_patients_data() :
    data = load_data()
    return data 

@app.post('/create')
def create_patient(patient : Patient) :
    data = load_data()
    if patient.id in data :
        raise HTTPException(status_code = 400 , detail = 'The Patient Id Already exists in database')
    data[patient.id] = patient.model_dump(exclude = ['id'])

    save_data(data)

    return JSONResponse(status_code = 200 , content = {'message' : 'patient created sucessfully'})

@app.put('/update/{patient_id}')
def update_patient(patient_id : str , patient_update : Patient_update) :
    data = load_data()
    if patient_id not in data :
        raise HTTPException(status_code = 400 , detail = 'The patient id to edit is not found in database')
    
    existing_patient_data = data[patient_id]

    update_patient_data = patient_update.model_dump(exclude_unset = True)

    for key , value in update_patient_data.items() :
        existing_patient_data[key] = value

    existing_patient_data['id'] = patient_id

    #convert existing patient data into pydantic object

    pydantic_object_data = Patient(**existing_patient_data)

    existing_patient_data = pydantic_object_data.model_dump(exclude = 'id')

    save_data(data)
    
    return JSONResponse(status_code = 200 , content = {'message' : 'The Patient data is updates sucessful'})

@app.delete('/delete/{patient_id}')
def delete_patient_id(patient_id) :
    data = load_data()
    if patient_id not in data :
        raise HTTPException(status_code = 400 , detail = 'The Patient id is not in database')
    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code = 200 , content = {'message' : 'The Patient details of the entered patient id is delted sucessfully'})

