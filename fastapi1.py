from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Optional

app = FastAPI()

class Item(BaseModel):
    id: Optional[int] = None
    name: str
    price: float
    is_offer: Optional[bool] = None

items_db: Dict[int, Item] = {}
last_id = 0

@app.post("/items/", response_model=Item)
def create_item(item: Item):
    global last_id
    last_id += 1

    new_item = Item(
        id=last_id,
        name=item.name,
        price=item.price,
        is_offer=item.is_offer
    )

    items_db[last_id] = new_item
    return new_item

@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return items_db[item_id]

@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: Item):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")

    updated_item = Item(
        id=item_id,
        name=item.name,
        price=item.price,
        is_offer=item.is_offer
    )

    items_db[item_id] = updated_item
    return updated_item

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")

    del items_db[item_id]
    return {"detail": "Item deleted"}