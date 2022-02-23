from typing import Optional

from fastapi import FastAPI, HTTPException
from logics import expression_count, history_support, validate_input
from pydantic import BaseModel

# History cache initiation
CACHE = []

# API object creation
app = FastAPI()


class Item(BaseModel):
    exp: str


@app.get("/calc")
async def welcome():
    return {"message": "Welcome to CalcAPI"}


@app.post("/calc")
async def calc(item: Item):
    """Main calculation and history initiation"""

    validation = validate_input(item.exp)
    if validation:
        result = expression_count(validation)
        CACHE.append(
            {
                "request": f"{item.exp}",
                "response": f"{result}",
                "status": "success",
            }
        )
    else:
        CACHE.append(
            {"request": f"{item.exp}", "response": "", "status": "fail"}
        )
        raise HTTPException(status_code=400, detail="Invalid input data")
    if len(CACHE) > 30:
        CACHE.pop(0)
    return {"result": result}


@app.get("/history")
async def history(limit: Optional[int]=None, status: Optional[str]=None):
    """History execution"""

    return history_support(CACHE, limit, status)
