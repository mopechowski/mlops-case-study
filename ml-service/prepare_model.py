# Based on: https://scikit-learn.org/stable/auto_examples/classification/plot_digits_classification.html
import os
from joblib import dump

import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt

from sklearnserver import SKLearnModel

from sklearn import datasets, metrics, svm
from sklearn.model_selection import train_test_split

MODEL_DIR = 'model'
JOBLIB_FILE = os.path.join(MODEL_DIR, "model.joblib")

digits = datasets.load_digits()

_, axes = plt.subplots(nrows=1, ncols=4, figsize=(10, 3))
for ax, image, label in zip(axes, digits.images, digits.target):
    ax.set_axis_off()
    ax.imshow(image, cmap=plt.cm.gray_r, interpolation="nearest")
    ax.set_title("Training: %i" % label)

# flatten the images
n_samples = len(digits.images)
data = digits.images.reshape((n_samples, -1))

# Create a classifier: a support vector classifier
model = svm.SVC(gamma=0.001)

# Split data into 50% train and 50% test subsets
X_train, X_test, y_train, y_test = train_test_split(
    data, digits.target, test_size=0.5, shuffle=False
)

# Learn the digits on the train subset
model.fit(X_train, y_train)

# Predict the value of the digit on the test subset
predicted = model.predict(X_test)


# Evaluate the classifier:
_, axes = plt.subplots(nrows=1, ncols=4, figsize=(10, 3))
for ax, image, prediction in zip(axes, X_test, predicted):
    ax.set_axis_off()
    image = image.reshape(8, 8)
    ax.imshow(image, cmap=plt.cm.gray_r, interpolation="nearest")
    ax.set_title(f"Prediction: {prediction}")

print(
    f"Classification report for classifier {model}:\n"
    f"{metrics.classification_report(y_test, predicted)}\n"
)

disp = metrics.ConfusionMatrixDisplay.from_predictions(y_test, predicted)
disp.figure_.suptitle("Confusion Matrix")
print(f"Confusion matrix:\n{disp.confusion_matrix}")

plt.show()


# Save the model artifact
dump(model, filename=JOBLIB_FILE)

# Read in the model artifact and test it
kserve_model = SKLearnModel(name="digits", model_dir=MODEL_DIR)
kserve_model.load()
test_cases = slice(45, 55, 1)
request = X_test[test_cases, :].tolist()
response = kserve_model.predict({"instances": request})
assert response["predictions"] == predicted[test_cases].tolist(), "Test prediction incorrect!"


def train():
    pass


if __name__ == '__main__':
    train()
