from fastapi import FastAPI
from pydantic import BaseModel 

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


class TaskCreate(BaseModel):

    Title : str
    Done : bool 



@app.post("/tasks")
def create(tasks : TaskCreate) :

    if tasks.title == "" : 
        return {
            "Error" : "Title is empty " , 
            "Status" : 400
        }
 


    Tasks.append(
        {
            "id": len(Tasks) + 1 , 
            "Title" : tasks.title , 
            "Done" : False
        }
    )

    return {"Task Added " 
            "Status :  201 " 
            }

@app.put("/tasks/{id}")
def change(id : int , tasks : TaskCreate):

     found = False
       

     if tasks.Title=="":
            return {
                "Empty Body " 
                "Error 400 "
    
            }


     for t in Tasks : 
         if t["id"] == id :
                    found = True 
                    t["Title"] = tasks.Title 
                    t["Done"] = tasks.Done 
                    return t
         
     if found == False :
          return {"Unknown ID    Error 404 " }    
    

    
     
     
@app.delete("/tasks/{id}")
def remove(id:int):
    found = False 

    for t in Tasks : 
          if t["id"] == id :
               found = True  
               t.pop("id")
               return {
                    "No Content - Content Successfully removed "
               }

    if found == False : 
         return {
              "Unknown ID -> Error - 404  "
         }


    

    
    




