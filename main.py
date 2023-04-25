from fastapi import FastAPI, File, UploadFile, Form
from deepface import DeepFace
import io
import os
from PIL import Image
import mysql.connector
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import asyncio

app = FastAPI()
load_dotenv()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db_config = {
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'host': os.getenv('MYSQL_HOST'),
    'database': os.getenv('MYSQL_DATABASE')
}

loop = asyncio.get_event_loop()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post('/upload')
async def upload(picture: UploadFile = File(...), EmpID: str = Form(...), Pin: str = Form(...), Device: str = Form(...)):
    save_path = '/tksgolry/Deepface/assets/'+picture.filename
    image_bytes = await picture.read()
    image_pil = Image.open(io.BytesIO(image_bytes))
    image_pil = image_pil.rotate(270, expand=True)
    if os.path.exists(save_path):
        os.remove(save_path)
    image_pil.save(save_path)

    try:
        faces = DeepFace.extract_faces(save_path , detector_backend='opencv')
    except ValueError as e:
        if "Face could not be detected" in str(e):
            os.remove(save_path)
            return {"message": "Error: " + str(e)}
            # return {"message": "Error"}
        else:
            raise e
        
    if faces:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        query = f"SELECT * FROM account WHERE Pincode = '{Pin}' AND EmployeeID = '{EmpID}' AND Device = '{Device}'"
        cursor.execute(query)
        results = cursor.fetchall()
        img1_path = f"/tksgolry/Deepface/assets/{picture.filename}"

        if results:
            try:
                update_query = f"UPDATE account SET Pincode = '{Pin}', Image = '{img1_path}', Device = '{Device}' WHERE EmployeeID = '{EmpID}'"
                cursor.execute(update_query)
                conn.commit()
                return {'message': 'File uploaded successfully'}
            except Exception as e:
                print(e)
                conn.rollback()
                return {'message': 'Failed to update database'}
        else:
            try:
                insert_query = f"INSERT INTO account (EmployeeID, Pincode, Image, Device) VALUES ('{EmpID}', '{Pin}', '{img1_path}', '{Device}')"
                cursor.execute(insert_query)
                conn.commit()
                return {'message': 'File uploaded successfully'}
            except Exception as e:
                print(e)
                conn.rollback()
                return {'message': 'Failed to update database'}
        conn.close()
    else: 
        os.remove(save_path)
        return {'message': 'Image and data uploaded successfully'}

@app.post("/verify")
async def verify(image: UploadFile = File(...)):
    img1_path = f"/tksgolry/Deepface/assets/{image.filename}"
    img2_path = f'/tksgolry/Deepface/assets/Verify_{image.filename}'
    image_bytes = await image.read()
    image_pil = Image.open(io.BytesIO(image_bytes))
    image_pil = image_pil.rotate(270, expand=True)
    image_pil.save(img2_path)
    try:
        result = await loop.run_in_executor(None, DeepFace.verify, img1_path, img2_path, "Facenet512")
    except ValueError as e:
        if "Face could not be detected" in str(e):
            os.remove(img2_path)
            return {"message": "Error: " + str(e)}
        else:
            raise e
    if result.get("verified") == True:
        os.remove(img2_path)
        return {"message": "Face match!!"}
    else:
        os.remove(img2_path)
        return {"message": "Face not match!!"}

# {
#     'verified': True, 
#     'distance': 0.14848632356763147, 
#     'threshold': 0.3, 
#     'model': 'Facenet512', 
#     'detector_backend': 'opencv', 
#     'similarity_metric': 'cosine', 
#     'facial_areas': {'img1': {'x': 179, 'y': 1031, 'w': 1685, 'h': 1685}, 
#                      'img2': {'x': 1901, 'y': 3612, 'w': 62, 'h': 62}}, 
#     'time': 5.29
# }