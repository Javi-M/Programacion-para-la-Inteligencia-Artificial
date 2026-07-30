import pandas as pd
from torch.utils.data import Dataset
import torch

# Procesamiento hecho en spaceship_1.ipynb
def process_data_1(df_in:pd.DataFrame, inplace=False, transported_column=True):
    """ 
    Por defecto crea otro dataframe, no lo hace inplace.
    
    Valores NaN: -1. Puesto que todos los valores del df son positivos, y hay
    demasiados nulos como para eliminarlos.
    
    Returns:
        - df procesado
        - lista de columnas numericas usadas como input para entrenar
    """
    
    if not inplace:
        df = df_in.copy()
    else:
        df = df_in
        
    df = df.drop(columns=["Name"])
    
    # Split cabin en 3 columnas distintas. Tratamiento de nulos
    df["Cabin_1"] = df["Cabin"].apply(lambda x: x.split("/")[0] if not pd.isna(x) else x)
    df["Cabin_2"] = df["Cabin"].apply(lambda x: x.split("/")[1] if not pd.isna(x) else x)
    df["Cabin_3"] = df["Cabin"].apply(lambda x: x.split("/")[2] if not pd.isna(x) else x)
    
    # Convertir a columnas numéricas
    df["Cabin_1"] = df["Cabin_1"].apply(lambda x: ord(x) - ord('A') if not pd.isna(x) else -1)
    # P -> 1, S -> 0, na -> -1
    df["Cabin_3"] = df["Cabin_3"].apply(lambda x: -1 if pd.isna(x) else 1 if x == 'P' else 0)
    
    planets = {
        'Europa': 1,
        'Earth': 2,
        'Mars': 3
    }
    
    # Convertir a columna numérica. Tratamiento de nulos
    df["HomePlanet"] =  df["HomePlanet"].apply(lambda x: planets[x] if not pd.isna(x) else -1)
    
    destination = {
        'TRAPPIST-1e': 1,
        'PSO J318.5-22': 2,
        '55 Cancri e': 3
    }
    
    df["Destination"] = df["Destination"].apply(lambda x: destination[x] if not pd.isna(x) else -1)
    
    df["VIP"] = df["VIP"].apply(lambda x: 1 if True and not pd.isna(x) 
                                else 0 if False and not pd.isna(x)
                                else -1)
    
    # Por que hago x==True? porque si pongo "x" simplemente, podria ser un na y fallar
    # por no ser un booleano.
    df["CryoSleep"] = df["CryoSleep"].apply(lambda x: 1 if x==True and not pd.isna(x) 
                                    else 0 if False and not pd.isna(x)
                                    else -1)
    
    # De antemano he visto que no tiene valores nulos
    if transported_column:
        df["Transported"] = df["Transported"].apply(lambda x: 1 if x else 0)
    
    input_columns = ["HomePlanet", "CryoSleep", "Destination", "Age", "VIP", 
                     "RoomService", "FoodCourt", "ShoppingMall", "Spa", "VRDeck",
                     "Cabin_1", "Cabin_2", "Cabin_3"]

    if transported_column:
        df[input_columns + ["Transported"]] = df[input_columns + ["Transported"]].astype(float)
    else:
        df[input_columns] = df[input_columns].astype(float)
        
    # Más tratamiento de valores nulos
    # df.Age, df.RoomService, df.FoodCourt, df.ShoppingMall, df.Spa, df.VRDeck,
    # df.Cabin_2
    mean_Age = df.Age.mean()
    df.Age = df.Age.apply(lambda x: -mean_Age if pd.isna(x) else x)
    
    mean_RoomService = df.RoomService.mean()
    df.RoomService = df.RoomService.apply(lambda x: -mean_RoomService if pd.isna(x) else x)
    
    mean_FoodCourt = df.FoodCourt.mean()
    df.FoodCourt = df.FoodCourt.apply(lambda x: -mean_FoodCourt if pd.isna(x) else x)
    
    mean_ShoppingMall = df.ShoppingMall.mean()
    df.ShoppingMall = df.ShoppingMall.apply(lambda x: -mean_ShoppingMall if pd.isna(x) else x)
    
    mean_Spa = df.Spa.mean()
    df.Spa = df.Spa.apply(lambda x: -mean_Spa if pd.isna(x) else x)
    
    mean_VRDeck = df.VRDeck.mean()
    df.VRDeck = df.VRDeck.apply(lambda x: -mean_VRDeck if pd.isna(x) else x)
    
    mean_Cabin_2 = df.Cabin_2.mean()
    df.Cabin_2 = df.Cabin_2.apply(lambda x: -mean_Cabin_2 if pd.isna(x) else x)
    
    return df, input_columns

# Para ir acostumbrando a usar dataset y dataloader de PyTorch
class SpaceshipDatset_1(Dataset):
    """ Batch size: 1. Es decir "fila a fila" """
    def __init__(self, df:pd.DataFrame, input_columns:list[str]):
        self.input_columns = sorted(input_columns)
        self.df = df.sort_index(axis=1)
        
    def __len__(self):
        return len(self.df)
    
    def __getitem__(self, idx:int):
        X = torch.Tensor(self.df[self.input_columns].iloc[idx].to_list())
        Y = self.df["Transported"].iloc[idx]
        return X, Y