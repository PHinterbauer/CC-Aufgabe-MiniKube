from fastapi import FastAPI, HTTPException, Query, Request, Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, generate_latest
from pydantic import BaseModel

from app.core import add


class User(BaseModel):
    name: str
    age: int
    email: str

users_db: dict[int, User] = {}


app = FastAPI(title="Test API", version="0.1.0")

http_requests_total = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "path", "status"],
)


@app.middleware("http")
async def count_requests(request: Request, call_next):
    response = await call_next(request)
    http_requests_total.labels(
        request.method,
        request.url.path,
        str(response.status_code),
    ).inc()
    return response


@app.get("/api/health")
def health() -> dict:
    checks = {}
    errors = {}

    try:
        if add(1, 2) != 3:
            raise ValueError("add check returned unexpected result")
    except Exception as exc:
        checks["add"] = "error"
        errors["add"] = str(exc)
    else:
        checks["add"] = "ok"

    try:
        generate_latest()
    except Exception as exc:
        checks["metrics"] = "error"
        errors["metrics"] = str(exc)
    else:
        checks["metrics"] = "ok"

    overall_status = "ok" if not errors else "degraded"

    return {"status": overall_status, "checks": checks, "errors": errors}


@app.get("/api/add")
def add_route(
    x: int = Query(..., description="First integer"),
    y: int = Query(..., description="Second integer"),
) -> dict:
    return {"result": add(x, y)}


@app.get("/metrics")
def metrics() -> Response:
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.post("/api/users/{user_id}")
def create_user(user_id: int, user: User) -> dict:
    if user_id in users_db:
        raise HTTPException(status_code=400, detail="Benutzer existiert bereits")
    users_db[user_id] = user
    return {"nachricht": "Benutzer erfolgreich angelegt", "benutzer": user}


@app.put("/api/users/{user_id}")
def update_user(user_id: int, user: User) -> dict:
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="Benutzer nicht gefunden")
    users_db[user_id] = user
    return {"nachricht": "Benutzer erfolgreich bearbeitet", "benutzer": user}


@app.delete("/api/users/{user_id}")
def delete_user(user_id: int) -> dict:
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="Benutzer nicht gefunden")
    del users_db[user_id]
    return {"nachricht": "Benutzer erfolgreich gelöscht"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
