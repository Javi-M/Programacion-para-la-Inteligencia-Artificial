Algoritmo SGD definido según la documentación de PyTorch <http://docs.pytorch.org/docs/2.14/generated/torch.optim.SGD.html> (código copiado del código fuente, en concreto de `SGD.__doc__`)

# class torch.optim.SGD

```python
class torch.optim.SGD (params, lr=0.001, momentum=0, dampening=0, 
                       weight_decay=0, nesterov=False, maximize=False, 
                       foreach=None, differentiable=False, fused=None)
```

$$
\begin{aligned}
    &\rule{110mm}{0.4pt}                                                                 \\
    &\textbf{input}      : \gamma \text{ (lr)}, \: \theta_0 \text{ (params)}, \: f(\theta)
        \text{ (objective)}, \: \lambda \text{ (weight decay)},                          \\
    &\hspace{13mm} \:\mu \text{ (momentum)}, \:\tau \text{ (dampening)},
    \:\textit{ nesterov,}\:\textit{ maximize}                                     \\
    &\rule{110mm}{0.4pt}                                                                 \\
    &\textbf{for} \: t=1 \: \textbf{to} \: \ldots \: \textbf{do}                         \\
    &\hspace{5mm}\textbf{if} \: \textit{maximize}:                                       \\
    &\hspace{10mm}g_t           \leftarrow   -\nabla_{\theta} f_t (\theta_{t-1})         \\
    &\hspace{5mm}\textbf{else}                                                           \\
    &\hspace{10mm}g_t           \leftarrow   \nabla_{\theta} f_t (\theta_{t-1})          \\
    &\hspace{5mm}\textbf{if} \: \lambda \neq 0                                           \\
    &\hspace{10mm} g_t \leftarrow g_t + \lambda  \theta_{t-1}                            \\
    &\hspace{5mm}\textbf{if} \: \mu \neq 0                                               \\
    &\hspace{10mm}\textbf{if} \: t > 1                                                   \\
    &\hspace{15mm} \textbf{b}_t \leftarrow \mu \textbf{b}_{t-1} + (1-\tau) g_t           \\
    &\hspace{10mm}\textbf{else}                                                          \\
    &\hspace{15mm} \textbf{b}_t \leftarrow g_t                                           \\
    &\hspace{10mm}\textbf{if} \: \textit{nesterov}                                       \\
    &\hspace{15mm} g_t \leftarrow g_{t} + \mu \textbf{b}_t                               \\
    &\hspace{10mm}\textbf{else}                                                   \\
    &\hspace{15mm} g_t  \leftarrow  \textbf{b}_t                                         \\
    &\hspace{5mm}\theta_t \leftarrow \theta_{t-1} - \gamma g_t                    \\
    &\rule{110mm}{0.4pt}                                                          \\
    &\bf{return} \:  \theta_t                                                     \\
    &\rule{110mm}{0.4pt}                                                          \\
\end{aligned}
$$



## Caso de **solo usar el argumento `lr`**

En el caso de solo usar `lr`, los demás argumentos se quedan por defecto. Podría decirse que el uso básico del SGD. Así queda el algoritmo:

$$
\begin{aligned}                                                    \\
    &\textbf{for} \: t=1 \: \textbf{to} \: \ldots \: \textbf{do}                        \\
    &\hspace{5mm}g_t           \leftarrow   \nabla_{\theta} f_t (\theta_{t-1})          \\
    &\hspace{5mm}\theta_t \leftarrow \theta_{t-1} - \gamma g_t                    \\
    &\rule{110mm}{0.4pt}                                                          \\
    &\bf{return} \:  \theta_t                                                     \\
    &\rule{110mm}{0.4pt}                                                          \\
\end{aligned}
$$

Que es como escribir que la regla para actualizar los parámetros:
$$
\theta_t \leftarrow \theta_{t-1} - \gamma \nabla_\theta f_t(\theta_{t-1})
$$

donde:
- $\theta_t$: parámetros tras la actualización.
- $\theta_{t-1}$: parámetros antes de la actualización.
- $\gamma$: _learning rate_, `lr`. Tasa de aprendizaje.
- $f_t(\theta_{t-1})$: función objetivo **que no recibe como argumento**. 
    Es la `loss_fn`, externa, que se encuentra en el bucle de entrenamiento y al llamarla `loss = loss_fn(...)` y luego con `loss.backward()` calcula los gradientes.
- $\nabla_\theta f_t(\theta_{t-1})$: es el gradiente de esa pérdida respecto a 
    los parámetros del modelo. `loss.backward()` (que ocurre de forma externa al optimizador) lo calcula y lo acumula en `param.grad`

(ChatGPT):
> Es decir, el optimizador recibe `params`, que contiene los parámetros del 
> modelo que debe actualizar. A través del atributo `param.grad` (para cada 
> parámetro en `params`), accede al gradiente de la función de pérdida, 
> $\nabla_\theta f_t(\theta_{t-1})$, respecto a cada parámetro, previamente 
> calculado mediante `loss.backward()`.

## Caso de usar _momentum_ (y `lr`)

(Caso de minimizar, como es común).
SGD con _momentum_. Es decir $\mu \ne 0$. Sin _dampening_. 

En el siguiente algoritmo se puede apreciar que para $t=0$, como no hay _momentum buffer_ previo, se le asigna simplemente el primer gradiente.

$$
\begin{aligned}
    &\textbf{for} \: t=1 \: \textbf{to} \: \ldots \: \textbf{do}                         \\
    &\hspace{5mm}g_t           \leftarrow   \nabla_{\theta} f_t (\theta_{t-1})          \\
    &\hspace{5mm}\textbf{if} \: t > 1                                                   \\
    &\hspace{10mm} \textbf{b}_t \leftarrow \mu \textbf{b}_{t-1} + g_t           \\
    &\hspace{5mm}\textbf{else}                                                          \\
    &\hspace{10mm} \textbf{b}_t \leftarrow g_t                                           \\
    &\hspace{5mm} g_t  \leftarrow  \textbf{b}_t                                         \\
    &\hspace{5mm}\theta_t \leftarrow \theta_{t-1} - \gamma g_t                    \\
    &\rule{110mm}{0.4pt}                                                          \\
    &\bf{return} \:  \theta_t                                                     \\
    &\rule{110mm}{0.4pt}                                                          \\
\end{aligned}
$$

Excepto para la primera actualización ($t=0$), donde se usa el gradiente a secas, la regla queda como:

$$
g_t \leftarrow   \nabla_{\theta} f_t (\theta_{t-1})  \\
\textbf{b}_t \leftarrow \mu \textbf{b}_{t-1} + g_t \\
\theta_t \leftarrow \theta_{t-1} - \gamma b_t 
$$

Es decir se usa el búfer de momentum y el gradiente $g_t$ nuevo.

donde:
- $\textbf{b}_{t-1}$: búfer de momentum, que acumula los gradientes anteriores.
- $\mu$: coeficiente de _momentum_. Es decir cuánto pesa "los gradientes acumulados".
