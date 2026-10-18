from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {
        "message" : "Project Dabbewala is serving.",
        "description" : "This is a project to manage the delivery of food and other items in a city using a network of delivery personnel called Dabbewalas."
    }
