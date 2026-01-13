from fastapi import FastAPI, Path, HTTPException, Query
import json

app = FastAPI()

def load_data():
    with open("C:/Users/makerofdreams/Desktop/Fast_api/medical_profiler/patients.json","r") as f:# here with "with" the document opens and closes by itself 
    # the open function opens it and "r" stands for read only 
        data = json.load(f) #json.load helps understand the raw data works as a parser
    return data


@app.get("/")
def hello():
    return {"message" : "pateint management system api"}

@app.get("/about")
def about():
    return {"message" : "a fully functional management system to record pateint's data"}

@app.get("/view")
def view():
    data = load_data()
    return data 

@app.get("/patient/{patient_id}")
def view_patient(patient_id: str = Path(..., description="enter the ID of the patient", examples=["P001"])):
    # this is the standard code for Path and str for establish str is required as argument
    # the problem here remains that if put a patient id that is not available in the json the http status code will still be 200 - ok 
    # all though it should be 404 not found 
    data  = load_data()
    if patient_id in data:
        return data[patient_id] 
    # to get 404 not found we add special exeption called httpexpection 
    'HttpException is  a  special exeption that allows user to put status code instead of json message'
    raise HTTPException(status_code=404 , detail="patient not found")
    # this does not break the code and gives an 404 error 

@app.get("/sort")
def sort_patients(sort_by : str = Query(...,description="this endpoint lets the user sort on the bases of height, weight and bmi"), order : str = Query("asc",description="an endpoint that allow user to choose sort by asc or desc")):
# in query "..."" means mandatory and "..." not present means optional as here order is option and by default the output will be asc
    valid_fields = ["height","bmi","weight"]

    valid_orders = ["asc", "desc"]

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail = f"wrong field selected, select between {valid_fields}")
    
    if order not in valid_orders:
        raise HTTPException(status_code=400, detail= f"wrong order selected, select between {valid_orders}")
    
    data =  load_data()

    if order == "desc":
        sorted_order =  True
    else: 
        sorted_order = False

    sorted_dict = sorted(data.values(),key = lambda x:x.get(sort_by,0),reverse= sorted_order)

    return sorted_dict