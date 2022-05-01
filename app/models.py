import logging
import time
from typing import List

from sqlalchemy import Column, DateTime, Integer, create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

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
    customer_id = Column(Integer)
    count = Column(Integer)

    def __repr__(self):
        return (
            f"PageLoads(created_ts={self.created_ts}, ts={self.ts}, customer_id={self.customer_id}, count={self.count})"
        )


class Clicks(Base):
    __tablename__ = "clicks"
    id = Column(Integer, primary_key=True)
    created_ts = Column(DateTime())
    ts = Column(DateTime())
    customer_id = Column(Integer)
    count = Column(Integer)

    def __repr__(self):
        return f"Clicks(created_ts={self.created_ts}, ts={self.ts}, customer_id={self.customer_id}, count={self.count})"


class UniqueUserClicks(Base):
    __tablename__ = "unique_user_clicks"
    id = Column(Integer, primary_key=True)
    created_ts = Column(DateTime())
    ts = Column(DateTime())
    customer_id = Column(Integer)
    count = Column(Integer)

    def __repr__(self):
        return f"UniqueUserClicks(created_ts={self.created_ts}, ts={self.ts}, customer_id={self.customer_id}, count={self.count})"


class ClickThroughRate(Base):
    __tablename__ = "click_through_rate"
    id = Column(Integer, primary_key=True)
    created_ts = Column(DateTime())
    ts = Column(DateTime())
    customer_id = Column(Integer)
    count = Column(Integer)

    def __repr__(self):
        return f"ClickThroughRate(created_ts={self.created_ts}, ts={self.ts}, customer_id={self.customer_id}, count={self.count})"


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


def save_unique_user_clicks(session: SessionLocal, unique_user_clicks: List[UniqueUserClicks]) -> None:
    session.bulk_save_objects(unique_user_clicks)
    session.commit()
    logging.info("Saved %s unique user clicks", len(unique_user_clicks))


def save_click_through_rate(session: SessionLocal, click_through_rate: List[ClickThroughRate]) -> None:
    session.bulk_save_objects(click_through_rate)
    session.commit()
    logging.info("Saved %s click through rate", len(click_through_rate))


def save_reports(
    page_loads: List[PageLoads],
    clicks: List[Clicks],
    unique_user_clicks: List[UniqueUserClicks],
    click_through_rate: List[ClickThroughRate],
) -> None:
    with SessionLocal() as session:
        save_page_loads(session, page_loads)
        save_clicks(session, clicks)
        save_unique_user_clicks(session, unique_user_clicks)
        save_click_through_rate(session, click_through_rate)
