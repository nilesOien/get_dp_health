from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

import do_known_query

# Set up tags that appear in the documentation pages that FastAPI generates.
tags_metadata = [
    {
        "name": "getDPhealthApp",
        "description": "Virtual Solar Observatory data provider test end point.",
        "externalDocs": {
            "description": "Small test web site",
            "url": "http://localhost:8004",
        },
    },
    {
        "name": "get-dp-health-get",
        "description": "The API end point using the GET method.",
    },
    {
        "name": "get-dp-health-post",
        "description": "The API end point using the POST method",
    },
    {
        "name": "dp-health-options",
        "description": "Get all the provider/source/instrument options for known queries",
    },
]


# Get an application object
getDPhealthApp = FastAPI(
    title="getDPhealth",
    summary="An API to test the response from a Virtual Solar Observatory (VSO) data provider (DP).",
    description="The API returns the result of a query to the DP.",
    contact={
        "name": "Virtual Solar Observatory",
        "url": "https://virtualsolar.org",
        "email": "vso@virtualsolar.org",
    },
    version="1.0.0",
    openapi_tags=tags_metadata,
)


# Pydantic class (inherits from BaseModel) that defines our response schema.
# Lets the documentation be more detailed.
class dpHealthResponseClass(BaseModel):
    """
    This defines the schema for the JSON response.
    """

    provider: str
    source: str
    instrument: str
    status: str
    code: int
    execSec: float
    startTime: str
    endTime: str


# The GET service front end, passes arguments back to do_known_query.vso_query() and returns the result.
@getDPhealthApp.get(
    "/get-dp-health-get",
    response_model=dpHealthResponseClass,
    tags=["get-dp-health-get"],
)
async def health_status_get(
    provider: str = Query(..., min_length=1, description="VSO provider"),
    source: str = Query(..., min_length=1, description="VSO source"),
    instrument: str = Query(..., min_length=1, description="VSO instrument"),
):
    """
    Returns the JSON response for a GET request.
    """
    return do_known_query.vso_query(provider, source, instrument)


# The POST service front end, passes arguments back to do_known_query.vso_query() and returns the result.
class dpHealthRequestClass(BaseModel):
    """
    This class defines what is passed into a POST request
    """

    provider: str = Field(..., min_length=1, description="VSO provider")
    source: str = Field(..., min_length=1, description="VSO source (required)")
    instrument: str = Field(..., min_length=1, description="VSO instrument (required)")


@getDPhealthApp.post(
    "/get-dp-health-post",
    response_model=dpHealthResponseClass,
    tags=["get-dp-health-post"],
)
async def health_status_post(request: dpHealthRequestClass):
    """
    Returns the JSON response for a POST request.
    """
    return do_known_query.vso_query(
        request.provider, request.source, request.instrument
    )


# Simple GET end point that shows options for provider, source, instrument for which we have a known query
class optionsResponseClass(BaseModel):
    """
    This defines the schema for the options JSON response.
    """

    provider: str
    source: str
    instrument: str


@getDPhealthApp.get(
    "/dp-health-options",
    response_model=list[optionsResponseClass],
    tags=["dp-health-options"],
)
async def dp_health_options():
    """
    Returns the options for provider, source and instrument in JSON format.
    """
    return do_known_query.vso_options()


# Simple web page that allows a query to be tested
getDPhealthApp.mount(
    "/",
    StaticFiles(directory="view_page", html=True, follow_symlink=True),
    name="viewpage",
)
