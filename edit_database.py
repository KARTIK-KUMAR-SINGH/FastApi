from fastapi import FastAPI , Path , HTTPException , Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel , Field , computed_field
from typing import Annotated , Literal , Optional
import json


app = FastAPI()

class Patients(BaseModel) :
    id : Annotated[str , Field(..., description = 'Enter the unique ID of the Patient')] 
    name : Annotated[str , Field(..., description = 'Enter the name of the Patient :- ')]
    city : Annotated[str , Field(..., description = 'Enter the name of the city :- ')]
    age : Annotated[int , Field(..., gt = 0 , lt = 120 , description = 'Enter the name of the patient :- ')]
    gender : Annotated[Literal['male' , 'female' , 'neutral'] , Field(..., description = 'Enter teh gender ofthe person :-')]
    height : Annotated[float , Field(..., description = 'Enter the height of the person in metres :- ')]
    weight : Annotated[float , Field(..., description = 'Enter the weight of the person in Kgs :-')]

    @computed_field
    @property
    def bmi(self) -> float :
        bmi = (self.weight / (self.height)**2)
        return bmi
    
    @computed_field
    @property
    def verdict(self) -> str :
        if self.bmi < 18.5 :
            return 'Underweight'
        elif(18.5 <= self.bmi <= 24.9) :
            return 'Normal'
        else : 
            return 'Obese'

class PatientUpdate(BaseModel) :
    name : Annotated[Optional[str] , Field(default = None , description = 'Enter the name of the correct Patient name :- ')]
    city : Annotated[Optional[str] , Field(default = None , description = 'Enter the correct city name :- ')]
    age : Annotated[Optional[int]  , Field(default = None , gt =0 , lt = 120 , description = 'Enter the new age number :- ')]
    gender : Annotated[Optional[Literal['male' , 'female' , 'neutral']], Field(default = None , description = 'Enter the updated gender :-')]
    height : Annotated[Optional[float] , Field(default = None , description = 'Enter the new height :- ')]
    weight : Annotated[Optional[float] , Field(default = None , description = 'Enter the new weight :- ')]

def load_data() :
    with open ('patients.json' , 'r') as f :
        data = json.load(f)
        return data
    
def save_data(data) :
    with open('patients.json' , 'w') as f :
        json.dump(data , f)

@app.put('/edit/{patient_id}')
def edit_patient_data(patient_id : str , patient_update : PatientUpdate) :
    data = load_data()

    if patient_id not in data :
        raise HTTPException(400 , detail = 'The Pateint Id doesnt exists in database :-')
    
    existing_patient_info = data[patient_id]

    updated_patient_info = patient_update.model_dump(exclude_unset = True)

    for key , value in updated_patient_info.items():
        existing_patient_info[key] = value

    existing_patient_info['id'] = patient_id
    patient_pydantic_obj = Patients(**existing_patient_info)

    existing_patient_info = patient_pydantic_obj.model_dump(exclude = 'id')

    data[patient_id] = existing_patient_info

    save_data(data)

    return JSONResponse(status_code = 200 , content = {'message' : 'patient details updated'})

@app.delete('/delete/{patient_id}') 
def delete(patient_id : str) :
    data = load_data()
    if patient_id not in data :
        raise HTTPException(status_code = 400 , detail = 'Patient id not found in database')
    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code = 200 ,content = {'message' : 'patient details deletion sucessful'})