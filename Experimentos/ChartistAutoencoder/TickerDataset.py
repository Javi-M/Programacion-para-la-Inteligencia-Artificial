from torch.utils.data import Dataset
import pandas as pd
import torch

class TickerDataset(Dataset):
    def __init__(self, 
                 df_ticker:pd.DataFrame, 
                 n_candles:int, 
                 features:list[str],
                 device:torch.device):
        """
        Dataset of sliding windows extracted from a single ticker time series.

        Parameters
        ----------
        df_ticker:
        DataFrame containing the columns specified in `features`.

        n_candles:
        Number of consecutive candles per sample.

        features:
        List of feature names to include in each sample
        (e.g. ["Open", "High", "Low", "Close"]).

        device:
        Device where tensors will be created.

        Notes
        -----
        The dataset generates overlapping sliding windows of length
        `n_candles`.

        Each sample has shape:

        (n_candles, len(features))

        If the DataFrame contains N rows, the dataset length is:
        N - n_candles + 1
        """
        self.n_candles = n_candles
        self.data = (
            df_ticker[features]
            .dropna()
            .to_numpy(dtype="float64")
        )
        self.device = device

    def __len__(self):
        return len(self.data) - self.n_candles + 1

    def __getitem__(self, idx):
        x = torch.tensor(
            self.data[idx:idx + self.n_candles],
            dtype=torch.float64,
            device=self.device
        )
        return x