from datetime import datetime
from sqlalchemy import select
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
                < datetime.strptime(creation_date, "%Y/%m/%d %H:%M:%S")
            )
        )

        results = session.execute(last_known_location)
        return results.fetchone()
