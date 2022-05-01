import datetime
import logging
import os
from typing import List, Tuple

import pandas as pd

from app.models import Clicks, ClickThroughRate, PageLoads, UniqueUserClicks
from app.settings import Settings

CLICK = "ReferralRecommendClick"
PAGE_LOAD = "ReferralPageLoad"

logger = logging.getLogger(__name__)

DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "aklamio_challenge.json")

CLICK_THROUGH_WINDOW = pd.Timedelta(seconds=Settings().click_through_window_seconds)


def calculate_statistics() -> Tuple[List[PageLoads], List[Clicks], List[UniqueUserClicks], List[ClickThroughRate]]:

    logger.info("Importing data")
    with open(DATA_FILE) as f:
        df = pd.read_json(f, lines=True)

    logger.info("Calculating statistics")

    df = df[df["fired_at"] >= datetime.datetime(2022, 1, 1)]
    df["hour"] = df["fired_at"].apply(lambda x: x.replace(minute=0, second=0))

    clicks = []
    page_loads = []
    unique_user_clicks = []
    click_through_rate = []

    page_loads_df = df[df["event_type"] == PAGE_LOAD].copy()
    clicks_df = df[df["event_type"] == CLICK].copy()
    g = page_loads_df.groupby(["hour", "customer_id"])["user_id"].count()
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

    g = clicks_df.groupby(["hour", "customer_id"])["user_id"].count()
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

    g = clicks_df.groupby(["hour", "customer_id"])["user_id"].nunique()
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

    clicks_df["is_related"] = 0
    for row in clicks_df.itertuples():
        # TODO: iterating over rows in pandas is not very fast, we should think about more efficient solution,
        # but our amount of data is processed reasonable time
        index = row[0]
        fired_at_end = row[3]
        customer_id = row[2]
        user_id = row[4]
        fired_at_start = fired_at_end - CLICK_THROUGH_WINDOW

        is_related = int(
            (
                (page_loads_df["fired_at"] >= fired_at_start)
                & (page_loads_df["fired_at"] <= fired_at_end)
                & (page_loads_df["customer_id"] == customer_id)
                & (page_loads_df["user_id"] == user_id)
            ).any()
        )
        clicks_df.loc[index, "is_related"] = is_related

    g = clicks_df.groupby(["hour", "customer_id"])["is_related"].sum()
    for index, value in g.items():
        ts, customer_id = index
        click_through_rate.append(
            ClickThroughRate(
                created_ts=datetime.datetime.now(),
                ts=ts,
                customer_id=customer_id,
                count=value,
            )
        )

    logger.info("Calculated page loads, first 5 are %s", page_loads[:5])
    logger.info("Calculated clicks, first 5 are %s", clicks[:5])
    logger.info("Calculated unique_user_clicks, first 5 are %s", unique_user_clicks[:5])
    logger.info("Calculated click_through_rate, first 5 are %s", click_through_rate[:5])
    logger.info("Statistics were successfully calculated")
    return page_loads, clicks, unique_user_clicks, click_through_rate
