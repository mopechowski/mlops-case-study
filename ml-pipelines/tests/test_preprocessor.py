from pathlib import Path
from common import DATA_DIR
from pipelines.components.preprocessor import preprocess


def test_preprocess():
    input_file = 'digits.joblib'
    output_file = 'instances.joblib'
    result = preprocess(data_dir=DATA_DIR, input_file=input_file, output_file=output_file)
    assert result
    assert Path(result).exists()
