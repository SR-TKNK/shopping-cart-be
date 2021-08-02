import uvicorn
from uvicorn.supervisors.basereload import BaseReload

if __name__ == "__main__":
    uvicorn.run("app:app", host="localhost", port=8000, reload=True)
    # uvicorn.run("app:app", reload=True)