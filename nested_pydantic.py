from pydantic import BaseModel

class Adress(BaseModel) :
    city : str
    state : str
    pin : int

class Patient(BaseModel) :
    name : str
    gender : str = 'Male'
    age : int
    address : Adress


adress_dict = {'city' : 'tumakuru' , 'state' : 'karnataka' , 'pin' : 572102}

adress1 = Adress(**adress_dict)

patients_dict = {'name' : 'Nitish' , 'gender' : 'male' , 'age' : 20 , 'address' : adress1}

patient1 = Patient(**patients_dict)

print(patient1)
print(patient1.name)
print(patient1.gender)
print(patient1.age)
print(patient1.address)

temp1 = patient1.model_dump()
print(temp1)
print(type(temp1))

temp2 = patient1.model_dump_json()
print(temp2)
print(type(temp2))


temp3 = patient1.model_dump(include = ['name' , 'gender'])
print(temp3)
print(type(temp3))

temp4 = patient1.model_dump(exclude = ['name' , 'gender'])
print(temp4)
print(type(temp4))

temp5 = patient1.model_dump(exclude = {'address' : ['state']})
print(temp5)
print(type(temp5))

temp6 = patient1.model_dump(exclude_unset = True)
print(temp6)
print(type(temp6))