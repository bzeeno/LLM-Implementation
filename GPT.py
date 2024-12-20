import torch
import torch.nn as nn

from gpt2_config import GPT2_CONFIG_124M
from Transformer import TransformerBlock
from LayerNormalization import LayerNorm

class GPTModel(nn.Module):
    def __init__(self, config):
        super().__init__()
        # Inputs to transformer layers
        self.token_embdg_layer = nn.Embedding(config.vocab_size, config.embedding_dimension)
        self.pos_embdg_layer = nn.Embedding(config.context_length, config.embedding_dimension)
        self.embdg_dropout = Dropout(config.drop_rate)

        # Transformer layers
        self.transformer_blocks = nn.Sequential(*[TransformerBlock(config) for _ in range(config.n_transformer_blocks)])
        
        # Output layers
        self.final_layer_norm = LayerNorm(config.embedding_dimension)
        self.out_head = nn.Linear(config.embedding_dimension, config.vocab_size)

    def forward(self, token_seq):
        # Initialize size and embeddings
        num_batches, seq_length = token_seq.shape
        token_embdgs = self.token_embdg_layer(token_seq)
        pos_embdgs = self.pos_embdg_layer(torch.arange(0, seq_length, device=token_seq.device))
        # Get embeddings and dropout
        embdgs = token_embdgs + pos_embdgs
        self.embdg_dropout(embdgs)
        # Pass embeddings into transformer blocks
        x = self.transformer_blocks(embdgs)
        # Output from transformer blocks to final layer norm
        x = self.final_layer_norm(x)
        # Get final logits
        logits = self.out_head(x)
        return logits
