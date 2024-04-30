from fastapi import APIRouter, File, UploadFile
from fastapi.responses import StreamingResponse, JSONResponse
from PIL import Image
from io import BytesIO
from ..image_processing import detect_faces, detect_and_crop_face

router = APIRouter()

@router.post("/upload-image")
async def process_image_upload(file: UploadFile = File(...)):
    image = Image.open(BytesIO(await file.read()))
    face_count = detect_faces(image)
    return {"faces_detected": face_count}

@router.post("/upload-and-return-image")
async def upload_and_return_image(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(BytesIO(contents))
    img_byte_arr = BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    return StreamingResponse(img_byte_arr, media_type="image/png")

@router.post("/predict")
async def upload_and_crop_face(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(BytesIO(contents))
    cropped_image = detect_and_crop_face(image)
    if cropped_image:
        img_byte_arr = BytesIO()
        cropped_image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        return StreamingResponse(img_byte_arr, media_type="image/png")
    else:
        return JSONResponse(status_code=404, content={"message": "No face detected"})
