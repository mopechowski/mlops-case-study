import sys
import logging
from joblib import load, dump
from pathlib import Path
import requests
from numpy import ndarray

# TODO: DRY: Duplicated code should be extracted to a common Python package!
# Everything should be set in the first call to the basicConfig method:
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s: %(levelname)s: %(name)s: %(message)s",
    handlers=(logging.StreamHandler(),),  # logging.FileHandler(log_filepath) log_filepath = prefix_path / Path('logs/postprocessor.log')
)
logger = logging.getLogger("ModelScorer")


def score(data_dir: str, input_file: str, output_file: str):
    """Gets predictions for instances in the input_file and saves the results to output_file in the data_dir.

    Returns:
        str: a path to the output file if successful
    """
    
    # TODO: DRY: Duplicated code should be extracted to a common Python package!
    data_path = Path(data_dir).resolve()
    input_path = data_path / Path(input_file)
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    input_data: ndarray = load(input_path)
    n_samples = len(input_data)
    logger.info(f"Successfully loaded {n_samples} instances.")
    
    instances = input_data.tolist()
    post_data = {"instances": instances}
    response = requests.post('http://localhost:8080/v1/models/model:predict', json=post_data)
    response.raise_for_status()
    logger.debug(f"Received response from ModelServer:\n{response.text}")
    response = response.json()
    if "predictions" not in response:
        raise KeyError('"predictions" not in response!')
    predictions: list = response['predictions']
    logger.info(f"Received predictions: {len(predictions)}")
    
    # TODO: DRY: Duplicated code should be extracted to a common Python package!
    output_data = predictions
    output_data_path = data_path / output_file
    dump(output_data, filename=output_data_path)
    logger.info(f"Predictions saved to: {output_data_path}")
    return str(output_data_path)


if __name__ == '__main__':
    # TODO: DRY: Duplicated code should be extracted to a common Python package!
    if len(sys.argv) != 4:
        logger.error(f"Wrong number of arguments passed: {sys.argv}")
        raise RuntimeError("You need to provide exactly THREE positional arguments: data_dir input_file output_file!")
    logger.info(f"Hello from ModelScorer! Args: {sys.argv[1:]}")
    score(sys.argv[1], sys.argv[2], sys.argv[3])
