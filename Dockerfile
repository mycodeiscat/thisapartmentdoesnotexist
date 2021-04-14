FROM python:3.8

WORKDIR /thisapartmentdoesnotexist

COPY requirements.txt ./
RUN pip3 install -r requirements.txt

RUN export PYTHONPATH='${PYTHONPATH}:/thisapartmentdoesnotexist'

COPY . .

CMD ["python", "./backend/app.py"]