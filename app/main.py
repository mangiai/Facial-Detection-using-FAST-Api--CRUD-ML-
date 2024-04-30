from fastapi import FastAPI
from .routes import user_routes, auth_routes, image_routes

app = FastAPI()

# Include API routers
app.include_router(user_routes.router, prefix="/users", tags=["Users"])
app.include_router(auth_routes.router, prefix="/auth", tags=["Authentication"])
app.include_router(image_routes.router, prefix="/images", tags=["Image Processing"])
