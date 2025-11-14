from flask import Flask, Blueprint, Response
from flask import request, url_for
from markupsafe import escape
from request_handler import RequestHandle
import json

request_handle = RequestHandle()

stars_bp = Blueprint('stars', __name__, url_prefix='/stars')
avg_bp = Blueprint('avg', __name__, url_prefix='/avg')
min_bp = Blueprint('min', __name__, url_prefix='/min')
max_bp = Blueprint('max', __name__, url_prefix='/max')
std_bp = Blueprint('std', __name__, url_prefix='/std')
argmin_bp = Blueprint('argmin', __name__, url_prefix='/argmin')
argmax_bp = Blueprint('argmax', __name__, url_prefix='/argmax')
health_bp = Blueprint('healthz', __name__, url_prefix='/healthz')


# Define your routes using only the *relative* path
@stars_bp.route('/')
def list_stars(org):
    """
    List all repositories and their stargazer counts for a given organization.
    
    Args:
        org (str): GitHub organization name (passed as URL parameter).
        
    Returns:
        Response: JSON response containing a dictionary mapping repository names to stargazer counts.
    """
    # This route will eventually be accessed via '/<org>/stars/'
    print(f"Listing stars for an {org}.")
    data = request_handle.process_endpoint(organisation=org, endpoint="list_all")
    return Response(
            response=json.dumps(data),
            status=200,
            mimetype="application/json",
        )

@avg_bp.route('/')
def get_avg(org):
    """
    Calculate and return the average number of stargazers across all repositories.
    
    Args:
        org (str): GitHub organization name (passed as URL parameter).
        
    Returns:
        Response: JSON response containing the average stargazer count rounded to 2 decimal places.
    """
    # This route will eventually be accessed via '/<org>/stars/'
    print(f"Get avg no. of stargazers for an {org}.")
    data = request_handle.process_endpoint(organisation=org, endpoint="avg")
    return Response(
            response=json.dumps({'avg' : round(data, 2)}),
            status=200,
            mimetype="application/json",
        )

@min_bp.route('/')
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
    return Response(
            response=json.dumps({'min' : data}),
            status=200,
            mimetype="application/json",
        )

@max_bp.route('/')
def get_max(org):
    """
    Get the maximum number of stargazers among all repositories.
    
    Args:
        org (str): GitHub organization name (passed as URL parameter).
        
    Returns:
        Response: JSON response containing the maximum stargazer count.
    """
    # This route will eventually be accessed via '/<org>/stars/'
    print(f"Max for an {org}.")
    data = request_handle.process_endpoint(organisation=org, endpoint="max")
    return Response(
            response=json.dumps({'max' : data}),
            status=200,
            mimetype="application/json",
        )

@std_bp.route('/')
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
    return Response(
            response=json.dumps({'std' : round(data,2)}),
            status=200,
            mimetype="application/json",
        )

@argmin_bp.route('/')
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
    return Response(
            response=json.dumps({'argmin' : data}),
            status=200,
            mimetype="application/json",
        )

@argmax_bp.route('/')
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
    return Response(
            response=json.dumps({'argmax' : data}),
            status=200,
            mimetype="application/json",
        )

@health_bp.route('/')
def health_check():
    """
    Health check endpoint to verify the API is running and responsive.
    
    Returns:
        Response: JSON response with a 'healthy' status message.
    """
    data = request_handle.process_endpoint(organisation=None, endpoint="healthz")
    return Response(
            response=json.dumps({'status': data}),
            status=200,
            mimetype="application/json",
        )
