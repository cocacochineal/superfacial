import streamlit as st
import numpy as np
import app2
import requests
import json
from PIL import Image, ImageDraw
    

with st.form("my_form"):
    col1, col2, col3= st.beta_columns(3)
    options=np.zeros(5)
    with col1:
        st.image(Image.open('/Users/shan/code/shan-gao-qd/superfacial/raw_data/1.jpg'), width=200)
        options[0]=st.checkbox('Like?1')
        st.image(Image.open('/Users/shan/code/shan-gao-qd/superfacial/raw_data/6.jpg'), width=200)
        options[3] = st.checkbox('Like?4')
    with col2:
        st.image(Image.open('/Users/shan/code/shan-gao-qd/superfacial/raw_data/2.jpg'), width=200)
        options[1] = st.checkbox('Like?2')  
        st.image(Image.open('/Users/shan/code/shan-gao-qd/superfacial/raw_data/7.jpg'), width=200)
        options[4] = st.checkbox('Like?5')
    with col3:
        st.image(Image.open('/Users/shan/code/shan-gao-qd/superfacial/raw_data/3.jpg'), width=200)
        options[2] = st.checkbox('Like?3')
        
    submitted = st.form_submit_button("Submit")

if submitted:
    st.write('submitted')
uploaded_file = st.file_uploader("Choose an image file")
if uploaded_file is not None:
    image = uploaded_file.read()
    params = {'image': image}
    url='http://127.0.0.1:8000/image'
    # make sure requests is using the correct method: post or get
    prediction = requests.post(url, files=params).json()       
    pil_image=Image.open(uploaded_file)
    d = ImageDraw.Draw(pil_image)
    results=prediction[0]
    face_landmarks_list = prediction[1]
    i=0
    for i in range(0,len(face_landmarks_list)):
        result =results[i]
        if result==0:
            color='red'
            txt='not match'
        else:
            color='green'
            txt='match'
        osd = Image.new("RGB", (100,25), color)
        dctx = ImageDraw.Draw(osd)  # create drawing context
        dctx.text((5, 5), txt,  fill="black") 
        x=face_landmarks_list[i]['left_eyebrow'] 
        (a,b)=[sum(y) / len(y) for y in zip(*x)]
        a=int(a)
        b=int(b)-25
        pil_image.paste(
        osd,
        box=(a, b, osd.size[0] + a, osd.size[1] + b),
        mask=Image.new("L", osd.size, 192))
        i+=1
    st.image(pil_image)
    