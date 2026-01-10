from fastapi import FastAPI
import json

app = FastAPI()

def laod_data():
    with open("C:/Users/makerofdreams/Desktop/Fast_api/medical_profiler/patients.json","r") as f:
        data = json.load(f)
    return data


@app.get("/")
def hello():
    return {"message" : "pateint management system api"}

@app.get("/about")
def about():
    return {"message" : "a fully functional management system to record pateint's data"}

@app.get("/view")
def view():
    data = laod_data()
    return data 



