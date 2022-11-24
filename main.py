from fastapi import FastAPI
from deepface import DeepFace
app = FastAPI()


@app.get("/verify/{img1,img2}")
async def verify(img1, img2):
    result = DeepFace.verify(img1_path = img1, img2_path = img2)
    if(result.get("verified") == True) :
        return {"message": "Face match!!"}
    else :
        return {"message": "Face not match!!"}