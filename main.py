from typing import List, Optional
from fastapi import FastAPI, HTTPException, Query, Depends
from geopy.distance import geodesic
import sys
from models import *
from db_connections import *
from utils import *


Base.metadata.create_all(bind=engine)

app = FastAPI()

#methods to stop the or exit the terminal in FASTAPI
def receive_signal(signalNumber, frame):
    print('Received:', signalNumber)
    sys.exit()

@app.on_event("startup")
async def startup_event():
    import signal
    signal.signal(signal.SIGINT, receive_signal)


@app.post("/addresses/", response_model=AddressInDB)
def create_new_address(address: AddressCreate, db = Depends(get_db)):
    return create_address(db, address)

@app.put("/addresses/{address_id}", response_model=AddressInDB)
def update_existing_address(address_id: int, address: AddressUpdate, db = Depends(get_db)):
    return update_address(db, address, address_id)

@app.delete("/addresses/{address_id}")
def delete_existing_address(address_id: int, db = Depends(get_db)):
    return delete_address(db, address_id)

@app.get("/addresses/", response_model=List[AddressInDB])
def get_all_addresses(skip: int = 0, limit: int = 10, db = Depends(get_db)):
    return get_addresses(db, skip, limit)

@app.get("/addresses/{place}")
def get_single_address(place: str, db = Depends(get_db)):
    place1_db = db.query(Address).filter(func.lower(Address.name) == place.lower()).first()
    if place1_db is None:
        raise HTTPException(status_code=404, detail=f"{place}  not found")
    return place1_db


@app.get("/addresses/distance/{place1}/{place2}")
def calculate_distance(place1: str, place2: str, db = Depends(get_db)):
    place1_db = db.query(Address).filter(func.lower(Address.name) == place1.lower()).first()
    place2_db = db.query(Address).filter(func.lower(Address.name) == place2.lower()).first()

    if place1_db is None or place2_db is None:
        return "places not found , add them sorry for INCONVIENCE!!"

    # Calculate the distance between the places
    coords1 = (float(place1_db.latitude), float(place1_db.longitude))
    coords2 = (float(place2_db.latitude), float(place2_db.longitude))
    distance = geodesic(coords1, coords2).kilometers

    return f'{place1} and {place2} are {distance} KM far away from each other'

