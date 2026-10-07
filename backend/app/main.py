from fastapi import FastAPI

app = FastAPI(
    title="Private Tutor Finder API",
    version="1.0.0",
)


@app.get("/")
def root():
    return {"message": "Private Tutor Finder API"}