import numpy as np
import tensorflow, os, json, pickle, yaml
from tensorflow.keras.utils import to_categorical
from collections import Counter

OUTPUT_DIR = "output"
fpath = os.path.join(OUTPUT_DIR, "data.pkl")
with open(fpath, "rb") as fd:
    data = pickle.load(fd)
(x_train, y_train),(x_test, y_test) = data
labels = y_test.astype(int)
y_test = to_categorical(y_test)

image_size = x_train.shape[1]
input_size = image_size * image_size

# Model specific code
x_test = x_test.reshape(-1, 28, 28, 1)
x_test = x_test.astype('float32') / 255
# End of Model specific code

model_file = os.path.join(OUTPUT_DIR, "model.h5")
model = tensorflow.keras.models.load_model(model_file)

metrics_dict = model.evaluate(x_test, y_test, return_dict=True)
print(metrics_dict)

METRICS_FILE = os.path.join(OUTPUT_DIR, "metrics.json")
with open(METRICS_FILE, "w") as f:
    f.write(json.dumps(metrics_dict))

pred_probabilities = model.predict(x_test)
predictions = np.argmax(pred_probabilities, axis=1)
all_predictions = [{"actual": int(actual), "predicted": int(predicted)} for actual, predicted in zip(labels, predictions)]

os.makedirs(os.path.dirname("output/test/"), exist_ok=True)
with open("output/test/predictions.json", "w") as f:
    json.dump(all_predictions, f)

predicted_classes = Counter(predictions)
predicted_classes = [{"class": int(k), "count": int(v)} for k,v in predicted_classes.items()]
with open("output/test/predicted_classes.json", "w") as f:
    json.dump(predicted_classes, f)