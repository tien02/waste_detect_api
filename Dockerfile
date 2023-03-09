FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
COPY ./requirements.txt /app/requirements.txt

COPY ./*.sh /app/

RUN pip install --no-cache-dir -r /app/requirements.txt
# RUN bash install.sh

COPY ./*.py /app/

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]