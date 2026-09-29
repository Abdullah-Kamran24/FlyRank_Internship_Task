from fastapi import FastAPI

app = FastAPI()

Tasks =  [ 

    {
        "id" : 1  ,
        "Title" : "Tasks 1 "  , 
        "Done" : True 

    } , 

    {
        "id" : 2  , 
        "Title" : "Task 2 " , 
        "Done" : False  , 

    }
    , 
    {
        "id" : 3 , 
        "Title" : "Task 3 " , 
        "Done" : False 
    }
]






@app.get("/") 
def root():
    return {
        "name" : "Task API" , 
        "version" : "1.0" , 
        "endpoint" : ['/tasks']
    }



@app.get("/health")
def health():
    return {"status": "Ok"}


@app.get("/tasks")
def tasks(): 
    return Tasks 


@app.get("/tasks/{id}")
def find(id: int):

    for task in Tasks:
        if task["id"] == id:
            return task

    return {
        "Error Status": "404",
        "Error": f"Task {id} NOT FOUND"
    }
