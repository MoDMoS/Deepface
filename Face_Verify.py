import streamlit as st
import pandas as pd
import tensorflow as tf
import numpy as np
import cv2
from tensorflow import keras
from PIL import Image
from mtcnn import MTCNN
from keras_vggface.utils import preprocess_input
from keras_vggface.vggface import VGGFace
from scipy.spatial.distance import cosine

detector = MTCNN()

def extract_face(image, resize=(224, 224)) :
    image = cv2.imread(image)
    faces = detector.detect_faces(image)
    x1, y1, width, height = faces[0]['box']
    x2, y2 = x1 + width, y1 + height

    face_boundary = image[y1:y2, x1:x2]

    face_image = cv2.resize(face_boundary, resize)

    return face_image

def get_embeddings(faces) :
    face = np.asarray(faces, 'float32')

    face = preprocess_input(face, version=2)

    model = VGGFace(model='resnet50', include_top=False, input_shape=(224, 224, 3), pooling='avg')

    return model.predict(face)

def get_similarity(faces) :
    embeddings = get_embeddings(faces)

    score = cosine(embeddings[0], embeddings[1])

    if score <= 0.5 :
        return "Face Matched", score
    return "Face Not Matched", score

st.set_page_config(page_title="Face Verification")
st.title('Face Verification')
st.header('Face Verification')
image_1 = st.file_uploader("Choose a image 1")
if image_1 is not None:
    img = Image.open(image_1)
    img = img.save("img1.jpg")
    st.image(image_1)
image_2 = st.file_uploader("Choose a image 2")
if image_2 is not None:
    img = Image.open(image_2)
    img = img.save("img2.jpg")
    st.image(image_2)



if st.button('Predict'):
    faces = [extract_face(img) for img in ["img1.jpg", "img2.jpg"]]
    Predict = get_similarity(faces)
    st.text(Predict)