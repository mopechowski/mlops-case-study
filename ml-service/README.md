# Inference Service

The Inference Service has been implemented as a simplified and minimal version of `SKLearnModel` and is based on the [KServe's Scikit-Learn Server](https://github.com/kserve/kserve/tree/master/python/sklearnserver) Python package.

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

To run the Scikit-Learn Server from CLI:
```shell
python -m sklearnserver --model_dir model
```
**Note:** This will not work on Windows, because [Windows doesn't support Signals](https://docs.python.org/3.11/library/asyncio-platforms.html#windows) and the `loop.add_signal_handler()` method fails. Use the `ml-service` Docker image instead.
