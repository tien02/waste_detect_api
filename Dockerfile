FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

COPY ./*.sh /app/

RUN bash install.sh

COPY ./*.py /app/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]