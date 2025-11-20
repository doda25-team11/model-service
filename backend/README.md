# SMS Checker / Backend

The backend of this project provides a simple REST service that can be used to detect spam messages.
We have extended the base project [rohan8594/SMS-Spam-Detection](https://github.com/rohan8594/SMS-Spam-Detection), which introduces several basic classification models, and wrap one of them in a microservice.

The following sections will explain you how to get started.
The project **requires a Python 3.12 environment** to run (tested with 3.12.9).
Use the `requirements.txt` file to restore the required dependencies in your environment.


### Training the Model

To train the model, you have two options.
Either you create a local environment...

    $ python -m venv venv
    $ source venv/bin/activate
    $ pip install -r requirements.txt

... or you train in a Docker container (recommended):

    $ docker run -it --rm -v ./:/root/sms/ python:3.12.9-slim bash
    ... (container startup)
    $ cd /root/sms/
    $ pip install -r requirements.txt

Once all dependencies have been installed, the data can be preprocessed and the model trained by creating the output folder and invoking three commands:

    $ mkdir output
    $ python src/read_data.py
    Total number of messages:5574
    ...
    $ python src/text_preprocessing.py
    [nltk_data] Downloading package stopwords to /root/nltk_data...
    [nltk_data]   Unzipping corpora/stopwords.zip.
    ...
    $ python src/text_classification.py

The resulting model files will be placed as `.joblib` files in the `output/` folder.


### Serving Recommendations

To make the models accessible, you need to start the microservice by running the `src/serve_model.py` script from within the virtual environment that you created before, or in a fresh Docker container (recommended):

    $ docker run -it --rm -p 8081:8081 -v ./:/root/sms/ python:3.12.9-slim bash
    ... (container startup)
    $ cd /root/sms/
    $ pip install -r requirements.txt
    $ python src/serve_model.py

The server will start on port 8081.
Once its startup has finished, you can either access [localhost:8081/apidocs](http://localhost:8081/apidocs) in your browser to interact with the service, or you send `POST` requests to request predictions, for example with `curl`:


    $ curl -X POST "http://localhost:8081/predict" -H "Content-Type: application/json" -d '{"sms": "test ..."}'
    {
      "classifier": "decision tree",
      "result": "ham",
      "sms": "test ..."
    }

## How to run the backend container (without Docker Compose)
First create the docker image.
```bash 
$ docker build .\backend\ -t model-service
```
Then, run the docker image on port 8081.
```bash
$ docker run -p 8081:8081 model-service
```
If you wish to run it on another port, do:
```bash
$ docker run -e MODEL_SERVICE_PORT=9000 -p 9000:9000 model-service
```
So this listens on port 9000.

## How to run the backend container with a volume mount

When running with the first command given above
```bash
$ docker run -p 8081:8081 model-service
```
there is no model provided so the docker file will download one from github releases (provided by F9)
For example from this link: [https://github.com/doda25-team11/model-service/releases/tag/model-20251118-102052]

To run with a volume mount, run the following command:
```bash
 $ docker run \                         
  -p 8081:8081 \
  -v (path to folder with models):/app/model \
  model-service
```
where the folder with models can be something like: backend/models that contains at least the following files:
- model.joblib
- preprocessor.joblib