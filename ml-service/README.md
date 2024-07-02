# Inference Service

The Inference Service has been developed as a simplified and minimal version of `SKLearnModel` and is based on the [KServe's Scikit-Learn Server](https://github.com/kserve/kserve/tree/master/python/sklearnserver) Python package. [KServe Python Server](https://github.com/kserve/kserve/tree/master/python/kserve#kserve-python-server) implements a standardized library that is extended by model serving frameworks such as Scikit Learn, XGBoost, PyTorch and others. It encapsulates data plane API definitions and storage retrieval for models.

It provides many functionalities, including among others:
* Registering a model and starting the server
* Prediction Handler
* Pre/Post Processing Handler
* Liveness Handler
* Readiness Handlers
* Metrics and Logging

## Development and testing
For development and testing install the [sklearnserver](src/sklearnserver) from source in editable mode:
```shell
pip install -e .
```
To run basic `SKLearnModel` tests run:
```shell
pytest -W ignore
```
To prepare a model artifact for `ModelServer` run the [prepare_model.py](prepare_model.py) script:
```shell
python prepare_model.py
```

To see usage and all available CLI options:
```shell
python -m sklearnserver --help
```
```shell
usage: __main__.py [-h] [--http_port HTTP_PORT] [--grpc_port GRPC_PORT] [--workers WORKERS] [--max_threads MAX_THREADS]
                   [--max_asyncio_workers MAX_ASYNCIO_WORKERS] [--enable_grpc ENABLE_GRPC] [--enable_docs_url ENABLE_DOCS_URL]
                   [--enable_latency_logging ENABLE_LATENCY_LOGGING] [--configure_logging CONFIGURE_LOGGING] [--log_config_file LOG_CONFIG_FILE]
                   [--access_log_format ACCESS_LOG_FORMAT] [--model_name MODEL_NAME] [--predictor_host PREDICTOR_HOST] [--protocol {v1,v2,grpc-v2}]
                   [--predictor_protocol {v1,v2,grpc-v2}] [--predictor_use_ssl PREDICTOR_USE_SSL]
                   [--predictor_request_timeout_seconds PREDICTOR_REQUEST_TIMEOUT_SECONDS] --model_dir MODEL_DIR

options:
  -h, --help            show this help message and exit
  --http_port HTTP_PORT
                        The HTTP Port listened to by the model server.
  --grpc_port GRPC_PORT
                        The GRPC Port listened to by the model server.
  --workers WORKERS     The number of uvicorn workers for multi-processing.
  --max_threads MAX_THREADS
                        The max number of gRPC processing threads.
  --max_asyncio_workers MAX_ASYNCIO_WORKERS
                        The max number of asyncio workers to spawn.
  --enable_grpc ENABLE_GRPC
                        Enable gRPC for the model server.
  --enable_docs_url ENABLE_DOCS_URL
                        Enable docs url '/docs' to display Swagger UI.
  --enable_latency_logging ENABLE_LATENCY_LOGGING
                        Enable a log line per request with preprocess/predict/postprocess latency metrics.
  --configure_logging CONFIGURE_LOGGING
                        Enable to configure KServe and Uvicorn logging.
  --log_config_file LOG_CONFIG_FILE
                        File path containing UvicornServer's log config. Needs to be a yaml or json file.
  --access_log_format ACCESS_LOG_FORMAT
                        The asgi access logging format. It allows to override only the `uvicorn.access`'s format configuration with a richer set of fields  
  --model_name MODEL_NAME
                        The name of the model used on the endpoint path.
  --predictor_host PREDICTOR_HOST
                        The host name used for calling to the predictor from transformer.
  --protocol {v1,v2,grpc-v2}
                        The inference protocol used for calling to the predictor from transformer. Deprecated and replaced by --predictor_protocol
  --predictor_protocol {v1,v2,grpc-v2}
                        The inference protocol used for calling to the predictor from transformer.
  --predictor_use_ssl PREDICTOR_USE_SSL
                        Use ssl for the http connection to the predictor.
  --predictor_request_timeout_seconds PREDICTOR_REQUEST_TIMEOUT_SECONDS
                        The timeout seconds for the request sent to the predictor.
  --model_dir MODEL_DIR
                        A local path to the model binary
```

To run the Scikit-Learn Server from CLI:
```shell
python -m sklearnserver --model_dir model
```
**Note:** This will not work on Windows, because [Windows doesn't support Signals](https://docs.python.org/3.11/library/asyncio-platforms.html#windows) and the `loop.add_signal_handler()` method fails. Use the `ml-service` Docker image instead:
```shell
docker run -it -p 8080:8080 ml-service
```

## KServe REST API
To enable the InferenceService REST API [Swagger UI](https://kserve.github.io/website/master/get_started/swagger_ui/), run the server with the `--enable_docs_url` flag:
```shell
docker run -it -p 8080:8080 ml-service --model_dir /model --enable_docs_url true
```
Now you can go to the: [`/docs`](http://localhost:8080/docs) and verify the KServe ModelServer's endpoints along with their docs and examples.

**Other useful resources:**
- [Model Serving Data Plane](https://kserve.github.io/website/master/modelserving/data_plane/data_plane/) introduction
- Kserve v2 (as well as many other serving frameworks) adopts [the Open Inference Protocol](https://github.com/kserve/open-inference-protocol) (OIP):
  - [Open Inference Protocol API Specification](https://kserve.github.io/website/master/reference/swagger-ui/) (Swagger UI)
  - OIP HTTP/REST [inference protocol spec](https://github.com/kserve/open-inference-protocol/blob/main/specification/protocol/inference_rest.md)
- [TorchServe Inference API](https://github.com/pytorch/serve/blob/master/docs/inference_api.md) which supports the KServe Inference API


## Observability
KServe ModelServer already implements ML-specific metrics and logging so users don't have to develop these components themselves. You need to just enable what's needed with appropriate CLI options.

### Metrics
For latency metrics, send a request to [`/metrics`](http://localhost:8080/metrics). Prometheus latency histograms are emitted for each of the steps (pre/postprocessing, explain, predict).

Additionally, the latencies of each step are logged per request.

| Metric Name                 | Description                    | Type      |
|-----------------------------|--------------------------------|-----------| 
| request_preprocess_seconds  | pre-processing request latency | Histogram | 
| request_explain_seconds     | explain request latency        | Histogram | 
| request_predict_seconds     | prediction request latency     | Histogram |
| request_postprocess_seconds | pre-processing request latency | Histogram | 

### Logging

To enable more extensive logging, for example to log the latency metrics, run:
```shell
docker run -it -p 8080:8080 ml-service --model_dir /model \
  --enable_latency_logging true --configure_logging true
```
```shell
2024-07-02 08:51:59.040 kserve.trace requestId: N.A., preprocess_ms: 0.005245209, explain_ms: 0, predict_ms: 0.495672226, postprocess_ms: 0.004768372
2024-07-02 08:51:59.041 uvicorn.access INFO:     172.17.0.1:34580 1 - "POST /v1/models/model%3Apredict HTTP/1.1" 200 OK
2024-07-02 08:51:59.041 kserve.trace kserve.io.kserve.protocol.rest.v1_endpoints.predict: 0.0014352798461914062
2024-07-02 08:51:59.041 kserve.trace kserve.io.kserve.protocol.rest.v1_endpoints.predict: 0.0014349999999989649
```
The logs can also include request and response payloads and can be saved to a log file for more advanced analysis, like input data drift or model performance tracking.
