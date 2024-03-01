from fastapi import  HTTPException, Query, Depends
from models import *
from db_connections import *



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_address(db, address_id: int):
    return db.query(Address).filter(Address.id == address_id).first()

def get_addresses(db, skip: int = 0, limit: int = 10):
    return db.query(Address).offset(skip).limit(limit).all()

def create_address(db, address: AddressCreate):
    db_address = Address(**address.dict())
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address

def update_address(db, address: AddressUpdate, address_id: int):
    db_address = db.query(Address).filter(Address.id == address_id).first()
    if db_address:
        for key, value in address.dict().items():
            setattr(db_address, key, value)
        db.commit()
        db.refresh(db_address)
        return db_address
    else:
        raise HTTPException(status_code=404, detail="Address not found")

def delete_address(db, address_id: int):
    db_address = db.query(Address).filter(Address.id == address_id).first()
    if db_address:
        db.delete(db_address)
        db.commit()
        return {"message": "Address deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Address not found")
    

def get_places_within_distance(db, latitude: float, longitude: float, distance: int):
    places = db.query(Address).all()
    places_within_distance = []
    try:
        for place in places:
            coords1 = (latitude, longitude)
            coords2 = (place.latitude, place.longitude) 
            distance_found = geodesic(coords1, coords2).kilometers
            if distance_found <= distance:
                places_within_distance.append({
                    "id": place.id,
                    "latitude": place.latitude,
                    "longitude": place.longitude,
                    "name": place.name
                })
        print(places_within_distance)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail="something went wrong")
    finally: 
        print(f'successfull executed, we found  {len(places_within_distance)} cities')
    return places_within_distance