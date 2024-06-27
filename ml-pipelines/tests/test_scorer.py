from pathlib import Path
from common import DATA_DIR
from pipelines.components.scorer import score


def test_score():
    input_file = 'instances.joblib'
    output_file = 'predictions.joblib'
    result = score(data_dir=DATA_DIR, input_file=input_file, output_file=output_file)
    assert result
    assert Path(result).exists()
