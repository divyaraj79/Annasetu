from fastapi import FastAPI

app = FastAPI(title="AnnaSetu API")


@app.get("/")
def root():
    return {"message": "AnnaSetu Backend Running 🚀"}