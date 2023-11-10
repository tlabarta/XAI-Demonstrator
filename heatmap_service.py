from lrp import LRPAnalzyer
from PIL import Image
import numpy as np
from matplotlib import cm
import io
import torch
from torchvision import datasets, transforms


class HeatmapService:
    def __init__(self):
        #self.image_shape = (224, 224)
        #self.analyzer = LRPAnalzyer()
        self.model = torch.load("data/model/trained_model.pth")
    @staticmethod

    def analyze_image(self, image_data):
        """Get the analysis for the image using lrp, apply a colormap and convert the resulting image to byte array

        Args:
            image_data (blob): The image sent by the fronend

        Returns:
            img_byte_arr (io.BytesIO): Byte array of the result
        """
        image, original_size = self.binary_to_numpy(image_data)
        result = self.analyzer.get_lrp_heatmap(image)
        image = cm.seismic(result)
        image = Image.fromarray(np.uint8(image*255)).resize(original_size)

        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        return img_byte_arr

    def predict_image(self, image_data):
        """Get the top predictions for a given image

        Args:
            image_data (blob): The image sent by the frontend

        Returns:
            result (List): Sorted list of confidences
        """
        image, _ = self(image_data)
        result = self.model(image)
        return result
