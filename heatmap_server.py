from aiohttp import web
import socketio
from heatmap_service import HeatmapService
import argparse
import random
from torchvision import datasets, transforms
import os
from PIL import Image
import torch
from model import Net



parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--port', '-p', type=int, default=8080,
                    dest="port", help="Port for the socketio server")
args = parser.parse_args()

#service = HeatmapService()
sio = socketio.AsyncServer()
app = web.Application()

sio.attach(app)

predictions = {}

transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5,), (0.5,))])
trainset = datasets.MNIST('./data', download=True, train=True, transform=transform)
testset = datasets.MNIST('./data', download=True, train=False, transform=transform)

# Load PyTorch Model
model_data = torch.load('data/model/trained_model.pth', map_location='cpu')

if 'model_state_dict' in model_data:
    model_state_dict = model_data['model_state_dict']
    net = Net()
    net.load_state_dict(model_state_dict)
else:
    # Handle the case when the model is not saved as expected
    raise ValueError("Invalid model file format.")



async def index(request):
    """Serve the client-side application."""
    with open('frontend/index.html') as f:
        return web.Response(text=f.read(), content_type='text/html')

@sio.event
def connect(sid, environ):
    print("connect ", sid)


@sio.event
async def button_click(sid, data):
    # Call select_input when the button is clicked
    await select_input(sid, data)

@sio.event
async def select_input(sid, data):
    # Get a random index from the MNIST test dataset
    random_index = random.randint(0, len(testset) - 1)

    # Get the image tensor based on the random index
    image_tensor, actual_label = testset[random_index]


    # Get model prediction
    prediction = get_prediction(net, image_tensor)


    # Get the image path based on the random index
    save_rand_img(testset[random_index])
    random_image_path = "website_img/temp_image.png"

    # Send the random image path to the client
    await sio.emit('input_image', {'data': random_image_path}, room=sid)
    await sio.emit('prediction', {'prediction': prediction, 'actual_label': actual_label}, room=sid)


@sio.event
async def explain_prediction(sid, data):
    # Get the selected XAI method from the client
    xai_method = data.get('xai_method', 'lrp')

    heatmap = None

    # Generate heatmap based on the selected XAI method
    if xai_method == 'lrp':
        #heatmap = generate_lrp_heatmap(model, image_tensor)
        print("lrp success")
    elif xai_method == 'shap':
        #heatmap = generate_shap_heatmap(model, image_tensor)
        print("shap success")
    else:
        heatmap = None

    heatmap_path = "website_img/heatmap.png"

    if heatmap is not None:
        await sio.emit('heatmap', {'data': heatmap}, room=sid)



def save_rand_img(sample, target_size=(640, 480)):
    # Assuming the sample is a tuple where the first element is the image tensor
    image_tensor = sample[0]

    #Transform the image tensor back to a NumPy array
    image_array = image_tensor.numpy()

    # Ensure the image_array is 2D (28x28) and convert to 8-bit unsigned integer
    image_array = (image_array * 255).astype('uint8')

    # Resize the image to the target size (640x480)
    resized_image = Image.fromarray(image_array.squeeze(), mode='L').resize(target_size)

    # Save the resized image as an image file
    temp_file_path = "frontend/website_img/temp_image.png"
    resized_image.save(temp_file_path)



# Create Prediction Function
def get_prediction(net, image_tensor):
    output = net(image_tensor)
    _, predicted_class = torch.max(output, 1)
    return predicted_class.item()

# Integrate XAI Methods
def generate_lrp_heatmap(model, image_tensor):
    pass

def generate_shap_heatmap(model, image_tensor):
    pass



@sio.event
async def chat_message(sid, data):
    print("message ", data)


@sio.event
def disconnect(sid):
    print('disconnect ', sid)
    del predictions[sid]


app.router.add_get('/', index)
app.add_routes([web.static('/', './frontend/')])

if __name__ == '__main__':
    # Get the absolute path to the frontend directory
    frontend_dir = os.path.abspath('frontend')

    # Configure the absolute path for serving static files
    app.router.add_static('/', frontend_dir)
    web.run_app(app, port=args.port)
