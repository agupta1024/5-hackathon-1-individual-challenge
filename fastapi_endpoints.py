from fastapi import APIRouter
from fastapi.responses import JSONResponse
from request_handler import RequestHandle
import json

request_handle = RequestHandle()

stars_router = APIRouter()

# --- Endpoint 1: Get Raw Stars Data ---
# Full path will be: /{org}/stars
@stars_router.get("/stars")
def list_stars(org: str):
    # The 'org' path variable is passed automatically because of how the router is mounted.
    print(f"Listing stars for an {org}.")
    data = request_handle.process_endpoint(organisation=org, endpoint="list_all")
    return JSONResponse(
            content=data,
            status_code=200,
        )

@stars_router.get("/avg")
def get_avg(org: str):
    # The 'org' path variable is passed automatically because of how the router is mounted.
    print(f"Get avg no. of stargazers for an {org}.")
    data = request_handle.process_endpoint(organisation=org, endpoint="avg")
    return JSONResponse(
            content={'avg' : data},
            status_code=200,
        )

@stars_router.get("/min")
def get_min(org):
    """
    Get the minimum number of stargazers among all repositories.
    
    Args:
        org (str): GitHub organization name (passed as URL parameter).
        
    Returns:
        Response: JSON response containing the minimum stargazer count.
    """
    # This route will eventually be accessed via '/<org>/stars/'
    print(f"Min for an {org}.")
    data = request_handle.process_endpoint(organisation=org, endpoint="min")
    print(f"{data=}")
    return JSONResponse(
            content={'min' : data},
            status_code=200,
        )

@stars_router.get("/max")
def get_min(org):
    print(f"Max for an {org}.")
    data = request_handle.process_endpoint(organisation=org, endpoint="max")
    return JSONResponse(
            content={'max' : data},
            status_code=200,
        )

@stars_router.get("/std")
def get_std(org):
    """
    Calculate and return the standard deviation of stargazer counts.
    
    Args:
        org (str): GitHub organization name (passed as URL parameter).
        
    Returns:
        Response: JSON response containing the standard deviation rounded to 2 decimal places.
    """
    # This route will eventually be accessed via '/<org>/stars/'
    print(f"Std for an {org}.")
    data = request_handle.process_endpoint(organisation=org, endpoint="std")
    return JSONResponse(
            content={'std' : round(data,2)},
            status_code=200,
        )

@stars_router.get("/argmin")
def argmin_data(org):
    """
    Get the repository with the minimum number of stargazers.
    
    Args:
        org (str): GitHub organization name (passed as URL parameter).
        
    Returns:
        Response: JSON response containing the name of the repository with minimum stargazers.
    """
    # This route will eventually be accessed via '/<org>/stars/'
    print(f"argmin for an {org}.")
    data = request_handle.process_endpoint(organisation=org, endpoint="argmin")
    return JSONResponse(
            content={'argmin' : data},
            status_code=200,
        )

@stars_router.get("/argmax")
def argmax(org):
    """
    Get the repository with the maximum number of stargazers.
    
    Args:
        org (str): GitHub organization name (passed as URL parameter).
        
    Returns:
        Response: JSON response containing the name of the repository with maximum stargazers.
    """
    # This route will eventually be accessed via '/<org>/stars/'
    print(f"Argmax for an {org}.")
    data = request_handle.process_endpoint(organisation=org, endpoint="argmax")
    return JSONResponse(
            content={'argmax' : data},
            status_code=200,
        )