from fastapi import FastAPI

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

