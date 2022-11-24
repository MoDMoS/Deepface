import streamlit as st
from PIL import Image
from deepface import DeepFace


def verify() :
    result = DeepFace.verify(img1_path = "img1.jpg", img2_path = "img2.jpg")
    if(result.get("verified") == True) :
        return "Face match!!" 
    else :
        return "Face not match!!" 

st.set_page_config(page_title="Face Verification")
st.title('Face Verification')
st.header('Face Verification')
image_1 = st.file_uploader("Choose a image 1")
if image_1 is not None:
    img1 = Image.open(image_1)
    img1 = img1.save("img1.jpg")
    st.image(image_1)
image_2 = st.file_uploader("Choose a image 2")
if image_2 is not None:
    img2 = Image.open(image_2)
    img2 = img2.save("img2.jpg")
    st.image(image_2)



if st.button('Predict'):
    Verify = verify()
    st.text(Verify)