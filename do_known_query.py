from datetime import UTC, datetime
from typing import TypedDict


# Define what this function returns. Note that because whatthis function returns
# is passed directly back thtough FastAPI, if you change this then you must also
# change the dpHealthResponseClass pydantic class in the file get_dp_health.py
class returnClass(TypedDict):
    instrument: str
    source: str
    status: str
    code: int
    startTime: str
    endTime: str
    execSec: float


def vso_query(instrument: str, source: str) -> returnClass:
    """
    Method to do a known query given a source/instrument.
    This is passed back to the user through an API, see
    the front end in get_dp_health.py
    """

    startTime = datetime.now(UTC)

    return_dict = {
        "source": source,
        "instrument": instrument,
        "status": "Good",
        "code": 0,
    }

    endTime = datetime.now(UTC)
    execSec = (endTime - startTime).total_seconds()

    return_dict["startTime"] = startTime.isoformat(timespec="milliseconds")
    return_dict["endTime"] = endTime.isoformat(timespec="milliseconds")
    return_dict["execSec"] = execSec

    return return_dict
