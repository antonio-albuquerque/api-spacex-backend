from datetime import datetime
from typing import Optional
from zipapp import create_archive

from fastapi import FastAPI
from api.schema import NearestSatelite, Satelite
from services.sevices import StartlinkService

app = FastAPI()


@app.get("/satelites/{satelite_id}", response_model=Satelite)
def get_satelite_by_id(
    satelite_id: str,
    creation_date: Optional[str] = datetime.strftime(
        datetime.now(), "%Y/%m/%d %H:%M:%S"
    ),
):
    satelite_exists = StartlinkService.satelite_exists(satelite_id)

    if satelite_exists:
        last_known_location = StartlinkService.get_last_known_location(
            creation_date=creation_date, satelite_id=satelite_id
        )

        if last_known_location:
            return {
                "id": last_known_location.StarlinkTrackingHistory.id,
                "satelite_id": last_known_location.StarlinkTrackingHistory.satelite_id,
                "creation_date": last_known_location.StarlinkTrackingHistory.creation_date,
                "latitude": last_known_location.StarlinkTrackingHistory.latitude,
                "longitude": last_known_location.StarlinkTrackingHistory.longitude,
                "message": "Success.",
            }
        else:
            return {
                "message": f"No track record found for satelite '{satelite_id}' before {creation_date}."
            }

    else:
        return {"message": f"Satelite '{satelite_id}' not found."}


@app.get("/satelites", response_model=NearestSatelite)
def get_closest_satelite(
    latitude: float,
    longitude: float,
    creation_date: Optional[str] = datetime.strftime(
        datetime.now(), "%Y/%m/%d %H:%M:%S"
    ),
):
    nearest_satelite = StartlinkService.get_nearest_satelite(
        creation_date=creation_date,
        latitude=latitude,
        longitude=longitude,
    )
    return nearest_satelite
