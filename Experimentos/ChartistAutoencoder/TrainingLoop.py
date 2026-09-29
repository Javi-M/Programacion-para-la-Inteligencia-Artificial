# Poder setear batch_size y crear dataloader dentro
# Mientras mas parámetros mejor para repetir

import torch
from torch.utils.data import DataLoader
from typing import Callable
from tqdm.auto import tqdm


def train_autoencoder(
    model,
    train_dataloader: DataLoader,
    epochs: int,
    loss_fn: Callable,
    optimizer: torch.optim.Optimizer,
    device: torch.device = torch.device("cpu"),
    val_dataloader: DataLoader | None = None,
    dtype=torch.float64
):
    """
    Entrena un autoencoder.

    Parameters
    ----------
    model : nn.Module
        Model to train.

    Returns
    -------
    model : nn.Module
        Trained model

    epoch_losses : list
        Mean loss per epoch
    """

    model = model.to(device)

    train_losses = []
    val_losses = []

    with tqdm(range(epochs), desc="epoch") as pbar:
        for epoch in pbar:

            # TRAIN
            batch_losses = []
            model.train()

            for x in train_dataloader:
                x = x.to(device, dtype=torch.float64)

                optimizer.zero_grad()
                x_pred: torch.Tensor = model(x)
                if x_pred.isinf().any():
                    print("Valores INF en x_pred (bucle entrenamiento)")
                loss = loss_fn(x_pred, x)
                loss.backward()
                batch_losses.append(loss.item())
                optimizer.step()

            epoch_loss = sum(batch_losses) / len(batch_losses)
            train_losses.append(epoch_loss)

            current_lr = optimizer.param_groups[0]["lr"]

            # VALIDATION
            if val_dataloader is not None:
                model.eval()
                batch_val_losses = []

                with torch.inference_mode():
                    for x in val_dataloader:
                        x = x.to(device, dtype=dtype)
                        x_pred = model(x)
                        loss = loss_fn(x_pred, x)
                        batch_val_losses.append(loss.item())

                epoch_val_loss = sum(batch_val_losses) / len(batch_val_losses)
                val_losses.append(epoch_val_loss)

            else:
                # So it has the same length as train_losses
                val_losses.append(None)
                epoch_val_loss = None

            postfix = {
                "loss": f"{epoch_loss:.4e}",
                "lr": f"{current_lr:.2e}"
            }

            if epoch_val_loss is not None:
                postfix["val_loss"] = f"{epoch_val_loss:.4e}"

            pbar.set_postfix(postfix)

    return model, train_losses, val_losses
