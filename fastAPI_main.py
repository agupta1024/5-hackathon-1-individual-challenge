from fastapi import FastAPI
from fastapi_endpoints import stars_router
import uvicorn


app = FastAPI()

#    Mount the Router to the main application
#    This is where you define the full path, including the path parameter `<org>`.
#    The path is '/{org}/stars', which is the FastAPI equivalent of Flask's '/<org>/stars'.
app.include_router(
    stars_router,
    prefix="/{org}",  # Defines the full URL structure
    tags=["Stars Metrics"]
)

# Optional: Add a root endpoint for basic health checks
@app.get("/healthz")
def health_check():
    """
    Health check endpoint to verify the API is running and responsive.
    
    Returns:
        Response: JSON response with a 'healthy' status message.
    """
    return {'status': 'healthy'}

if __name__ == "__main__":
    uvicorn.run("fastAPI_main:app", port=8000)