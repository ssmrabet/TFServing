# TFServing

## RESNET Model
[I got the pre-trained RESNET pb model from here](https://storage.googleapis.com/download.tensorflow.org/models/official/20181001_resnet/savedmodels/resnet_v2_fp32_savedmodel_NHWC_jpg.tar.gz)

## Other Models

for more models you can check this link
[Lets check the link](https://github.com/tensorflow/serving/tree/master/tensorflow_serving/servables/tensorflow/testdata)

## Download TFServing 

First we need to pull an image of tensorflow serving
```bash
docker pull tensorflow/serving
```

## Run Models with Serving

--mount type=bind,source=<model location on host>,target=<model location in container>
the location of the ML model on the host machine is bound to the location to which it will be copied onto in the docker container

-e MODEL_NAME=<model name>
the environmental variable representing the model name is explicitly changed to whatever name we've chosen to call our model 

-t tensorflow/serving
we specify that we are running tensorFlow serving

### Run one model

```bash
docker run -p 8501:8501 --name tfserving_resnet \
--mount type=bind,source=/tmp/resnet,target=/models/resnet \
-e MODEL_NAME=resnet -t tensorflow/serving &
```

We have to check that this two local links for our two models so we gonna find that our models are available:
http://localhost:8501/v1/models/resnet
http://localhost:8501/v1/models/half_plus_two

Now we're gonna test resnet pre-trained model with this client code
```bash
python3 resnet_client.py
```

### Run two or more models

```bash
docker run -p 8501:8501 --name tfserving_models \
--mount type=bind,source=/tmp/half_plus_two,target=/models/half_plus_two \
--mount type=bind,source=/tmp/resnet,target=/models/resnet \
--mount type=bind,source=/tmp/model_config.config,target=/models/model_config.config \
-t tensorflow/serving \
--model_config_file=/models/model_config.config &
```

We can test with the same client code for resnet pre-trained model
```bash
python3 resnet_client.py
```

### To check the difference without serving

resnet_client_without_serving.py it's a sample to calculate resnet pre-trained pb model latency

```bash
python3 resnet_client_without_serving.py
```
  
## Run models with docker.yml file
  
You need to use this method if you are looking to relate your tf serving to a flask project docker image or any other type of project

First, you need to create a network to use it in all related projects
```bash
docker network create test-network
```
  
Second, create your docker.yml file configs
  
```bash
version: "1"
networks:
  test-network:
    driver: bridge
services:
  serving:
    image: tensorflow/serving:latest
    restart: unless-stopped
    ports:
      - 8500:8500
      - 8501:8501
    volumes:
      - ./models:/models  # --> this folder is where yout put all your models
      - ./models.config:/models.config  # --> this is the config file
    command:
      - "bash -c"
      - "--model_config_file=/models.config"
      - "--model_config_file_poll_wait_seconds=60"
    networks:
      - test-network
  flask-project-image:  # --> the name of your flask project image
    image: flask-project-image  # --> the name of your flask project image
    ports:
      - port:port  # --> port used in the docker image
    networks:
      - test-network  # --> relate this image with the same network
```

Finally, launch this command line
```bash
docker run -it --rm --name image-name -p port:port --network test-network -v /Path-to-the-project/src:/code image-of-flask-project:version
```
