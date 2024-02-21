from typing import List, Optional
from fastapi import FastAPI, HTTPException, Query, Depends
from geopy.distance import geodesic
import sys
from models import *
from db_connections import *
from utils import *


Base.metadata.create_all(bind=engine)

app = FastAPI()

def receive_signal(signalNumber, frame):
    print('Received:', signalNumber)
    sys.exit()

@app.on_event("startup")
async def startup_event():
    import signal
    signal.signal(signal.SIGINT, receive_signal)
    # startup tasks

# API Endpoints
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

@app.get("/addresses/{address_id}", response_model=AddressInDB)
def get_single_address(address_id: int, db = Depends(get_db)):
    db_address = get_address(db, address_id)
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return db_address


@app.get("/addresses/distance/{place1}/{place2}")
def calculate_distance(place1: str, place2: str, db = Depends(get_db)):
    # Query the database for the places
    place1_db = db.query(Address).filter(Address.name == place1).first()
    place2_db = db.query(Address).filter(Address.name == place2).first()

    # Calculate the distance between the places
    coords1 = (float(place1_db.latitude), float(place1_db.longitude))
    coords2 = (float(place2_db.latitude), float(place2_db.longitude))
    distance = geodesic(coords1, coords2).kilometers

    return f'{place1} and {place2} are {distance} KM far away from each other'








# @app.get("/addresses/distance/")
# def get_addresses_within_distance(
#     latitude: float,
#     longitude: float,
#     distance: Optional[float] = Query(..., gt=0),
#     db = Depends(get_db)
# ):
#     addresses = get_addresses(db)
#     valid_addresses = []
#     for address in addresses:
#         address_coordinates = (address.latitude, address.longitude)
#         given_coordinates = (latitude, longitude)
#         if geodesic(given_coordinates, address_coordinates).miles <= distance:
#             valid_addresses.append(address)
#     return valid_addresses
