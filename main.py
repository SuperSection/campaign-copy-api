from datetime import datetime
from random import randint
from typing import Any

from fastapi import FastAPI, HTTPException, Response

app = FastAPI(root_path="/api/v1")


data: Any = [
    {
        "campaign_id": 1,
        "name": "Summer Launch",
        "due_date": datetime.now(),
        "created_at": datetime.now(),
    },
    {
        "campaign_id": 2,
        "name": "Black Friday",
        "due_date": datetime.now(),
        "created_at": datetime.now(),
    },
]


@app.get("/")
async def root():
    return {"message": "Ad Copy API!"}


@app.get("/campaigns")
async def read_campaigns():
    return {"campaigns": data}


@app.get("/campaigns/{id}")
async def read_campaign(id: int):
    for campaign in data:
        if campaign.get("campaign_id") == id:
            return {"campaign": campaign}
    raise HTTPException(status_code=404)


@app.post("/campaigns", status_code=201)
async def create_campaign(body: dict[str, Any]):

    new: Any = {
        "campaign_id": randint(100, 1000),
        "name": body.get("name"),
        "due_date": body.get("due_date"),
        "created_at": datetime.now(),
    }

    data.append(new)
    return {"campaign": new}


@app.put("/campaigns/{id}")
async def update_campaign(id: int, body: dict[str, Any]):

    for index, campaign in enumerate(data):
        if campaign.get("campaign_id") == id:

            updated_campaign: Any = {
                "campaign_id": id,
                "name": body.get("name"),
                "due_date": (
                    body.get("due_date")
                    if body.get("due_date") is not None
                    else campaign.get("due_date")
                ),
                "created_at": campaign.get("created_at"),
            }
            data[index] = updated_campaign
            return {"campaign": updated_campaign}

    raise HTTPException(status_code=404)


@app.delete("/campaigns/{id}")
async def delete_campaign(id: int):

    for index, campaign in enumerate(data):
        if campaign.get("campaign_id") == id:
            data.pop(index)
            return Response(status_code=204)

    raise HTTPException(status_code=404)
