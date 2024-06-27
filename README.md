# MLOps Case Study

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
Go to the [ml-service](ml-service) directory to prepare and test a `Model` artifact.

Build the `ml-service` image with `ModelServer` that will be serving a model through the REST API:
```shell
docker buildx build -t ml-service --progress plain -f ml-service.Dockerfile .
```

To verify the image:
```shell
docker image ls ml-service
```

To rebuild the image from scratch:
```shell
docker buildx build -t ml-service --progress plain --no-cache --pull -f ml-service.Dockerfile .
```

To run the containerized Inference Service:
```shell
docker run -it -p 8080:8080 ml-service
```

Once the service starts you can open the `/metrics` endpoint in your browser: http://localhost:8080/metrics and observe how the endpoint behaves.

To test the REST API run the simple script (a cURL replacement on Windows):
```shell
python try_ml_service.py
```

The output should be:
```text
<Response [200]>
{"predictions":[8,9,8]}
```

### Batch Inference Pipeline
Go to the [ml-pipelines](ml-pipelines) directory to build and test the `pipelines` components.

Build the `ml-pipelines` image with the components that will be used in the batch prediction pipeline:
```shell
docker buildx build -t ml-pipelines --progress plain -f ml-pipelines.Dockerfile .
```

To verify the image:
```shell
docker image ls ml-pipelines
```

You can also run it to see if it works as expected:
```shell
docker run -it ml-pipelines
```

To rebuild the image from scratch:
```shell
docker buildx build -t ml-pipelines --progress plain --no-cache --pull -f ml-pipelines.Dockerfile .
```

To run the pipeline, first you need to start the Inference Service:
```shell
docker run -it -p 8080:8080 ml-service
```

Once the service is ready, run the batch pipeline:
```shell
python batch_inference_pipeline.py
```
The output should look like this:
```text
(mlops-dev) ..\mlops-case-study>python batch_inference_pipeline.py
Starting the pipeline...
Pipeline: PreProcessor step starting...
Pipeline: PreProcessor step DONE!
Pipeline: ModelScore step starting...
Pipeline: ModelScore step DONE!
Pipeline: PostProcessor step starting...
Pipeline: PostProcessor step DONE!
Pipeline DONE!
```

### Monitoring and Observability
* Logging, emitting metrics, proper app instrumentation and monitoring -> to be discussed

### Software Development standards
* Testing - showed a proper structure -> details to be discussed
* Code Quality
  * focused on a good repo layout and code structure
  * DRY needed (lack of time)
  * details to be discussed
* Documentation
  * skipped (lack of time) included only some docstrings -> to be discussed

### Fine-tuning of the model
* I recommend performing HPO with [Optuna](https://optuna.org/) framework
