# Waste Detectioni API

## Tools

* Model: [Yolov5](https://github.com/ultralytics/yolov5)

* Dataset: [TACO](http://tacodataset.org) trash detection dataset

* API: [fastapi](https://fastapi.tiangolo.com)

## Run

### Run on local

```
bash uvicorn_run.sh
```

### Run on Docker

1. Build docker image

```
bash build.sh
```

2. Run docker container

```
bash run.sh
```

or run in interative mode to custom the 
```
bash run_it_mode.sh
```