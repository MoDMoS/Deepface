# import streamlit as st
from PIL import Image
from deepface import DeepFace

models = "Facenet"

def verify() :
    result = DeepFace.verify(img1_path = "img1.jpg", img2_path = "img1.jpg", model_name = models)
    print(result)

Verify = verify()