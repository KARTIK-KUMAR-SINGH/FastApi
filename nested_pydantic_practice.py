from pydantic import BaseModel

class Adress(BaseModel) :
    city : str
    state : str
    pin : int

class Patient(BaseModel) :
    name : str
    gender : str
    age : int
    adress : Adress

adress_dict_1 = {'city' :'Tumakuru' , 'state' : 'Karnataka' , 'pin' : 572102}
adress1 = Adress(**adress_dict_1)

patient_dict_1 = {'name' : 'Nitish' , 'gender' : 'Male' , 'age' : 20 , 'adress' : adress1}
patient1 = Patient(**patient_dict_1)

print(patient1)
print(patient1.name)
print(patient1.gender)
print(patient1.age)
print(patient1.adress)
print(adress1.city)
print(adress1.state)
print(adress1.pin)
