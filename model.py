import torch.nn as nn
class Net(nn.Module):
    def __init__(self, n=16):
        super().__init__()
        self.hidden_layer = nn.Linear(784, n)
        self.flatten = nn.Flatten()
        self.finale_layer = nn.Linear(n, 10)

    def forward(self, x):
        x = self.flatten(x)
        x = self.hidden_layer(x)
        x = self.finale_layer(x)
        return x