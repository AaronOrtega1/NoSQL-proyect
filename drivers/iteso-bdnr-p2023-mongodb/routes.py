#!/usr/bin/env python3
from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from model import Book, BookUpdate

router = APIRouter()

@router.post("/", response_description="Post a new book", status_code=status.HTTP_201_CREATED, response_model=Book)
def create_book(request: Request, book: Book = Body(...)):
    book = jsonable_encoder(book)
    new_book = request.app.database["books"].insert_one(book)
    created_book = request.app.database["books"].find_one(
        {"_id": new_book.inserted_id}
    )

    return created_book


@router.get("/", response_description="Get all books", response_model=List[Book])
def list_books(request: Request, rating: float = 0, pages: int = 0, title: str = "", limit: int = 0, skip: int = 0 ):
    books = list(request.app.database["books"].find())
    books_by_rating = list(request.app.database["books"].find({"average_rating":{"$gte":rating}}))
    books_by_page = list(request.app.database["books"].find({"num_pages": {"$gte": pages}}))
    books_by_title = list(request.app.database["books"].find({"title":title}))
    if(rating != 0):
        return books_by_rating
    elif (pages != 0):
        return books_by_page
    elif (title != ""):
        return books_by_title
    else:
        return books



@router.get("/{id}", response_description="Get a single book by id", response_model=Book)
def find_book(id: str, request: Request):
    if (book := request.app.database["books"].find_one({"_id": id})) is not None:
        return book

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with ID {id} not found")

@router.put("/{id}", response_description="Update a book by id", response_model=Book)
def update_book(id: str, request: Request, book: BookUpdate = Body(...)):
    if(request.app.database["books"].find_one({"_id": id})) is not None:
        my_query = {"_id": id}
        updated_book = book.dict(exlude_unset=True)
        new_values = {"$set": {updated_book}}
        request.app.database["books"].update_one(my_query, new_values)
        return updated_book
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with ID {id} not found")

@router.delete("/{id}", response_description="Delete a book")
def delete_book(id: str, request: Request, response: Response):
    if(request.app.database["books"].find_one({"_id": id})) is not None:
        my_query = {"_id": id}
        request.app.database["books"].delete_one(my_query)
        response.status_code = status.HTTP_204_NO_CONTENT
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with ID {id} not found")