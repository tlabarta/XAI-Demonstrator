import innvestigate
import numpy as np
import PIL.Image
import keras.applications.vgg16 as vgg16
import matplotlib.pyplot as plt
import tensorflow as tf


class LRPAnalzyer:
    def __init__(self):
        #Current workaround of innvestigate to solve issue, see here: https://github.com/albermax/innvestigate/issues/284
        tf.compat.v1.disable_eager_execution()

        self.model, self.preprocess = vgg16.VGG16(), vgg16.preprocess_input
        # Strip softmax layer
        self.model_wo_softmax = innvestigate.model_wo_softmax(self.model)
        # Create analyzer
        self.analyzer = innvestigate.create_analyzer(
            "lrp.sequential_preset_a_flat", self.model_wo_softmax, epsilon=1)

        with open("./imagenet_label_mapping") as f:
            self.labels = {int(x.split(":")[0]): x.split(":")[1].strip()
                           for x in f.readlines() if len(x.strip()) > 0}

    def get_lrp_heatmap(self, input):
        """Get the explanation of a predition via LRP, aggregate along color channels and normalize

        Args:
            input (np.ndarray): The image numpy array

        Returns:
            np.ndarray: The normalized 2d explanation array
        """
        x = self.preprocess(input[None])
        # Apply analyzer w.r.t. maximum activated output-neuron
        a = self.analyzer.analyze(x)

        # Aggregate along color channels and normalize to [-1, 1]
        a = a.sum(axis=np.argmax(np.asarray(a.shape) == 3))
        a /= np.max(np.abs(a))
        a = (a + 1)/2
        return a[0]

    def get_prediction(self, input):
        """Returns the tpo n predictions on an instance

        Args:
            input (np.ndarray): The image numpy array

        Returns:
            List: The list of objects, with fields of prob and label
        """
        n_probs = 5
        x = self.preprocess(input[None])
        prob = self.model.predict_on_batch(x)[0]
        y_hat = prob.argsort()[-n_probs:][::-1]
        preds = [{'probability': "{:.2f}".format(prob[i]), 'label':self.labels[i]}
                 for i in y_hat]
        return preds
