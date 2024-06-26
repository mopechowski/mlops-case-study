# MLOps Case Study

---

## Main components of the Solution

### Inference Service
- Hosts the model as an RESTful API service that allows users to submit new data and receive predictions from
  - Model training is not important here, it can be any simple example model or pretrained one from the web. 

### Batch Inference Pipeline
* Pipeline components/steps:
  * `Preprocessor` - prepares data
  * `ModelScorer` - performs the inference task, requests the model API
  * `Postprocessor` - saves inference results to a CSV file
* The pipeline should be modular and easily reused for additional model APIs or data sources
* Dockerization and Deployment:
  * The entire inference pipeline should be packaged into Docker image(s)
    * so it can be potentially used by different orchestration systems
  * Describe how the dockerized pipeline could be integrated into different orchestration systems (Airflow, Kubeflow, Sagemaker, Vertex AI).

### Monitoring and Observability
Implement (or describe) a monitoring and observability strategy:
* System to track the performance of the inference pipeline over time
* Set up rules to notify you of potential issues or performance degradation
* Monitor and analyze data to identify patterns and trends in pipeline behavior

### Software Development standards
* Testing
* Documentation
* Code Quality

### Bonus: Fine-tuning of the model
* Fine-tune the selected model to improve its predictive performance.
* Evaluate the fine-tuned model's performance and compare it to the original model.

---

## Python Environment

To create this Python dev [environment](environment.yml) from scratch run:
```shell
conda env create
```
To check conda envs:
```shell
conda env list && conda list
```
To update the env during development:
```shell
conda env update -n mlops-dev --prune
```

To recreate this env:
```shell
conda activate base && 
conda env remove -n mlops-dev && 
conda env create && 
conda env list && 
conda activate mlops-dev && 
conda list
```

---

## The Solution

### Inference Service
[WIP] Go to the [ml-service](ml-service) directory, prepare a model artifact and test a `Model`.

Build the ml-service image with `ModelServer` that will be serving a model through REST API:
```shell
docker buildx build -t ml-service --progress plain -f ml-service.Dockerfile .
```
To rebuild the image from scratch:
```shell
docker buildx build -t ml-service --progress plain --no-cache --pull -f Dockerfile .
```
To run `ModelServer` run:
```shell
docker run -it -p 8080:8080 ml-service
```

### Batch Inference Pipeline
WIP...
