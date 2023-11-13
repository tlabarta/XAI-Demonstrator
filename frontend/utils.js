document.addEventListener('DOMContentLoaded', function () {
    const socket = io();

    // Get the selected XAI method from the dropdown
    var xaiMethodSelector = document.getElementById('xaiMethodDropdown');
    var selectedXaiMethod = xaiMethodSelector.value;

    // Set explanation text to default
    updateXaiInfoText(xaiMethodSelector.value);

    // Get the initial default selection by column
    let selectedNodesByColumn = { '1': '1_8', '2': '2_7' };

    // Set initial default selection
    for (const column in selectedNodesByColumn) {
        const defaultNode = document.getElementById(selectedNodesByColumn[column]);
        if (defaultNode) {
            defaultNode.style.fill = 'rgb(0, 148, 116)';
            const defaultTextElement = document.querySelector(`.node-text[id="${selectedNodesByColumn[column]}"]`);
            if (defaultTextElement) {
                defaultTextElement.style.stroke = 'white';
            }
        }
    }

    // Set initial default neuron IDs
    let selectedHiddenNeuronId = selectedNodesByColumn['1'].split('_')[1];
    let selectedOutputNeuronId = selectedNodesByColumn['2'].split('_')[1];

    document.getElementById('selectedHiddenNeuron').textContent = "Selected Hidden Neuron: " + selectedHiddenNeuronId;
    document.getElementById('selectedOutputNeuron').textContent = "Selected Output Neuron: " + selectedOutputNeuronId;

    socket.emit('select_input', { xai_method: selectedXaiMethod });
    socket.emit('explain_prediction', { xai_method: xaiMethodSelector.value });

    // Add an event listener for the change event on the dropdown
    xaiMethodSelector.addEventListener('change', function () {
        // Emit 'explain_prediction' event with updated XAI method
        updateXaiInfoText(xaiMethodSelector.value);
        document.getElementById('currentXAIselection').textContent = "XAI Method: " + xaiMethodSelector.value;
        document.getElementById('selectedNeuron').textContent = "Selected Neuron: 19";
        socket.emit('explain_prediction', { xai_method: xaiMethodSelector.value });
    });

    document.getElementById('action_button').addEventListener('click', function () {
        // Emit a custom event to the server
        socket.emit('button_click', { xai_method: xaiMethodSelector.value });
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

    // Select the default nodes
    const nodes = document.querySelectorAll('.node');
    let selectedPathId = null; // Variable to store the ID of the selected path

    // Add a click event listener to each node
    nodes.forEach(node => {
        node.addEventListener('click', function () {
            const clickedColumn = this.id.split('_')[0];
            const clickedNodeId = this.id.split('_')[1];

            // Update the selectedHiddenNeuronId or selectedOutputNeuronId based on the clicked column
            if (clickedColumn === '1') {
                selectedHiddenNeuronId = clickedNodeId;
                document.getElementById('selectedHiddenNeuron').textContent = "Selected Hidden Neuron: " + clickedNodeId;
            } else if (clickedColumn === '2') {
                selectedOutputNeuronId = clickedNodeId;
                document.getElementById('selectedOutputNeuron').textContent = "Selected Output Neuron: " + clickedNodeId;
            }

            // Check if another node is selected in the same column
            if (selectedNodesByColumn[clickedColumn]) {
                const previousNode = document.getElementById(selectedNodesByColumn[clickedColumn]);
                if (previousNode) {
                    previousNode.style.fill = 'rgb(255, 255, 255)';
                    const previousTextElement = document.querySelector(`.node-text[id="${selectedNodesByColumn[clickedColumn]}"]`);
                    if (previousTextElement) {
                        previousTextElement.style.stroke = 'black';
                    }
                }
            }

            console.log('Clicked Node ID:', this.id);
            console.log('Successful');

            // Change the fill color to green
            this.style.fill = 'rgb(0, 148, 116)';

            const newTextElement = document.querySelector(`.node-text[id="${this.id}"]`);
            if (newTextElement) {
                newTextElement.style.stroke = 'white';
            }

            // Update the selectedNodesByColumn variable
            selectedNodesByColumn[clickedColumn] = this.id;

            // Check if there was a previously selected path and change its color back to black
            if (selectedPathId) {
                const previousPath = document.getElementById(selectedPathId);
                console.log(selectedPathId)
                if (previousPath) {
                    previousPath.style.stroke = 'rgb(80, 80, 80)';
                    previousPath.style.strokeWidth = 0.5;
                }
            }

            // Construct the path ID based on the selected nodes
            const pathId = `path_${selectedNodesByColumn['1']}_${selectedNodesByColumn['2']}`;

            // Change the color of the path connecting the selected nodes to green
            const newPath = document.getElementById(pathId);
            console.log(pathId)
            if (newPath) {
                newPath.style.stroke = 'rgb(0, 148, 116)';
                newPath.style.strokeWidth = 3;
                selectedPathId = pathId; // Update the selectedPathId variable
            }
        });
    });

    // Function to update xai_info text based on the selected value
    function updateXaiInfoText(selectedXaiMethod) {
        // Hide all xai-info-text elements
        document.querySelectorAll('.xai-info-text').forEach(function (element) {
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
});
