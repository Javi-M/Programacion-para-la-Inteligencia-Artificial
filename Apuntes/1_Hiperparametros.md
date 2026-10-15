# Hiperparámetros

¿Qué son los hiperparámetros? ¿De qué manera afecta cada hiperparámetro al aprendizaje? ¿Cómo se elige la forma de _ajustar_ estos hiperparámetros? (Tuning).

## Número de _epochs_
Este parámetro es bastante intuitivo. Demasiadas épocas pueden llevar al sobreajuste, mientras que demasiadas pocas pueden hacer que el modelo no haya aprendido lo suficiente.

Observando las métricas de entrenamiento y validación y, una vez finalizado el entrenamiento, los resultados sobre el conjunto de test, podemos decidir si es necesario seguir entrenando o detener el entrenamiento.

Si el rendimiento se estanca, puede ser necesario revisar otros aspectos del entrenamiento. Si el modelo sigue mejorando en validación y no parece estar sobreajustando, puede ser conveniente entrenar durante más épocas.

Una técnica habitual es utilizar early stopping, que detiene el entrenamiento cuando la métrica de validación deja de mejorar durante un determinado número de épocas.

## Batch size
Un _batch size_ más grande hará que el gradiente tenga menos ruido y que el entrenamiento sea más estable/tenga menos variabilidad. La relación entre _batch size_ y generalización es compleja.

Un _batch size_ grande consume (como cabe esperar) más memoria. Un ejemplo aproximado: para  10.000 imágenes de 1 MB cada una, 10 GB de memoria gráfica... no es poco. Sin embargo, el entrenamiento tardará menos.

Un _batch size_ más pequeño introduce más ruido en las actualizaciones, lo que puede favorecer la exploración.

## Ratio de aprendizaje (learning rate)
Una tasa de aprendizaje demasiado alta puede llevar a actualizaciones que _salten_ un ajuste adecuado. 

Un ratio de aprendizaje demasiado bajo puede llevar a hacer parecer que el aprendizaje se estanca.