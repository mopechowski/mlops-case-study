# Batch Inference Pipeline

Install pipelines components in editable mode:
```shell
pip install -e .
```

Run simple components tests:
```shell
pytest
```

To run individual components respectively:
```shell
python -m pipelines.components.preprocessor ../data digits.joblib
```
```shell
python -m pipelines.components.scorer ../data instances.joblib 
```
```shell
python -m pipelines.components.postprocessor ../data predictions.joblib
```
