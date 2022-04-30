import datetime
import logging
import os
from typing import List, Tuple

import pandas as pd

from app.models import Clicks, PageLoads

CLICK = "ReferralRecommendClick"
PAGE_LOAD = "ReferralPageLoad"

logger = logging.getLogger(__name__)

data_file = os.path.join(os.path.dirname(__file__), "data", "aklamio_challenge.json")


def calculate_statistics() -> Tuple[List[Clicks], List[PageLoads]]:

    logger.info("Importing data")
    with open(data_file) as f:
        df = pd.read_json(f, lines=True)
    logger.info("Calculating statistics")

    df = df[df["fired_at"] >= datetime.datetime(2022, 1, 1)]
    df["hour"] = df["fired_at"].apply(lambda x: x.replace(minute=0, second=0))
    g = df.groupby(["hour", "customer_id", "event_type"])["event_type"].count()
    clicks = []
    page_loads = []
    for index, value in g.items():
        ts, user_id, name = index
        if name == CLICK:
            clicks.append(
                Clicks(
                    created_ts=datetime.datetime.now(),
                    ts=ts,
                    user_id=user_id,
                    count=value,
                )
            )
        if name == PAGE_LOAD:
            page_loads.append(
                PageLoads(
                    created_ts=datetime.datetime.now(),
                    ts=ts,
                    user_id=user_id,
                    count=value,
                )
            )
    logger.info("Calculated clicks, first 5 are %s", clicks[:5])
    logger.info("Calculated page loads, first 5 are %s", page_loads[:5])
    return clicks, page_loads
