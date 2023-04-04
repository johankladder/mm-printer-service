
from sqlalchemy import Column, Integer, String
from .database import Base


class Printer(Base):

    __tablename__ = "printers"

    id = Column(Integer, primary_key=True, index=True)
    readable_name = Column(String)
    progressor_identifier = Column(String)
    remote_identifier = Column(String)
