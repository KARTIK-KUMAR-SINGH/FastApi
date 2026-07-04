# from pydantic import BaseModel

# class Patient(BaseModel) :
#     name : str
#     age : int

# def insert_patient_data(patient : Patient) :
#     print(patient.name)
#     print(patient.age)
#     print("Insterted")

# patients_info = {'name' : 'nitish' , 'age' : 30}

# patient1 = Patient(**patients_info)
# a
# insert_patient_data(patient1)

from pydantic import BaseModel ,EmailStr ,Field , field_validator ,model_validator ,computed_field
from typing import List , Dict ,Annotated
from typing import Optional
class Patient(BaseModel):
    # name : str = Field(max_length = 50)
    # email : EmailStr
    # age : int
    # # weight : float = Field(ge = 0 , lt = 60)
    # weight : Annotated[float , Field(gt = 0 , strict = True)]
    # married : bool = False
    # allergies : Optional[List[str]] = None
    # contact_details : Dict[str , str]
    name : str
    email : EmailStr
    age : int
    weight : float
    height : float
    married : bool = False
    allergies : Optional[List[str]] = None
    contact_details : Dict[str , str]

    @field_validator('email')
    @classmethod
    def email_validator(cls , value) :
        valid_domain = ['hdfc.com' , 'icci.com']
        domain_name = value.split('@')[-1]
        if domain_name not in valid_domain :
            raise ValueError('Not Valid email domain fo this')
        return value
    
    # @field_validator('name')
    # @classmethod
    # def field_validator(cls , value) :
    #     value_check = value.isupper()
    #     if(value_check != True) :
    #         raise ValueError('The Name is not in Capital Letters')
    #     return value

    @field_validator('name')
    @classmethod
    def field_checker(cls , value) :
        return value.upper()
    
    # @model_validator(mode = 'after')
    # def validate_emergency_contact(cls , model) :
    #     if model.age > 60 and 'emergency' not in model.contact_details :
    #         raise ValueError ('Patients greater than 60 should have emergency conatact number in there contact details')
    #     return model

    @computed_field
    @property
    def calculate_bmi(self) -> float :
        bmi = round(self.weight/(self.height**2) , 2)
        return bmi
def insert_a_data(patient : Patient):
    print(patient.name)
    print(patient.email)
    print(patient.age)
    print(patient.weight)
    print(patient.height)
    print(patient.calculate_bmi)
    print(patient.married)
    print(patient.allergies)
    print(patient.contact_details)

    print("Inserted")

def update_a_data(patient : Patient):
    print(patient.name)
    print(patient.age)
    print("Updated")

patient_info = {'name' : 'Nitish' , 'email' : 'abc@icci.com' , 'age' : 20 , 'weight' : 55 , 'height' : 1.72 , 'contact_details' : {'email' : 'Nitish@gmail.com' , 'phone_no' : '11111000000'}}
patient1 = Patient(**patient_info)

# update_info = {'name' : 'Ramesh' , 'age' : 20}
# patient2 = Patient(**update_info)
insert_a_data(patient1)
# update_a_data(patient2)