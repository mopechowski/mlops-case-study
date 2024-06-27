import sys
import logging
from joblib import load, dump
from pathlib import Path

# Everything should be set in the first call to the basicConfig method:
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s: %(levelname)s: %(name)s: %(message)s",
    handlers=(logging.StreamHandler(),),  # logging.FileHandler(log_filepath) log_filepath = prefix_path / Path('logs/postprocessor.log')
)
logger = logging.getLogger("PreProcessor")


def preprocess(data_dir: str, input_file: str, output_file: str):
    """Preprocesses the input_file and saves the results to output_file in the data_dir.

    Returns:
        str: a path to the output file if successful
    """
    
    data_path = Path(data_dir).resolve()
    input_path = data_path / Path(input_file)
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    input_data = load(input_path)
    n_samples = len(input_data.images)
    logger.info(f"Successfully loaded {n_samples} input samples.")
    
    output_data = input_data.images.reshape((n_samples, -1))
    output_data_path = data_path / output_file
    dump(output_data, filename=output_data_path)
    logger.info(f"Preprocessed data saved to: {output_data_path}")
    return str(output_data_path)


if __name__ == '__main__':
    if len(sys.argv) != 4:
        logger.error(f"Wrong number of arguments passed: {sys.argv}")
        raise RuntimeError("You need to provide exactly THREE positional arguments: data_dir input_file output_file!")
    logger.info(f"Hello from PreProcessor! Args: {sys.argv[1:]}")
    preprocess(sys.argv[1], sys.argv[2], sys.argv[3])
