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
        #vis_heatmap = heatmap.permute(1, 2, 0)
        #heatmap_path = "website_img/heatmap.png"

        #vis_heatmap = vis_heatmap[:, :, np.newaxis]  # Add a channel dimension

        #v = max(abs(heatmap.max().item()), abs(heatmap.min().item()))
        #norm = Normalize(vmin=-v, vmax=v)
        # Apply the normalization to the data
        #normalized_vis_heatmap = norm(vis_heatmap)


        # plt.imsave("frontend/" + heatmap_path, vis_heatmap.numpy(), cmap='bwr')
        #
        # vis_heatmap = Image.open("frontend/" + heatmap_path)
        # resized_heatmap = vis_heatmap.resize((640, 480))
        # resized_heatmap.save("frontend/" + heatmap_path)


        # norm_heatmap = (heatmap - heatmap.min()) / (heatmap.max() - heatmap.min())

        heatmap_path = "website_img/heatmap.png"
        tensor_to_pil = transforms.ToPILImage()(heatmap.squeeze_(0)).resize((640, 480))
        tensor_to_pil.save("frontend/" + heatmap_path, "PNG")

        return heatmap_path

