from fastapi import FastAPI, File, UploadFile, Form
from deepface import DeepFace
import io
import os
from PIL import Image
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/verify")
async def verify(image: UploadFile = File(...)):
    img1_path = f"/tksgolry/Deepface/assets/{image.filename}"
    img2_path = f'/tksgolry/Deepface/assets/Verify_{image.filename}'
    image_bytes = await image.read()
    image_pil = Image.open(io.BytesIO(image_bytes))
    image_pil = image_pil.rotate(270, expand=True)
    image_pil.save(img2_path)
    try:
        result = DeepFace.verify(img1_path=img1_path, img2_path=img2_path, model_name="Facenet512")
    except ValueError as e:
        if "Face could not be detected" in str(e):
            os.remove(img2_path)
            return {"message": "Error: " + str(e)}
            # return {"message": "Error"}
        else:
            raise e
    if result.get("verified") == True:
        os.remove(img2_path)
        return {"message": "Face match!!"}
    else:
        return {"message": "Face not match!!"}