import json
from database.config import Session
from database.models import StarlinkTrackingHistory

session = Session()

with open("starlink_historical_data.json") as file:
    file_content = json.load(file)
    for position in file_content:
        creation_date = position["spaceTrack"]["CREATION_DATE"]
        latitude = position["latitude"]
        longitude = position["longitude"]
        satelite_id = position["id"]

        starlink_track = StarlinkTrackingHistory(
            creation_date=creation_date,
            latitude=latitude or 0,
            longitude=longitude or 0,
            location=f"POINT({longitude or 0} {latitude or 0})",
            satelite_id=satelite_id,
        )

        session.add(starlink_track)

    session.commit()
