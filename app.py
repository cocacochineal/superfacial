import streamlit as st
import numpy as np
import app2
import requests
import json

from PIL import Image, ImageDraw, ImageFont
    
st.markdown('# Choose 10 faces you like (please be **superfacial**!) :heart_eyes:')
with st.form("my_form"):
    
    col1, col2, col3, = st.beta_columns(3)
    options=np.zeros(52)
    c1=[]
    c2=[]
    c3=[]
    
    for i in range(1, 52):
        if(i%3==0):
            c1.append(i-2)
            c2.append(i-1)
            c3.append(i)
            # c4.append(i)
    # for i in range(1, 13):
    #     # if(i%4==0):
    #     #     c1.append(i-3)
    #     #     c2.append(i-2)
    #     #     c3.append(i-1)
    #     #     c4.append(i)
    c3.append(52)
    with col1:
        for i in c1:
            st.image(Image.open(f'pics/interface_face/{i}.jpg'), width=150)
            options[i-1]=st.checkbox(f'Like?', key=f"{i}")
    with col2:
        for i in c2:
            st.image(Image.open(f'pics/interface_face/{i}.jpg'), width=150)
            options[i-1]=st.checkbox(f'Like?', key=f"{i}")
    with col3:
        for i in c3:
            st.image(Image.open(f'pics/interface_face/{i}.jpg'), width=150)
            options[i-1]=st.checkbox(f'Like?', key=f"{i}")
        # with col4:
        #     # for i in c4:
        #     st.image(Image.open(f'pics/interface_face/{c4[i-1]}.jpg'), width=150)
        #     options[i-1]=st.checkbox(f'Like?', key=f"{c4[i-4]}")
    # with col2:
    #         # for i in c4:
    #         st.image(Image.open(f'pics/interface_face/52.jpg'), width=150)
    #         options[i-1]=st.checkbox(f'Like?', key="52")
        
    submitted = st.form_submit_button("Submit")

if submitted:
    # prediction = requests.post(url, files=params).json()
    #st.write(options)
    params={'options_': list(options)}
    #params=json.dumps({'options_': list(options)})
    url='http://139.198.183.85:5000/form/'
    #url = 'http://localhost:8005/form'
    #st.write(requests.get(url))
    form_submit= requests.post(url, data=params).json()
    #st.write(form_submit)
    st.title('Now, you match...')

if st.button('Your Le Wagon Match'):
        
    #url = 'http://localhost:8005/wagon'
    url='http://139.198.183.85:5000/wagon/'
    # make sure requests is using the correct method: post or get
    prediction = requests.get(url).json()      
    #st.write(prediction) 
    pil_image=Image.open('wagon.jpeg')
    d = ImageDraw.Draw(pil_image)
    #st.write(prediction)
    results=prediction[0]
    face_landmarks_list = prediction[1]
    print(results)
    print(face_landmarks_list)
    first_in=results.index(sorted(results)[-1])
    i=0
    snd_in=results.index(sorted(results)[-2])
    third_in=results.index(sorted(results)[-3])
    for i in range(0,len(face_landmarks_list)):
        result =results[i]
        if i==first_in:
            color='green'
            txt="#1 MATCH!"
        elif i==snd_in:
            color='green'
            txt="#2 MATCH"
        elif i==third_in:
            color='green'
            txt="#3 MATCH"
        else:
            color='red'
            txt="not match..."
        osd = Image.new("RGB", (130,35), color)
        font = ImageFont.truetype(r'arial.ttf', 20) 
        dctx = ImageDraw.Draw(osd)  # create drawing context
        dctx.text((10, 10), txt,  fill="black", font=font) 
        x=face_landmarks_list[i]['left_eyebrow'] 
        (a,b)=[sum(y) / len(y) for y in zip(*x)]
        a=int(a)
        b=int(b)-35
        pil_image.paste(
        osd,
        box=(a, b, osd.size[0] + a, osd.size[1] + b),
        mask=Image.new("L", osd.size, 192))
        i+=1
    st.image(pil_image)
    st.balloons()
    

uploaded_file = st.file_uploader("Predict on your own chosen image")
if uploaded_file is not None:
    image = uploaded_file.read()
    params = {'image': image}
    #url = 'http://localhost:8005/image'
    url='http://139.198.183.85:5000/image/'
    # make sure requests is using the correct method: post or get
    prediction = requests.post(url, files=params).json()      
    #st.write(prediction) 
    pil_image=Image.open(uploaded_file)
    d = ImageDraw.Draw(pil_image)
    #st.write(prediction)
    results=prediction[0]
    face_landmarks_list = prediction[1]
    print(results)
    print(face_landmarks_list)
    i=0
    if len(results)==1:
        if results[0]>=0.5:
            color='green'
            txt="MATCH!"
        else:
            color='red'
            txt="not match..."
        osd = Image.new("RGB", (130,35), color)
        font = ImageFont.truetype(r'arial.ttf', 20) 
        dctx = ImageDraw.Draw(osd)  # create drawing context
        dctx.text((10, 5), txt,  fill="black", font=font) 
        x=face_landmarks_list[i]['left_eyebrow'] 
        (a,b)=[sum(y) / len(y) for y in zip(*x)]
        a=int(a)
        b=int(b)-35
        pil_image.paste(
        osd,
        box=(a, b, osd.size[0] + a, osd.size[1] + b),
        mask=Image.new("L", osd.size, 192))
    elif len(results)<5:
        first_in=results.index(sorted(results)[-1])
        for i in range(0,len(face_landmarks_list)):
            result =results[i]
            if i==first_in:
                color='green'
                txt="#1 MATCH!"
            elif results>=0.5:
                color='green'
                txt="MATCH"
            else:
                color='red'
                txt="not match..."
            osd = Image.new("RGB", (100,25), color)
            font = ImageFont.truetype(r'arial.ttf', 20) 
            dctx = ImageDraw.Draw(osd)  # create drawing context
            dctx.text((10, 5), txt,  fill="black", font=font) 
            x=face_landmarks_list[i]['left_eyebrow'] 
            (a,b)=[sum(y) / len(y) for y in zip(*x)]
            a=int(a)
            b=int(b)-25
            pil_image.paste(
            osd,
            box=(a, b, osd.size[0] + a, osd.size[1] + b),
            mask=Image.new("L", osd.size, 192))
            i+=1
    else:             
        first_in=results.index(sorted(results)[-1])
        snd_in=results.index(sorted(results)[-2])
        third_in=results.index(sorted(results)[-3])
        for i in range(0,len(face_landmarks_list)):
            result =results[i]
            if i==first_in:
                color='green'
                txt="#1 MATCH!"
            elif i==snd_in:
                color='green'
                txt="#2 MATCH"
            elif i==third_in:
                color='green'
                txt="#3 MATCH"
            else:
                color='red'
                txt="not match..."
            osd = Image.new("RGB", (100,25), color)
            dctx = ImageDraw.Draw(osd)  # create drawing context
            font = ImageFont.truetype(r'arial.ttf', 20) 
            dctx.text((10, 5), txt,  fill="black", font=font) 
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
    
# else:
#     st.write('Goodbye')    
