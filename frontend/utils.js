

document.addEventListener('DOMContentLoaded', function () {
    const socket = io();

        // Get the selected XAI method from the dropdown
    var xaiMethodSelector = document.getElementById('xaiMethodDropdown');

    var selectedXaiMethod = xaiMethodSelector.value;

    // Set explanation text to default
    updateXaiInfoText(xaiMethodSelector.value);
    document.getElementById('currentXAIselection').textContent = "XAI Method: " + xaiMethodSelector.value;
    document.getElementById('selectedNeuron').textContent = "Selected Neuron: 19";


    // Emit 'videoframe' event with dataset ID and selected XAI method
    socket.emit('select_input', {xai_method: selectedXaiMethod });
    socket.emit('explain_prediction', {xai_method: xaiMethodSelector.value });

           // Add an event listener for the change event on the dropdown
    xaiMethodSelector.addEventListener('change', function () {
        // Emit 'explain_prediction' event with updated XAI method
        updateXaiInfoText(xaiMethodSelector.value);
        document.getElementById('currentXAIselection').textContent = "XAI Method: " + xaiMethodSelector.value;
        document.getElementById('selectedNeuron').textContent = "Selected Neuron: 19";
        socket.emit('explain_prediction', {xai_method: xaiMethodSelector.value });

    });

    document.getElementById('action_button').addEventListener('click', function () {
    // Emit a custom event to the server
        socket.emit('button_click', {xai_method: xaiMethodSelector.value });
    });

    // Listen for the 'input_image' event from the server
    socket.on('input_image', function (data) {
        // Update the src attribute of the img element with the received image path

        document.getElementById('input_img').src = data.data + '?' + new Date().getTime();

    });

    // Listen for the 'prediction' event from the server
    socket.on("prediction", function (data) {
        var prediction = data.prediction;
        var actual_label = data.actual_label;
        console.log(prediction);

        const responseText = document.getElementById('prediction');
        responseText.textContent = 'Predicted number: ' + String(prediction);

        const actLabel = document.getElementById('label');
        actLabel.textContent = 'Actual number: ' + String(actual_label);

    });


    socket.on("heatmap", function (data) {
        var heatmapResponse = data.data;
        console.log(heatmapResponse)
        document.getElementById('explanation_img').src = heatmapResponse + '?' + new Date().getTime();
    });

    const nodes = document.querySelectorAll('.node'); // Select nodes with the class 'node'
    let selectedNode = null; // To keep track of the currently selected node

    // Add a click event listener to each node
    nodes.forEach(node => {
        node.addEventListener('click', function() {
            // If another node was previously selected, reset its color
            if (selectedNode !== null) {
                selectedNode.style.fill = 'rgb(255, 255, 255)'; // Reset color to default (empty string)
            }

            // Log the node ID to the console
            console.log('Clicked Node ID:', this.id);
            console.log('Successful');

            // Change the fill color to red
            this.style.fill = 'red';

            // Update the selectedNode variable
            selectedNode = this;
        });
    });



});


    // Function to update xai_info text based on the selected value
function updateXaiInfoText(selectedXaiMethod) {
    // Hide all xai-info-text elements
    document.querySelectorAll('.xai-info-text').forEach(function(element) {
        element.style.display = 'none';
    });

    // Show the relevant xai-info-text based on the selected XAI method
    switch (selectedXaiMethod) {
        case 'lrp':
            document.getElementById('lrpInfo').style.display = 'block';
            break;
        case 'crp':
            document.getElementById('crpInfo').style.display = 'block';
            break;
        // Add more cases as needed for other XAI methods
        // ...
    }
}
