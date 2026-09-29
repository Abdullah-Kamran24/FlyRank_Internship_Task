from fastapi import FastAPI
from pydantic import BaseModel 
import _sqlite3 

db = _sqlite3.connect('tasks.db', check_same_thread=False)  
cmnd = db.cursor()

cmnd.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        done INTEGER DEFAULT 0
    )
''')

cmnd.execute("SELECT COUNT (*) FROM tasks")
count =  cmnd.fetchone()[0]

if count == 0 :
     cmnd.execute("INSERT INTO tasks (title , done) VALUES (?,?)", ("LEARN SQLITE" , 0) )

     cmnd.execute("INSERT INTO tasks (title , done) VALUES (?,?)", ("BULID Fast API" , 0) )

     cmnd.execute("INSERT INTO tasks (title , done) VALUES (?,?)", ("FINISH ASSIGNMENT" , 1) )
    
db.commit()

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
    cmnd.execute("SELECT * FROM tasks")
    rows = cmnd.fetchall()
    return rows


# STAGE 1: GET ONE TASK FROM DATABASE
@app.get("/tasks/{id}")
def find(id: int):
    cmnd.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (id,)
    )

    row = cmnd.fetchone()

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
 


    cmnd.execute ("Insert into tasks (Title , Done) Values (?,?)" , (tasks.Title , tasks.Done))
    db.commit()


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

    cmnd.execute(
        "UPDATE tasks SET title = ?, done = ? WHERE id = ?",
        (tasks.Title, tasks.Done, id)
    )

    db.commit()

    if cmnd.rowcount == 0:
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

    cmnd.execute(
        "DELETE FROM tasks WHERE id = ?",
        (id,)
    )

    db.commit()

    if cmnd.rowcount == 0:
        return {
            "error": "Task not found"
        }

    return {
        "message": "Task deleted successfully"
    }
    
    




