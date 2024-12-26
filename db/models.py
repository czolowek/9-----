from typing import Optional

from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base


class Room(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[int] = mapped_column()
    floor: Mapped[int] = mapped_column()
    type: Mapped[str] = mapped_column(String(50))
    squire: Mapped[Optional[float]] = mapped_column(nullable=True)
    img_name_origin: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    img_name: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    img_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    reserved: Mapped[bool] = mapped_column(Boolean(), default=False)
