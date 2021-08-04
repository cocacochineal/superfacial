import streamlit as st
import numpy as np
import app2
import requests
import json

from PIL import Image, ImageDraw
    

with st.form("my_form"):
    col1, col2, col3= st.beta_columns(3)
    options=np.zeros(52)
    c1=[]
    c2=[]
    c3=[]
    for i in range(1, 55):
        if(i%3==0):
            c1.append(i-2)
            c2.append(i-1)
            c3.append(i)
    with col1:
        for i in c1:
            st.image(Image.open(f'pics/interface_face/{i}.jpg'), width=200)
            options[i-1]=st.checkbox(f'Like?{i}')
    with col2:
        for i in c2:
            st.image(Image.open(f'pics/interface_face/{i}.jpg'), width=200)
            options[i-1]=st.checkbox(f'Like?{i}')
    with col3:
        for i in c3:
            st.image(Image.open(f'pics/interface_face/{i}.jpg'), width=200)
            options[i-1]=st.checkbox(f'Like?{i}')
        
    submitted = st.form_submit_button("Submit")

if submitted:
    # prediction = requests.post(url, files=params).json()
    st.write(options)
    params={'options_': options}
    url='https://superfacial-api.herokuapp.com/form'
    form_submit= requests.post(url, data=params).json()   
    st.write(form_submit)

uploaded_file = st.file_uploader("Choose an image file")
if uploaded_file is not None:
    image = uploaded_file.read()
    params = {'image': image}
    url='https://superfacial-api.herokuapp.com/image/'
    # make sure requests is using the correct method: post or get
    prediction = requests.post(url, files=params).json()      
    #st.write(prediction) 
    pil_image=Image.open(uploaded_file)
    d = ImageDraw.Draw(pil_image)
    results=prediction[0]
    face_landmarks_list = prediction[1]
    i=0
    for i in range(0,len(face_landmarks_list)):
        result =results[i]
        if result>0.6:
            color='red'
            txt=f"{result}"
        else:
            color='green'
            txt=f"{result}"
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
    