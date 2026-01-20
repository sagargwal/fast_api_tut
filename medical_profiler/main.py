from fastapi import FastAPI, Path, HTTPException, Query
import json
from fastapi.responses import JSONResponse
from pydantic  import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional



app = FastAPI()


class patient(BaseModel):
    # Annotated is a typing wrapper class it is not a function nor a class and  stores a base type and metadata so tools like Pydantic can enforce rules later.
    '''
    this is how annotated will look like 
    class FakeAnnotated:
    def __init__(self, base_type, *metadata):
        self.base_type = base_type
        self.metadata = metadata'''
    # the reason why wee are not using comma after each variable is because they are independent and does not work as arguments of a function
    #  the reason why str and fields are stored in [] and not in () is because it is not  callable class that does something and str and field does not go it .__init__ but it goes in .__getitems__()
    id : Annotated[str, Field(..., description="id of the patient", examples=["P001"])]
    name : Annotated[str, Field(..., description="name of the patient")]
    city : Annotated[str, Field(..., description="city of the patient")]
    age : Annotated[int, Field(...,gt=0 , lt= 120,description="age of the patient")]
    gender : Annotated[Literal["male","female","others"],Field(...,description="gender of the patient")]
    height : Annotated[float, Field(...,gt=0, description="height of the patient in mtrs")]
    weight : Annotated[float, Field(...,gt=0, description="weight of the patient in kgs")]


    '''@property & @computed_field — very short notes (final)

    @property → access method like a variable (patient.bmi)

    Without @property → patient.bmi is a method, not a value

    @computed_field → include field in model_dump() / JSON

    Without @property → model_dump() will NOT include bmi

    Both together → value auto-calculates and appears in JSON

    One-line rule:

    @property makes it readable, @computed_field makes it exportable.'''
    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi
    
    @computed_field
    @property
    def verdict(self) -> str:

        if self.bmi < 18.5:
            return 'Underweight'
        elif self.bmi < 25:
            return 'Normal'
        elif self.bmi < 30:
            return 'Normal'
        else:
            return 'Obese'





def load_data():
    with open("C:/Users/makerofdreams/Desktop/Fast_api/medical_profiler/patients.json","r") as f:# here with "with" the document opens and closes by itself 
    # the open function opens it and "r" stands for read only 
        data = json.load(f) #json.load helps understand the raw data works as a parser
    return data

def save_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data, f)
    


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


@app.post('/create')
def create_patient(patient: patient):

    # load existing data
    data = load_data()

    # check if the patient already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail='Patient already exists')

    # new patient add to the database
    data[patient.id] = patient.model_dump(exclude=['id'])

    # save into the json file
    save_data(data)

    return JSONResponse(status_code=201, content={'message':'patient created successfully'})


    