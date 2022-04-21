from datetime import datetime
from typing import Optional

from fastapi import FastAPI
from services.sevices import StartlinkService

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/satelites/{satelite_id}")
def read_item(
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
