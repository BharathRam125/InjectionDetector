import torch
import numpy
import json
import dgl
from dgl.nn import GraphConv
from torch.utils.data import DataLoader
from dgl.dataloading import GraphDataLoader
import torch.nn as nn
import torch.nn.functional as F

from flask import Flask, render_template, request, redirect, url_for, render_template_string

app = Flask(__name__)

USERNAME = "SaiyanSai"
PASSWORD = "P4$$W0RD"

class GCNClassifier(nn.Module):
    def __init__(self, vocab_size, embed_dim=128, hidden_dim=128, num_classes=2, dropout=0.6):
        super().__init__()
        print("Initializing Improved GCN model...")

        self.embed = nn.Embedding(vocab_size, embed_dim)

        # Three GraphConv layers for better feature extraction
        self.conv1 = GraphConv(embed_dim, hidden_dim, allow_zero_in_degree=True)
        self.conv2 = GraphConv(hidden_dim, hidden_dim, allow_zero_in_degree=True)
        self.conv3 = GraphConv(hidden_dim, hidden_dim, allow_zero_in_degree=True)

        # Batch Normalization to stabilize training
        self.bn1 = nn.BatchNorm1d(hidden_dim)
        self.bn2 = nn.BatchNorm1d(hidden_dim)
        self.bn3 = nn.BatchNorm1d(hidden_dim)

        # Fully connected layers
        self.fc1 = nn.Linear(hidden_dim, hidden_dim // 2)
        self.fc2 = nn.Linear(hidden_dim // 2, num_classes)

        # Dropout for regularization
        self.dropout = nn.Dropout(dropout)
        print("Model initialized.")

    def forward(self, g):
        h = self.embed(g.ndata["feat"].squeeze(1).to(self.embed.weight.device))
        h = F.relu(self.bn1(self.conv1(g, h)))
        h = F.relu(self.bn2(self.conv2(g, h)))
        h = F.relu(self.bn3(self.conv3(g, h)))

        with g.local_scope():
            g.ndata["h"] = h
            hg = dgl.mean_nodes(g, "h")

        hg = self.dropout(F.relu(self.fc1(hg)))
        return self.fc2(hg)

with open('Models/char_vocab.json', 'r', encoding='utf-8') as file:
    vocab = json.load(file)

device = torch.device("cpu")
model = GCNClassifier(vocab_size=len(vocab)).to(device)
model.load_state_dict(torch.load("Models/gcn_model_v3.pth", map_location=device, weights_only=True))
model.eval()
print("Model loaded successfully.")

def preprocess_payload(payload, vocab):
    if not payload:  # Handle empty payloads
        return dgl.graph(([], []), num_nodes=1)

    chars = list(payload)  # Keep character sequence
    num_nodes = len(chars)

    g = dgl.graph(([], []))
    g.add_nodes(num_nodes)

    # Assign features (character embeddings)
    char_ids = [vocab.get(c, 0) for c in chars]  # Unknown chars get ID 0
    g.ndata["feat"] = torch.tensor(char_ids, dtype=torch.long).unsqueeze(1)

    # Create directed edges (bi-directional for better context)
    src = list(range(num_nodes - 1))
    dst = list(range(1, num_nodes))

    g.add_edges(src, dst)  # Forward edges
    g.add_edges(dst, src)  # Backward edges

    return g


def predict(payload):
    g = preprocess_payload(payload, vocab)
    g = g.to(device)

    with torch.no_grad():
        logits = model(g)
        probs = torch.softmax(logits, dim=1).cpu().numpy()
        pred_label = int(probs.argmax(axis=1)[0])  # Get class label
        confidence = float(probs[0][pred_label])   # Get confidence score

        print(pred_label, confidence)

    return pred_label


@app.route('/')
def home():
    return render_template('home.html')

#This code is where the injection is intended to happen
@app.route('/login', methods = ['GET', 'POST'])
def login():
    prediction1 = 0
    prediction2 = 0
    if request.method == 'POST' : 
        username = request.form['username']
        password = request.form['password']

        prediction1 = predict(username)
        prediction2 = predict(password)


        print(prediction1, prediction2)
        if prediction1 == 1 or prediction2 == 1:
            return 'Haha Pathetic... Your injection attacks wont work on me'


        if username == USERNAME and password == PASSWORD:
            return redirect(url_for('home'))
        else:
            return 'Invalid Username or Password'
    return render_template('login.html')

#This code is intentionally vulnerable to XSS
@app.route('/greet', methods = ['GET'])
def greet():
    prediction = 0
    name = request.args.get('name')

    if name:
        prediction = predict(name)

    if prediction == 1:
        return 'You Seriously thought that was going to work??'
    response = f"<h3>H3LL0, {name} !!!! </h3>"
    return render_template_string(response)
if __name__ == '__main__':
    app.run(debug=True)
    
