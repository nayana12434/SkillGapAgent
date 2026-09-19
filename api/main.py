from fastapi import FastAPI

app = FastAPI(title="SkillBridge")


@app.post("/analyze")
def analyze(payload: dict):
    raise NotImplementedError
