from fastapi import FastAPI , Path , HTTPException , Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel , Field , computed_field
from typing import Annotated , Literal , Optional
import json

app = FastAPI ()

class Patients(BaseModel) :
    id : Annotated[str , Field(..., description = "Enter the Patient Unique id :- " , examples = ['P001'])]
    name : Annotated[str , Field(..., description = "Enter the Name of the Patient")]
    city : Annotated[str , Field(..., description = "Enter the City name :- ")]
    age : Annotated[int , Field(..., gt = 0 , lt = 120 , description = "Enter the Ange of the Patient :- ")]
    gender : Annotated[Literal['male' , 'female' , 'others'], Field(..., description = "Enter either Male or Female :-")]
    height : Annotated[float , Field(..., gt = 0 , desription = 'Enter the Height of the Person in Meteres :-')]
    weight : Annotated[float , Field(..., gt = 0 , description = 'Enter the Weight of the Person :-')]

    @computed_field
    @property
    def bmi(self) -> float :
        bmi = round(self.weight/(self.height**2) , 2)
        return bmi 

    @computed_field
    @property
    def verdict(self) -> str :
        if(self.bmi < 18.5) :
            return 'Underweight'
        elif(self.bmi < 25) :
            return 'Normal'
        elif(self.bmi < 30) :
            return 'Normal'
        else :
            return 'Obese'
        
def load_data() :
    with open ('patients.json') as f :
        data = json.load(f)
        return data
    
def save_data(data) :
    with open ('patients.json' , 'w') as f :
        json.dump(data , f)

@app.post('/create')
def create_patient(patient : Patients):
    #load Existing data
    data  = load_data()

    #check whether data is already present or not 
    if patient.id in data :
        raise HTTPException(status_code = 400 , detail = 'Patient Id already Exists')
    
    #add the new data if it is not present
    data[patient.id] = patient.model_dump(exclude = ['id'])

    #save into json file 
    save_data(data)

    return JSONResponse(status_code = 201 , content = {'message' : 'patient created sucessfully'})