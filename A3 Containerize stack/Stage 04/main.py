from fastapi import FastAPI
from pydantic import BaseModel 
import database
from dotenv import load_dotenv

app = FastAPI()
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
    database.cmnd.execute("SELECT * FROM tasks")
    rows = database.cmnd.fetchall()
    return rows


# STAGE 1: GET ONE TASK FROM DATABASE
@app.get("/tasks/{id}")
def find(id: int):
    database.cmnd.execute(
        "SELECT * FROM tasks WHERE id = %s",
        (id,)
    )

    row = database.cmnd.fetchone()

    if row is None:
        return {
            "error": "Task not found"
        }

    return row


class TaskCreate(BaseModel):

    Title : str
    Done : bool 



@app.post("/tasks")
def create(tasks : TaskCreate) :

    if tasks.Title == "" : 
        return {
            "Error" : "Title is empty " , 
            "Status" : 400
        }
 


    database.cmnd.execute ("Insert into tasks (Title , Done) Values (%s,%s)" , (tasks.Title , tasks.Done))
    database.db.commit()


    return {"Task Added " 
            "Status :  201 " 
            }

@app.put("/tasks/{id}")
def change(id: int, tasks: TaskCreate):

    if tasks.Title == "":
        return {
            "Error": "Title is empty",
            "Status": 400
        }

    database.cmnd.execute(
        "UPDATE tasks SET title = %s, done = %s WHERE id = %s",
        (tasks.Title, tasks.Done, id)
    )

    database.db.commit()

    if database.cmnd.rowcount == 0:
        return {
            "error": "Task not found"
        }

    return {
        "id": id,
        "Title": tasks.Title,
        "Done": tasks.Done
    }
    
     
     
@app.delete("/tasks/{id}")
def remove(id: int):

    database.cmnd.execute(
        "DELETE FROM tasks WHERE id = %s",
        (id,)
    )

    database.db.commit()

    if database.cmnd.rowcount == 0:
        return {
            "error": "Task not found"
        }

    return {
        "message": "Task deleted successfully"
    }
    
    




