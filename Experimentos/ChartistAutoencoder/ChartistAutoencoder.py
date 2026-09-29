"""
Autoencoder for learning chart patterns.

This model learns chart patterns and encodes them as normalized latent vectors
with values in the range [0, 1].

The reconstruction error between the input and the output can be used to assess
whether a pattern has been learned. The corresponding latent vector provides a 
compact representation of the pattern in the latent space.

Author: Javier Márquez Ruiz
"""

import torch
import torch.nn as nn

# Uses X0 to reconstruct the prices when "denormalizing".


class X0_LogNormalizer():
    @staticmethod
    def normalize(x: torch.Tensor, eps=None) -> torch.Tensor:
        """
        Since log(x) is computed, epsilon helps with small values to vaoid
        -infty.
        """
        # x2 = x.detach().clone()
        # if eps is not None:
        #     x2 = x + eps
        x0 = x[..., 0:1, :]  # [B, 1, n_features]
        if (x <= 0).any():
            raise ValueError("X0_LogNormalizer requires x > 0")
        y = torch.log(x) - torch.log(x0)  # x / x0
        if not torch.isfinite(y).all():
            print("Valores no finitos en normalize")
        return y

    @staticmethod
    def denormalize(x, x_original):
        x0 = x_original[..., 0:1, :]
        y = x0 * torch.exp(x)
        return y


class ChartistAutoencoder(torch.nn.Module):
    def __init__(self,
                 device: torch.device,
                 normalize_fn=X0_LogNormalizer.normalize,
                 denormalize_fn=X0_LogNormalizer.denormalize,
                 seq_len=24,
                 latent_dim=6,
                 n_features=4,
                 dtype=torch.float64,
                 hidden_dims=None):
        """
        Parameters
        ----------

        seq_len:
            Number of candles for pattern-recognition.

        n_features:
            Features per candle. Default 4: OHLC [Open, Highl, Low, Close]

        latent_dim:
            Nº values [0,1] in the latent space.
        
        hidden_dims:
            Features per layer. By default: 96 -> 256 -> 128 -> latent -> ...

        """
        super().__init__()

        self.seq_len = seq_len
        self.n_features = n_features
        self.normalize_fn = normalize_fn
        self.denormalize_fn = denormalize_fn
        self.latent_dim = latent_dim
        self.device = device

        input_dim = seq_len * n_features
        if hidden_dims is None:
            hidden_dims = [96, 256, 128]  # Works well for 24 candles
        self.encoder = self._create_encoder(input_dim, hidden_dims)
        self.decoder = self._create_decoder(output_dim=input_dim,  # Is an autoencoder...
                                            hidden_dims=hidden_dims)
        self.to(device=device, dtype=dtype)

    def encode(self, x: torch.Tensor) -> torch.Tensor:
        x = self.normalize_fn(x)
        z = self.encoder(x)
        return z

    def decode(self, z: torch.Tensor) -> torch.Tensor:
        x = self.decoder(z)
        x = x.reshape(-1, self.seq_len, self.n_features)
        return x

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        if x.ndim != 3:
            raise ValueError(
                f"Expected input shape [B, {self.seq_len}, {self.n_features}], "
                f"but got {tuple(x.shape)}."
            )
        _, seq_len, n_features = x.shape
        if seq_len != self.seq_len or n_features != self.n_features:
            raise ValueError(
                f"Expected input shape [B, {self.seq_len}, {self.n_features}], "
                f"but got {tuple(x.shape)}."
            )
        y = self.encode(x)
        x_pred = self.decode(y)
        x_pred = self.denormalize_fn(x_pred, x)
        return x_pred

    def get_latent(self, x: torch.Tensor) -> torch.Tensor:
        """
        Return the latent-space representation of the input.
        
        (Stops training and uses an eval mode, then resume).
        """
        was_training = self.training
        self.eval()
        with torch.inference_mode():
            z = self.encode(x)
        if was_training:
            self.train()
        return z

    def _create_encoder(self,
                        input_dims: int,
                        hidden_dims: list[int]) -> nn.Sequential:
        layers: list[nn.Module] = [nn.Flatten()]
        prev_dim = input_dims
        for dim in hidden_dims:
            layers.append(nn.Linear(prev_dim, dim))
            # nn.ReLU() Could be a parameter for the class: activation function
            layers.append(nn.ReLU())
            prev_dim = dim
        layers.append(nn.Linear(prev_dim, self.latent_dim))
        layers.append(nn.Sigmoid())
        return nn.Sequential(*layers)

    def _create_decoder(self,
                        output_dim: int,
                        hidden_dims: list[int]) -> nn.Sequential:
        """
        Constructs a model symetrical to the encoder.
        """
        layers: list[nn.Module] = []

        prev_dim = self.latent_dim
        for dim in reversed(hidden_dims):
            layers.append(nn.Linear(prev_dim, dim))
            layers.append(nn.ReLU())
            prev_dim = dim

        layers.append(nn.Linear(prev_dim, output_dim))

        return nn.Sequential(*layers)
