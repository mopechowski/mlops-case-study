# This dummy pipeline triggers containerized components in a sequence
import docker
from pathlib import Path


IMAGE = 'ml-pipelines'
DATA_DIR = '/data'
STORAGE_DIR = './data/storage'
STORAGE_PATH = Path(STORAGE_DIR).resolve()

client = docker.from_env()


# TODO: Such a class should be extracted to a common package
class PipelineComponent:
    """A pipeline component class holding common pipeline's arguments."""
    
    def __init__(self, component: str, input_file: str, output_file: str, image: str):
        self.component = component
        self.input_file = input_file
        self.output_file = output_file
        self.image = image
        
        # I know I shouldn't set it up like this, but I'm running out of time:
        self._client = client
        self._cmd = [component, DATA_DIR, input_file, output_file]
        self._volumes = {str(STORAGE_PATH.absolute()): {'bind': DATA_DIR, 'mode': 'rw'}}
    
    def __call__(self):
        """Runs a containerized component"""
        # The client.containers.run returns:
        # The container logs, either STDOUT, STDERR, or both, depending on the value of the stdout and stderr arguments.
        # STDOUT and STDERR may be read only if either json-file or journald logging driver used.
        # Thus, if you are using none of these drivers, a None object is returned instead. See the Engine API documentation for full details.
        # => That's why in this version you cannot see the logs stream from containers...
        client.containers.run(
            self.image,
            command=self._cmd,
            volumes=self._volumes,
            remove=True,
            detach=False,
            stdout=True,
            stderr=True,
            stream=True,
            network_mode='host',  # The host network mode is just for demonstration purpose, it shouldn't be used in PROD!
        )


# TODO: Add proper parametrization and logging:
def inference_pipeline(image: str):
    
    # Initialize the components:
    preprocess_step = PipelineComponent('pipelines.components.preprocessor', 'digits.joblib', 'instances.joblib', image)
    score_step = PipelineComponent('pipelines.components.scorer', 'instances.joblib', 'predictions.joblib', image)
    postprocess_step = PipelineComponent('pipelines.components.postprocessor', 'predictions.joblib', 'results.csv', image)
    
    # Run the pipeline's steps
    print("Pipeline: PreProcessor step starting...")
    preprocess_step()
    print("Pipeline: PreProcessor step DONE!")

    print("Pipeline: ModelScore step starting...")
    score_step()
    print("Pipeline: ModelScore step DONE!")

    print("Pipeline: PostProcessor step starting...")
    postprocess_step()
    print("Pipeline: PostProcessor step DONE!")


if __name__ == '__main__':
    print("Starting the pipeline...")
    inference_pipeline(image=IMAGE)
    print("Pipeline DONE!")
