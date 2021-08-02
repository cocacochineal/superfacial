FROM python:3.7
# RUN cd ~ && \
#     mkdir -p dlib && \
#     git clone -b 'v19.9' --single-branch https://github.com/davisking/dlib.git dlib/ && \
#     cd  dlib/ && \
#     python3 setup.py install --yes USE_AVX_INSTRUCTIONS
COPY app.py app.py
COPY requirements.txt requirements.txt

RUN pip install -U pip
RUN pip install -r requirements.txt

ENTRYPOINT ["streamlit", "run"]

CMD ["app.py"]