from sqlalchemy import Float, Integer, Column, DateTime
from geoalchemy2 import Geography
from database.config import Base


class StarlinkTrackingHistory(Base):
    __tablename__ = "starlink_tracking_history"

    id = Column(Integer, primary_key=True)
    creation_date = Column(DateTime, nullable=False)
    location = Column(
        Geography(geometry_type="POINT", srid=4326), nullable=False
    )  # SRID 4326 is used in GPSs
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    def __repr__(self) -> str:
        return f"<StarlinkTrackingHistory(\
            id='{self.id}',\
            latitude='{self.latitude}',\
            longitude='{self.longitude}')> "
