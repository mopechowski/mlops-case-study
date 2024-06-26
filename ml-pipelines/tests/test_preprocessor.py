from pathlib import Path
from common import DATA_DIR
from pipelines.components.preprocessor import preprocess


def test_preprocess():
    filename = 'digits.joblib'
    result = preprocess(data_dir=DATA_DIR, filename=filename)
    assert result
    assert Path(result).exists()
