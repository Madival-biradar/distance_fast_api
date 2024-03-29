from typing import List, Optional
from fastapi import FastAPI, HTTPException, Query, Depends
from geopy.distance import geodesic
import sys
from models import *
from db_connections import *
from utils import *
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s: %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

Base.metadata.create_all(bind=engine)

app = FastAPI()

#methods to stop the or exit the terminal in FASTAPI
def receive_signal(signalNumber, frame):
    logger.debug('received',signalNumber)
    sys.exit()

@app.on_event("startup")
async def startup_event():
    import signal
    signal.signal(signal.SIGINT, receive_signal)


@app.post("/addresses/", response_model=AddressInDB)
def create_new_address(address: AddressCreate, db = Depends(get_db)):
    logger.debug("creating address")
    return create_address(db, address)

@app.put("/addresses/{address_id}", response_model=AddressInDB)
def update_existing_address(address_id: int, address: AddressUpdate, db = Depends(get_db)):
    logger.debug(address_id)
    return update_address(db, address, address_id)

@app.delete("/addresses/{address_id}")
def delete_existing_address(address_id: int, db = Depends(get_db)):
    logger.debug(address_id)
    return delete_address(db, address_id)

@app.get("/addresses/", response_model=List[AddressInDB])
def get_all_addresses(skip: int = 0, limit: int = 10, db = Depends(get_db)):
    logger.debug("fetching the all records")
    return get_addresses(db, skip, limit)

@app.get("/addresses/{place}")
def get_single_address(place: str, db = Depends(get_db)):
    logger.debug(place)
    logger.debug(type(place))
    place1_db = db.query(Address).filter(func.lower(Address.name) == place.lower()).first()
    if place1_db is None:
        raise HTTPException(status_code=404, detail=f"{place}  not found")
    return place1_db


@app.get("/addresses/distance/{latitude}/{longitude}/{distance}",response_model=List[AddressInDB])
def calculate_distance(latitude: float, longitude: float, distance: int, db = Depends(get_db)):
    logger.debug(latitude,longitude,distance)
    places_within_distance = get_places_within_distance(db, latitude, longitude, distance)
    return places_within_distance