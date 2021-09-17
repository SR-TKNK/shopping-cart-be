FROM python:3.8
COPY . .
RUN apt-get update
RUN apt install -y libgl1-mesa-glx
RUN pip install -r requirements.txt
RUN pip install uvicorn[standard]
CMD [ "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "10400" ]