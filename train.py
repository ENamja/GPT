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

print(encode('hello world'))
print(decode(encode('hello world')))