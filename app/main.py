from fastapi import FastAPI, Depends, HTTPException, File, UploadFile, status
from fastapi.responses import StreamingResponse, Response, JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from PIL import Image
from io import BytesIO
from .auth import get_current_user, authenticate_user, create_access_token
from . import crud, models, schemas, database
from .schemas import UserCreate
from .image_processing import detect_faces, crop_face, detect_and_crop_face
import numpy as np
import cv2
import jwt
models.Base.metadata.create_all(bind=database.engine)


app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def authenticate_user(username: str, password: str):
    if username == "admin" and password == "secret":
        return {"username": username}  # Correctly return a dictionary
    return None

def create_access_token(data: dict):
    encoded_jwt = jwt.encode(data, "secret", algorithm="HS256")
    return encoded_jwt

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user['username']})  # Corrected access
    return {"access_token": access_token, "token_type": "bearer"}




def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.exception_handler(Exception)
async def exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"message": "An error occurred: " + str(exc)},
    )

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password"
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user_name=user.name)

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.post("/upload-image/")
async def process_image_upload(file: UploadFile = File(...)):
    try:
        # Load the image from the uploaded file
        image = Image.open(BytesIO(await file.read()))
        
        # Process the image to detect faces
        face_count = detect_faces(image)  # Example usage
        
        return {"faces_detected": face_count}
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e)})
    
def crop_face(image: Image.Image):
    image_cv = np.array(image)
    gray = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    if len(faces) == 0:
        return None

    # Crop the first face
    (x, y, w, h) = faces[0]
    face = image_cv[y:y+h, x:x+w]
    cropped_image = Image.fromarray(cv2.cvtColor(face, cv2.COLOR_BGR2RGB))

    return cropped_image

@app.post("/upload-and-return-image/")
async def upload_and_return_image(file: UploadFile = File(...)):
    try:
        # Read the image from the uploaded file
        contents = await file.read()
        image_stream = BytesIO(contents)
        image = Image.open(image_stream)

        # Save the processed image to a byte stream to return it as a response
        img_byte_arr = BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)  # Important: move to the start of the BytesIO object

        # Create a StreamingResponse object
        return StreamingResponse(img_byte_arr, media_type="image/png")

    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})
    
@app.post("/upload-and-crop-face/")
async def upload_and_crop_face(file: UploadFile = File(...)):
    try:
        # Load the image from the uploaded file
        contents = await file.read()
        image_stream = BytesIO(contents)
        image = Image.open(image_stream)

        # Detect and crop the face
        cropped_image = detect_and_crop_face(image)

        if cropped_image:
            # Prepare the cropped image for response
            img_byte_arr = BytesIO()
            cropped_image.save(img_byte_arr, format='PNG')
            img_byte_arr.seek(0)

            return StreamingResponse(img_byte_arr, media_type="image/png")
        else:
            return JSONResponse(status_code=404, content={"message": "No face detected"})

    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})