import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import Normalize
from PIL import Image
from PIL import ImageOps


from zennit.composites import EpsilonPlus
from crp.attribution import CondAttribution
from torchvision import transforms
class CRPAnalyzer():

    def __init__(self, model, randID, hiddenIDX, outputIDX):#, selected_hidden_neuron, selected_output_neuron):
        self.model = model
        self.img = "frontend/website_img/input.png"
        self.idx = randID  # index of the data sample in the dataset
        self.hidden_neuron_idx = hiddenIDX#8#selected_hidden_neuron #8  # 0-15 or None    # index of the hidden neuron (which concept) we condition the explanation on
        self.output_neuron_idx = outputIDX#7#selected_output_neuron #7  # 0-9             # index of the output neuron (which output-class) we condition the explanation on
    def preprocess_image(self):
        # Open the image
        image = Image.open(self.img)

        # Convert to grayscale using the luminance formula
        grayscale_image = ImageOps.grayscale(image)

        # Resize the image to the target size (28x28)
        resized_image = grayscale_image.resize((28, 28))

        # Convert the image to a PyTorch tensor
        image_tensor = transforms.ToTensor()(resized_image).unsqueeze_(0)

        return image_tensor

    def explain_prediction(self):
        attributor = CondAttribution(self.model, EpsilonPlus())
        conditions = [{
            'y': self.output_neuron_idx,
            'hidden_layer': self.hidden_neuron_idx
        }]


        # Preprocess the input image
        x = self.preprocess_image()
        x.requires_grad_()         # for the heatmap computation the data requires gradients


        attribution = attributor(x, conditions=conditions)

        heatmap = attribution.heatmap # THIS IS THE HEATMAP YOU NEED TO SHOW
        vis_heatmap = heatmap.permute(1, 2, 0)

        heatmap_path = "frontend/website_img/heatmap.png"

        vis_heatmap = vis_heatmap[:, :, np.newaxis]  # Add a channel dimension
        normalized_vis_heatmap = (vis_heatmap - vis_heatmap.min()) / (vis_heatmap.max() - vis_heatmap.min())
        plt.imsave(heatmap_path, normalized_vis_heatmap.numpy(), cmap='seismic')

        vis_heatmap = Image.open(heatmap_path)
        resized_heatmap = vis_heatmap.resize((640, 480))
        resized_heatmap.save(heatmap_path)

        return heatmap_path

