# TFServing

## RESNET Model
[Lets download the pre-trained RESNET pb model](https://storage.googleapis.com/download.tensorflow.org/models/official/20181001_resnet/savedmodels/resnet_v2_fp32_savedmodel_NHWC_jpg.tar.gz)

## Other Models

for more models you can check this link
[Lets check the link](https://github.com/tensorflow/serving/tree/master/tensorflow_serving/servables/tensorflow/testdata)

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

### To check the difference for without serving

resnet_client_without_serving.py it's a sample to calculate resnet pre-trained pb model latency

```bash
python3 resnet_client_without_serving.py
```