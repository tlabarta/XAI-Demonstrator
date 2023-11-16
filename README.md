# Interactive demonstrator for XAI
This repository contains an interactive XAI demonstrator for [Concept Relevance Propagation (CRP)](https://www.hhi.fraunhofer.de/en/departments/ai/technologies-and-solutions/concept-relevance-propagation.html).

This technique allows to measure the (conditional) relevance a neural network assigns to the individual parts of an input. 

For this demo, a simple feed-forward neural network with one hidden layer was visualized alongside the input-image, 
the network's prediction, and the corresponding heatmap.

The visualization of the network architecture needs to includes all layers. As we can condition the CRP heatmaps on hidden and output neurons, they are selectable in the demo by clicking on them, using them as input parameters for CRP. The displayed heatmap dynamically recomputes and update after selecting new neurons.

### Frontend
The frontend was built using HTML ('file: index.html'), CSS ('main.css') and JavaScript ('client.js'). The input from MNIST and the explanation are loaded as '.png' images from 'frontend/website_img' into the website. The feed-forward network was visualized with a SVG file built into the HTML. The SVG was initially created with the [NN SVG tool by Alex Lenail](http://alexlenail.me/NN-SVG/LeNet.html). All dynamic formatting like coloring of selected nodes and weights was developed additionally. 

### Backend
The backend was built in a client-server architecture using socket.io. The client is developed in JavaScript ('client.js') while the server ('heatmap_server.py') is written in Python. Additional server dependencies are  'model.py' where the feed-forward architecture is defined and 'crpAnalyze.py' which builds a CRP Analyzer to explain incoming predictions based on input samples and hidden and output neuron IDs. The file 'lrpAnalyze.py' for building a LRP Analyzer is still work in progress (WIP) and is not to be used.

### demo_and_defaults.ipynb
This file was adapted from the examples.ipynb to allow for setting the default input and heatmaps to display when starting the demo. It can also be used to retrain the model or changing its architecture. Remember to adapt 'model.py' accordingly when changing the architecture.

## Set up:

For running the demo you need to have Python 3.11. You can set up a conda environment, for example, with
```bash
conda create --name demo_hhi python=3.11
```

and then install the requirements from `requirements.txt` with `pip` (as some are not available in the usual conda channels):
```bash
pip install -r requirements.txt
```

If you are not familiar with conda, you can also just manually install the dependencies listed.


