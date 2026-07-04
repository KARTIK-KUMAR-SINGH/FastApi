from fastapi import FastAPI , Path , HTTPException , Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel , Field , computed_field
from typing import Annotated , Literal , Optional
import json

app = FastAPI()

class Patients(BaseModel) :
    id = Annotated[str , Field(..., description = 'Enter the unique ID of the Patient')] 
    name : Annotated[str , Field(..., description = 'Enter the name of the Patient :- ')]
    city : Annotated[str , Field(..., description = 'Enter the name of the city :- ')]
    age : Annotated[int , Field(..., gt = 0 , lt = 120 , description = 'Enter the name of the patient :- ')]
    gender : Annotated[Literal['Male' , 'Female' , 'Neutral'] , Field(..., description = 'Enter teh gender ofthe person :-')]
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
            return {'Underweight'}
        elif(18.5 <= self.bmi <= 24.9) :
            return {'Normal'}
        else : 
            return {'Obese'}


def load_data():
    with open('patients.json' , 'w') as f :
        data = json.load(f)
        return data
    
def save_data(data) :
    with open('patients.json' , 'w') as f :
        json.dump(data , f)
    
@app.get('/create')
def create(patient : Patients) :
    #load data
    data = load_data()

    #check whether the data exists?
    if(data[patient.id] == data) :
        raise HTTPException(status_code = 400 , detail = 'The given Patient id already exists in database')
    
    #if data dosen't exists --> save data --> create the data
    data[patient.id] = patient.model_dump(exclude = ['id'])
    save_data(data)

    return JSONResponse(status_code = 201 , content = {'message' : 'The Patient details created sucessfully'})