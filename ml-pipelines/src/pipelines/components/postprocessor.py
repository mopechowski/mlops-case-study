import sys
import logging
from joblib import load
from pathlib import Path
from pandas import DataFrame

# TODO: DRY: Duplicated code should be extracted to a common Python package!
# Everything should be set in the first call to the basicConfig method:
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s: %(levelname)s: %(name)s: %(message)s",
    handlers=(logging.StreamHandler(),),  # logging.FileHandler(log_filepath) log_filepath = prefix_path / Path('logs/postprocessor.log')
)
logger = logging.getLogger("PostProcessor")


def postprocess(data_dir: str, input_file: str, output_file: str):
    """Postprocesses the data from the input_file and saves the results to a csv output_file in the data_dir.
    
    Returns:
        str: a path to the output file if successful
    """
    
    # TODO: DRY: Duplicated code should be extracted to a common Python package!
    data_path = Path(data_dir).resolve()
    input_path = data_path / Path(input_file)
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    input_data: list = load(input_path)
    n_samples = len(input_data)
    logger.info(f"Successfully loaded {n_samples} records.")
    
    output_data_path = data_path / output_file
    # It's an overkill to use pandas only to save a simple list to a csv file, but it's just a nice one-liner ;-)
    DataFrame(input_data, columns=['prediction']).to_csv(output_data_path, index_label='id')
    logger.info(f"Results saved to: {output_data_path}")
    return str(output_data_path)


if __name__ == '__main__':
    # TODO: DRY: Duplicated code should be extracted to a common Python package!
    if len(sys.argv) != 4:
        logger.error(f"Wrong number of arguments passed: {sys.argv}")
        raise RuntimeError("You need to provide exactly THREE positional arguments: data_dir input_file output_file!")
    logger.info(f"Hello from PostProcessor! Args: {sys.argv[1:]}")
    postprocess(sys.argv[1], sys.argv[2], sys.argv[3])
