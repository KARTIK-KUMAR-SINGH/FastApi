from fastapi import FastAPI
import json

app = FastAPI()

def load_data():
    with open('patients.json') as f:
        data = json.load(f)

    return data

@app.get("/")
def Hello() :
    return {'message' : 'Pateints data is avaliable here'}

@app.get("/about")
def about() :
    return {'message' : 'All patients data can be found here'}

@app.get("/view")
def view() :
    data = load_data()
    return data