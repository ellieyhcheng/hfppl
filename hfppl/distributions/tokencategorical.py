from .distribution import Distribution
from ..util import log_softmax
from ..llms import Token
import numpy as np

class TokenCategorical(Distribution):

    def __init__(self, lm, logits):     
        self.lm        = lm
        self.log_probs = log_softmax(logits)
        if self.lm.tokenizer.vocab_size != len(logits):
            raise RuntimeError(f"TokenCategorical: vocab size is {self.lm.tokenizer.vocab_size} but provided {len(logits)} logits.")

    def sample(self):
        n = np.random.choice(len(self.log_probs), p=(np.exp(self.log_probs)))
        return Token(self.lm, n, self.lm.tokenizer.convert_ids_to_tokens(n)), self.log_probs[n]

    def log_prob(self, value):
        return self.log_probs[value.token_id]
    
    def argmax(self, idx):
        tok = torch.argsort(self.log_probs)[-idx]
        return Token(self.lm, tok, self.lm.tokenizer.convert_ids_to_tokens(tok)), self.log_probs[tok]