# Read input file and inspect it
with open('input.txt', 'r', encoding='utf-8') as file:
    text = file.read()

# Here are all the unique characters within the text file
chars = sorted(list(set(text)))
vocab_size = len(chars)

# Create a mapping from characters to integers
stoi = { ch : i for i, ch in enumerate(chars) }
itos = { i : ch for i, ch in enumerate(chars) }
encode = lambda s : [stoi[c] for c in s] # Given a string input, output a list of integers
decode = lambda l : ''.join([itos[i] for i in l]) # Given a list of integers, output a string

# Encode entire text dataset and store it into torch.Tensor
import torch

data = torch.tensor(encode(text), dtype=torch.long)
print(data.shape, data.dtype)

# Split up data into train and validation sets
n = int(0.9 * len(data)) # First 90% is training set, remaining 10% is validation set
train_data = data[:n]
val_data = data[n:]

# Demoing a single sequence of training with a set of batch and block size
torch.manual_seed(1337) # For reproducability
batch_size = 4 # How many independent sequences are processed in parallel
block_size = 8 # Maximum context length for predictions

def get_batch(split):
    # generate a small batch of data of inputs x and y
    data = train_data if split == 'train' else val_data
    ix = torch.randint(len(data) - block_size, (batch_size,))
    x = torch.stack([data[i:i + block_size] for i in ix])
    y = torch.stack([data[i + 1:i + block_size + 1] for i in ix])
    return x, y

xb, yb = get_batch('train')
print('inputs:')
print(xb.shape)
print(xb)
print('targets:')
print(yb.shape)
print(yb)

#####
import torch.nn as nn
from torch.nn import functional as F
torch.manual_seed(1337) # For reproducability

class BigramLanguageModel(nn.Module):

    def __init__(self, vocab_size):
        super().__init__()
        # each token directly reads off the logits for the next token from a lookup table
        self.token_embedding_table = nn.Embedding(vocab_size, vocab_size)

    def forward(self, idx, targets):
        # idx and targets are both (B,T) tensor of integers
        logits = self.token_embedding_table(idx) # (B,T,C)

        B, T, C = logits.shape
        logits = logits.view(B * T, C)
        targets = targets.view(B * T)
        loss = F.cross_entropy(logits, targets)

        return logits, loss
    
    def generate(self, idx, max_new_tokens):
        # idx is (B, T) array of indices in the current context
        for _ in range(max_new_tokens):
            # get the predictions
            logits, loss = self(idx)
            # focus only on the last time step
            logits = logits[:, -1, :] # becomes (B, C)
            # apply softmax to get probabilities
            probs = F.softmax(logits, dim=-1) # (B, C)
            idx_next = torch.multinomial(probs, num_samples=1) # (B, 1)
            # append sampled index to the running sequence
            idx = torch.cat((idx, idx_next), dim=1) # (B, T + 1)
        return idx


    
m = BigramLanguageModel(vocab_size)
logits, loss = m(xb, yb)
print(logits.shape)
print(loss)