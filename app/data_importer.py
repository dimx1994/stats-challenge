import datetime
import logging
import os
from typing import List, Tuple

import pandas as pd

from app.models import Clicks, PageLoads, UniqueUserClicks

CLICK = "ReferralRecommendClick"
PAGE_LOAD = "ReferralPageLoad"

logger = logging.getLogger(__name__)

data_file = os.path.join(os.path.dirname(__file__), "data", "aklamio_challenge.json")


def calculate_statistics() -> Tuple[
    List[PageLoads], List[Clicks], List[UniqueUserClicks]
]:

    logger.info("Importing data")
    with open(data_file) as f:
        df = pd.read_json(f, lines=True)

    logger.info("Calculating statistics")

    df = df[df["fired_at"] >= datetime.datetime(2022, 1, 1)]
    df["hour"] = df["fired_at"].apply(lambda x: x.replace(minute=0, second=0))
    # g = df.groupby(["hour", "customer_id", "event_type"])["event_type"].count()
    clicks = []
    page_loads = []
    unique_user_clicks = []

    g = (
        df[df["event_type"] == PAGE_LOAD]
        .groupby(["hour", "customer_id"])["user_id"]
        .count()
    )
    for index, value in g.items():
        ts, customer_id = index
        page_loads.append(
            PageLoads(
                created_ts=datetime.datetime.now(),
                ts=ts,
                customer_id=customer_id,
                count=value,
            )
        )

    g = (
        df[df["event_type"] == CLICK]
        .groupby(["hour", "customer_id"])["user_id"]
        .count()
    )
    for index, value in g.items():
        ts, customer_id = index
        clicks.append(
            Clicks(
                created_ts=datetime.datetime.now(),
                ts=ts,
                customer_id=customer_id,
                count=value,
            )
        )

    g = (
        df[df["event_type"] == CLICK]
        .groupby(["hour", "customer_id"])["user_id"]
        .nunique()
    )
    for index, value in g.items():
        ts, customer_id = index
        unique_user_clicks.append(
            UniqueUserClicks(
                created_ts=datetime.datetime.now(),
                ts=ts,
                customer_id=customer_id,
                count=value,
            )
        )

    logger.info("Calculated page loads, first 5 are %s", page_loads[:5])
    logger.info("Calculated clicks, first 5 are %s", clicks[:5])
    logger.info("Calculated unique_user_clicks, first 5 are %s", unique_user_clicks[:5])
    return page_loads, clicks, unique_user_clicks
