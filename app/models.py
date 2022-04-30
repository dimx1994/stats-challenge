import logging
import time
from typing import List

from sqlalchemy import Column, DateTime, Integer, create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

from app.settings import Settings

SQLALCHEMY_DATABASE_URL = Settings().sqlalchemy_database_uri

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class PageLoads(Base):
    __tablename__ = "page_loads"
    id = Column(Integer, primary_key=True)
    created_ts = Column(DateTime())
    ts = Column(DateTime())
    user_id = Column(Integer)
    count = Column(Integer)

    def __repr__(self):
        return f"PageLoads(created_ts={self.created_ts}, ts={self.ts}, user_id={self.user_id}, count={self.count})"


class Clicks(Base):
    __tablename__ = "clicks"
    id = Column(Integer, primary_key=True)
    created_ts = Column(DateTime())
    ts = Column(DateTime())
    user_id = Column(Integer)
    count = Column(Integer)

    def __repr__(self):
        return f"Clicks(created_ts={self.created_ts}, ts={self.ts}, user_id={self.user_id}, count={self.count})"


def create_all_models_waiting_postgres() -> None:
    """
    Postgres initialization in docker could take some time so we have to wait
    """
    for _ in range(10):
        try:
            logging.info("Creating all dbs")
            Base.metadata.create_all(bind=engine)
            break
        except OperationalError:
            logging.info("Waiting for postres")
            time.sleep(1)


def save_page_loads(session: SessionLocal, page_loads: List[PageLoads]) -> None:
    session.bulk_save_objects(page_loads)
    session.commit()
    logging.info("Saved %s page loads", len(page_loads))


def save_clicks(session: SessionLocal, clicks: List[Clicks]) -> None:
    session.bulk_save_objects(clicks)
    session.commit()
    logging.info("Saved %s clicks", len(clicks))


def save_reports(page_loads: List[PageLoads], clicks: List[Clicks]) -> None:
    with SessionLocal() as session:
        save_page_loads(session, page_loads)
        save_clicks(session, clicks)
