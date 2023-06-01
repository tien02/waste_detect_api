# Waste Detectioni API

<p float="left">
  <img src="asset/img1.jpeg" height="200" />
  <img src="asset/img2.jpeg" height="200" /> 
  <img src="asset/img3.jpeg" height="200" />
  <img src="asset/img4.jpeg" height="200" />
</p>

## Tools

* Model: [Yolov8](https://ultralytics.com/yolov8)

* Dataset: [TACO](http://tacodataset.org) trash detection dataset

* API: [fastapi](https://fastapi.tiangolo.com)

## Type of waste

| # | Names |
|---|---|
| 0 | Metal |
| 1 | Plastic Bottle |
| 2 | Cigarette |
| 3 | Carton |
| 4 | Paper |
| 5 | Plastic Bag |
| 6 | Glass |
| 7 | Straw |
| 8 | Cap/Lid |
| 9 | Plastic things |
| 10 | Cup |
| 11 | Other trash |

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