En realidad (de momento) no es un glosario, sino una **lista de términos** utilizados. 
<!-- En cualquier caso, si es una cuestión de PyTorch se puede buscar
en su documentación, o por lo demás en internet o los apuntes. Esta lista
es más que nada para tener presentes los términos con los que estar
familiarizado. -->

**Propuesta de estudio**: empieza a recorrer los términos, o elige un subconjunto, y habla/escribe todo lo que puedas sobre cada uno. (Ecuaciones, relaciones con otros conceptos, etc.)

# Funciones de error
- Error absoluto - _Absolute Error_ - AE
    - Error absoluto medio - _Mean Absolute Error_ - MAE
    - `L1Loss()`
- Error cuadrático - _Squared Error_ - SE
    - Error cuadrático medio - _Mean Squared Errro_ - MSE
    - `MSELoss()`
- Entropía Cruzada - _Cross Entropy_ - CE
- Entropía Binaria Crucada - _Binary Cross-Entropy_ - BCE

## Otras métricas
- _Accuracy_
- _Precision_
- _Recall_

# Funciones de activación
- Sigmoide
- Tangente hiperbólica - `torch.tanh()`
- ReLU
- LeakyReLU
- Softmax
- LogSoftmax

# Técnicas de regularización
- Parada temprana - _Early Stopping_
- Aumentado de datos
  - Condicionante de consistencia
- _Weight decay_
- Regularización L2
- Regularización L1 - <b style="color: red">no confundir con <code>torch.nn.L1Loss</code></b>
- Max-Norm
- Normalización de lote - _batch normalization_
- Dropout
- _Elastic Weight Consolidation_
- FGSM
- PGD


# PyTorch
- `state_dict()`
- `torch.cat()`
- `torch.linspace()`
- `torch.optim.SGD`
- `torch.nn.Sequential()`
- `torch.nn.Linear()`
- `torch.nn.Tanh()`
- `torch.normal()`
- `torch.rand()`
- `torch.ones_like()`
- `torch.unsqueeze(input, dim)`
- `torch.nn.BCELoss()`
- `torch.nn.LazyLinear()`
- `torch.nn.ModuleList()`
- `torch.nn.ModuleDict()`
- `torch.zeros_like()`
- `torch.nn.functional.one_hot()`
- `torch.nn.Softmax()`
- `torch.nn.CrossEntropyLoss()`
- `torch.nn.LogSoftmax()`

# Miscelánea (o _por organizar_)
- Autoencoder
- Neurona lineal
- Pasada hacia adelante - _Forward pass_
- Pasada hacia detrás - _Backwards pass_
- Red neuronal prealimentada - _Feed Forward Neural Network_
- Sesgo - _bias_ - $b$
- Matriz de confusión
- _One-hot encoding_
- Problema del desvanecimiento del gradiente
- Zona de saturación