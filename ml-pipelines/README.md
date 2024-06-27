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
python -m pipelines.components.preprocessor ../data digits.joblib instances.joblib
```
The output should look like:
```shell
(mlops-dev) ..\mlops-case-study\ml-pipelines>python -m pipelines.components.preprocessor ../data digits.joblib instances.joblib
2024-06-27 10:44:10,925: INFO: PreProcessor: Hello from PreProcessor! Args: ['../data', 'digits.joblib', 'instances.joblib']
2024-06-27 10:44:11,711: INFO: PreProcessor: Successfully loaded 1797 input samples.
2024-06-27 10:44:11,712: INFO: PreProcessor: Preprocessed data saved to: ..\mlops-case-study\data\instances.joblib
```

```shell
python -m pipelines.components.scorer ../data instances.joblib predictions.joblib
```
The output should look like:
```shell
(mlops-dev) ..\mlops-case-study\ml-pipelines>python -m pipelines.components.scorer ../data instances.joblib predictions.joblib
2024-06-27 10:47:50,124: INFO: ModelScorer: Hello from ModelScorer! Args: ['../data', 'instances.joblib', 'predictions.joblib']
2024-06-27 10:47:50,126: INFO: ModelScorer: Successfully loaded 1797 instances.
2024-06-27 10:47:50,229: INFO: ModelScorer: Received predictions: 1797
2024-06-27 10:47:50,233: INFO: ModelScorer: Predictions saved to: C:\Users\marek\Repos\mlops-case-study\data\predictions.joblib
```

```shell
python -m pipelines.components.postprocessor ../data predictions.joblib
```
