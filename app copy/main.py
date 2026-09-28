from fastapi import FastAPI

app = FastAPI(title="StudyHub Planner API")

@app.get("/status")
def health():
    return {
        'status': 'ok'
    }