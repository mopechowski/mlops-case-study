from pathlib import Path
from common import DATA_DIR
from pipelines.components.scorer import score


def test_score():
    # I know, a real unit test should use fixtures and mocking here
    input_file = 'instances.joblib'
    output_file = 'predictions.joblib'
    result = score(data_dir=DATA_DIR, input_file=input_file, output_file=output_file)
    assert result
    assert Path(result).exists()
