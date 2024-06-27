from pathlib import Path
from common import DATA_DIR
from pipelines.components.postprocessor import postprocess


def test_postprocess():
    # I know, a real unit test should use fixtures and mocking here
    input_file = 'predictions.joblib'
    output_file = 'results.csv'
    result = postprocess(data_dir=DATA_DIR, input_file=input_file, output_file=output_file)
    assert result
    assert Path(result).exists()
