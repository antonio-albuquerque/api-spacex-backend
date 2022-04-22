from datetime import datetime
from sqlalchemy import select
from haversine import haversine
from database.models import StarlinkTrackingHistory
from database.config import Session


class StartlinkService(StarlinkTrackingHistory):
    @staticmethod
    def satelite_exists(satelite_id: str) -> bool:
        session = Session()
        return (
            session.execute(
                select(StarlinkTrackingHistory).filter(
                    StarlinkTrackingHistory.satelite_id == satelite_id
                )
            ).fetchone()
            is not None
        )

    @staticmethod
    def get_last_known_location(
        creation_date: str, satelite_id: str
    ) -> StarlinkTrackingHistory:
        session = Session()

        last_known_location = (
            select(StarlinkTrackingHistory)
            .filter(StarlinkTrackingHistory.satelite_id == satelite_id)
            .filter(
                StarlinkTrackingHistory.creation_date
                <= datetime.strptime(creation_date, "%Y/%m/%d %H:%M:%S")
            )
            .order_by(StarlinkTrackingHistory.creation_date.desc())
        )

        results = session.execute(last_known_location)
        return results.fetchone()

    @staticmethod
    def get_nearest_satelite(
        creation_date: str, latitude: float, longitude: float
    ) -> StarlinkTrackingHistory:
        session = Session()

        all_locations = session.execute(
            select(
                StarlinkTrackingHistory.satelite_id,
                StarlinkTrackingHistory.latitude,
                StarlinkTrackingHistory.longitude,
                StarlinkTrackingHistory.id,
                StarlinkTrackingHistory.creation_date,
            ).filter(
                StarlinkTrackingHistory.creation_date
                <= datetime.strptime(creation_date, "%Y/%m/%d %H:%M:%S")
            )
        ).fetchall()

        min_distance = None

        for location in all_locations:
            lat = location[1]
            lon = location[2]
            distance = haversine((lat, lon), (latitude, longitude))

            if not min_distance or distance <= min_distance:
                min_distance = distance
                nearest_satelite = location

        print(nearest_satelite)

        return {
            "id": nearest_satelite[3],
            "satelite_id": nearest_satelite[0],
            "latitude": nearest_satelite[1],
            "longitude": nearest_satelite[2],
            "creation_date": nearest_satelite[4],
            "distance": min_distance,
            "unit": "kilometers",
            "message": "Success",
        }
