from fastapi import FastAPI , Path , HTTPException , Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel , Field , computed_field
from typing import Annotated , Literal , Optional
import json


app = FastAPI()

class Books(BaseModel) :
    id : Annotated[str , Field(..., description = 'This is the id of the book')]
    title : Annotated[str , Field(..., description = 'This is the title of the Book')]
    author : Annotated[str , Field(..., description = 'This is the author of the book')]
    genre : Annotated[str , Field(..., description = 'This is category of the book')]
    price : Annotated[int , Field(..., description = 'This is the price of the book')]
    available : Annotated[bool , Field(..., description = 'This is the staus of avaliability of the book')]

class Book_update(BaseModel) :
    title : Annotated[Optional[str] , Field(default = None, description = 'This is the title of the Book')]
    author : Annotated[Optional[str] , Field(default = None, description = 'This is the author of the book')]
    genre : Annotated[Optional[str] , Field(default = None, description = 'This is category of the book')]
    price : Annotated[Optional[int] , Field(default = None, description = 'This is the price of the book')]
    available : Annotated[Optional[bool] , Field(default = None, decription = 'This is the staus of avaliability of the book')]

def load_data() :
    with open ('books.json' , 'r') as w :
        data = json.load(w)
        return data

def save_data(data) :
    with open ('books.json' , 'w') as w :
        json.dump(data , w)

@app.get('/first_page')
def first_page() :
    return {'This is the first page of the website'}

@app.get('/about')
def about() :
    return {'This project focuses on learning and practicing fast api and its implemnetaion in backend for accessing the database and performing operation like create , update , retrive , delete in database'}

@app.get('/all_books_database')
def all_patients() :
    data = load_data()
    return data

@app.post('/create')
def create(book : Books) :
    data = load_data()
    if book.id in data :
        raise HTTPException(status_code = 400 , detail = 'The book id is already present in the database')
    data[book.id] = book.model_dump(exclude = 'id')
    save_data(data)

    return JSONResponse(status_code = 200 , content = {'message' : 'The Book details is sucessfully saved in the database'})

@app.put('/update/{book_id}')
def update(book_id : str , book_update : Book_update) :
    data = load_data()
    if book_id not in data :
        raise HTTPException(status_code = 400 , detail = 'The book id not exist in database')
    
    existing_book_id_detail = data[book_id]

    updated_data_book_id = book_update.model_dump(exclude_unset = True)

    for key , value in updated_data_book_id.items() :
        existing_book_id_detail[key] = value 
    existing_book_id_detail['id'] = book_id

    pydantic_obj_data = Books(**existing_book_id_detail)

    data[book_id] = pydantic_obj_data.model_dump(exclude = 'id')

    save_data(data)

    return JSONResponse(status_code = 200 , content = {'message' : 'The patient details is upadted sucessfully'})

@app.delete('/delete/{book_id}')
def delete(book_id) :
    data = load_data()
    if book_id not in data :
        raise HTTPException(status_code = 400 , detail = 'The book id is not present in the database')
    del data[book_id]

    save_data(data)

    return JSONResponse(status_code = 400 , content = {'message' : 'The book id details are deleted sucessfully'})
