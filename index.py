# import streamlit as st
# import os
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'
from PIL import Image
from deepface import DeepFace

models = "DeepFace"

def verify() :
    for i in range(0, 5) :
        if(i == 0) :
            print("1 : ", i, "\n")
            result = DeepFace.verify(img1_path = "img1.jpg", img2_path = "img1.jpg", model_name = models)
            print(result)
        else :
            print("2 : ", i, "\n")
            result = DeepFace.verify(img1_path = "img2.jpg", img2_path = "img1.jpg", model_name = models)
            print(result)

verify()