import streamlit as st
import requests
import json
from PIL import Image

uploaded_file = st.file_uploader("Choose an image file")

if uploaded_file is not None:
    image = uploaded_file.read()
    st.image(Image.open(uploaded_file))
    params = {'image': image}
    url='http://127.0.0.1:8000/image'
    # make sure requests is using the correct method: post or get
    prediction = requests.post(url, files=params)
    st.write(prediction.text)