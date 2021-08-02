import streamlit as st
import requests
import json
from PIL import Image, ImageDraw

def app():
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
            