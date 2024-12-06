from fastapi import FastAPI
from classifier_models import app as classifier_app

main_app = FastAPI()

main_app.mount("/", classifier_app)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(main_app, host="0.0.0.0", port=8000, reload=True)
