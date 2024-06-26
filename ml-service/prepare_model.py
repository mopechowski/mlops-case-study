# Based on: https://scikit-learn.org/stable/auto_examples/classification/plot_digits_classification.html
import os
from joblib import dump

import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt

from numpy import ndarray

from sklearnserver import SKLearnModel

from sklearn import datasets, metrics, svm
from sklearn.model_selection import train_test_split

MODEL_DIR = 'model'
JOBLIB_FILE = os.path.join(MODEL_DIR, "model.joblib")


def plot_digits(images: ndarray, labels: ndarray, title: str = ''):
    """Plots the digits with labels"""

    _, axes = plt.subplots(nrows=1, ncols=4, figsize=(10, 3))
    for ax, image, label in zip(axes, images, labels):
        ax.set_axis_off()
        if image.shape != (8, 8):
            image = image.reshape(8, 8)
        ax.imshow(image, cmap=plt.cm.gray_r, interpolation="nearest")
        _title = f"{title}: {label}" if title else f"{label}"
        ax.set_title(_title)


def show_model_evaluation(model, y_true: ndarray, y_pred: ndarray):
    """Shows the model evaluation."""
    
    print(
        f"Classification report for classifier {model}:\n"
        f"{metrics.classification_report(y_true, y_pred)}\n"
    )
    
    disp = metrics.ConfusionMatrixDisplay.from_predictions(y_true, y_pred)
    disp.figure_.suptitle("Confusion Matrix")
    print(f"Confusion matrix:\n{disp.confusion_matrix}")
    plt.show()


def try_model_artifact(name: str, model_dir: str, X_test: ndarray, y_test_pred: ndarray, test_cases: slice):
    """Reads in the model artifact and tests using test samples"""
    kserve_model = SKLearnModel(name=name, model_dir=model_dir)
    kserve_model.load()
    request = X_test[test_cases, :].tolist()
    response = kserve_model.predict({"instances": request})
    if response["predictions"] != y_test_pred[test_cases].tolist():
        raise ValueError("Test predictions incorrect!")
    print("Model artifact works as expected!")


if __name__ == '__main__':
    # Read in the digits datasets and plot it:
    digits = datasets.load_digits()
    plot_digits(digits.images, digits.target, 'Training')
    
    # Flatten the images:
    n_samples = len(digits.images)
    data = digits.images.reshape((n_samples, -1))
    print(f"Successfully loaded {n_samples} samples.")
    
    # Split data into 50% train and 50% test subsets
    X_train, X_test, y_train, y_test = train_test_split(
        data, digits.target, test_size=0.5, shuffle=False
    )
    
    # Create a support vector classifier:
    model = svm.SVC(gamma=0.001)
    
    # Learn the digits on the train subset:
    model.fit(X_train, y_train)
    print(f"Trained the model {model}")
    
    # Predict the value of the digit on the test subset
    y_test_pred = model.predict(X_test)
    
    # Evaluate the classifier:
    print(f"Model evaluation on the TEST dataset:")
    plot_digits(X_test, y_test_pred, 'Prediction')
    show_model_evaluation(model, y_true=y_test, y_pred=y_test_pred)
    
    # Save the model artifact
    dump(model, filename=JOBLIB_FILE)
    print(f"Model: {model} saved to: {JOBLIB_FILE}")
    
    # Read in the model artifact and test it
    try_model_artifact("digits", MODEL_DIR, X_test, y_test_pred, slice(45, 55, 1))
    print(f"Work DONE")
