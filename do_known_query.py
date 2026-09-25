import logging
import os
from datetime import UTC, datetime
from typing import TypedDict

from dotenv import load_dotenv
from sqlalchemy import (
    Column,
    Integer,
    MetaData,
    String,
    Table,
    UniqueConstraint,
    create_engine,
    select,
)
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import sessionmaker
from sunpy.net import Fido, vso
from sunpy.net import attrs as a

logger = logging.getLogger(__name__)

load_dotenv()
DB_URL = os.getenv("DATABASE_URL")
if not DB_URL:
    raise RuntimeError("DATABASE_URL is not set")

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
metadata = MetaData()

known_queries_table = Table(
    "known_queries",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("Active", Integer),
    Column("Provider", String),
    Column("Source", String),
    Column("Instrument", String),
    Column("Date_End", String),
    Column("Date_Start", String),
    UniqueConstraint(
        "Provider", "Source", "Instrument", name="uq_provider_source_instrument"
    ),
)


# Define what this function returns. Note that because whatthis function returns
# is passed directly back thtough FastAPI, if you change this then you must also
# change the dpHealthResponseClass pydantic class in the file get_dp_health.py
class returnClass(TypedDict):
    provider: str
    source: str
    instrument: str
    status: str
    code: int
    startTime: str
    endTime: str
    execSec: float


# Add the final items to the return dict before retruning it.
def close_dict(return_dict, startTime, status, code):

    return_dict["status"] = status
    return_dict["code"] = code

    endTime = datetime.now(UTC)
    execSec = (endTime - startTime).total_seconds()

    return_dict["startTime"] = startTime.isoformat(timespec="milliseconds")
    return_dict["endTime"] = endTime.isoformat(timespec="milliseconds")
    return_dict["execSec"] = execSec


def vso_query(provider: str, source: str, instrument: str) -> returnClass:
    """
    Method to do a known query given a source/instrument.
    This is passed back to the user through an API, see
    the front end in get_dp_health.py
    """

    startTime = datetime.now(UTC)

    client = vso.VSOClient()

    return_dict = {
        "provider": provider,
        "source": source,
        "instrument": instrument,
    }

    t = known_queries_table.c
    stmt = select(t.Date_Start, t.Date_End).where(
        t.Provider == provider, t.Source == source, t.Instrument == instrument
    )
    with SessionLocal() as db:
        try:
            row = db.execute(stmt).one()
        except NoResultFound:
            row = None

    if row is None:
        close_dict(return_dict, startTime, "No such provider", -1)
        return return_dict

    (data_start_str, data_end_str) = row

    logger.info(
        "Known query data window for %s,%s,%s is %s to %s",
        provider,
        source,
        instrument,
        data_start_str,
        data_end_str,
    )

    data_start = datetime.strptime(data_start_str, "%Y-%m-%d %H:%M:%S.%f").replace(
        tzinfo=UTC
    )
    data_end = datetime.strptime(data_end_str, "%Y-%m-%d %H:%M:%S.%f").replace(
        tzinfo=UTC
    )

    # Run the query
    try:
        result = client.search(
            a.Time(data_start, data_end),
            a.Provider(provider),
            a.Source(source),
            a.Instrument(instrument),
        )
        # The comment below is a way to get ruff to accept a blind exception catch
    except Exception:
        logger.exception("Query threw exception")
        close_dict(return_dict, startTime, "Query threw an exception", -2)
        return return_dict

    if len(result) == 0:
        close_dict(return_dict, startTime, "Query returned zero results", -3)
        return return_dict

    # If we got here, the query worked.
    # print(f"Result size is {len(result)} :")
    # print(result)

    # Try to download data, see how that goes. Need to set overwrite=True or if the
    # data file already exists then the data will not be downloaded again.
    try:
        files = Fido.fetch(
            result, path="./out_tmp/{file}", progress=False, overwrite=True
        )
    except Exception:
        logger.exception(
            "Download for %s,%s,%s threw an exception",
            provider,
            source,
            instrument,
        )
        close_dict(return_dict, startTime, "Download threw an exception", -4)
        return return_dict

    if files.errors:
        close_dict(return_dict, startTime, "Download had errors", -5)
        return return_dict

    close_dict(return_dict, startTime, "OK", 0)
    return return_dict


class optionsClass(TypedDict):
    Provider: str
    Source: str
    Instrument: str


def vso_options() -> list[optionsClass]:
    """
    Method to get the provider/source/instrument options
    """

    t = known_queries_table.c
    stmt = (
        select(t.Provider, t.Source, t.Instrument)
        .where(t.Active > 0)
        .order_by(t.Provider, t.Source, t.Instrument)
    )
    with SessionLocal() as db:
        rows = db.execute(stmt).all()

    return [
        optionsClass(provider=r.Provider, source=r.Source, instrument=r.Instrument)
        for r in rows
    ]
