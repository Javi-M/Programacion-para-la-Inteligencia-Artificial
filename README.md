# Programación para la Inteligencia Artificial
[![GitHub Pages](https://img.shields.io/badge/Web-GitHub%20Pages-blue?style=flat-square&logo=github)](https://javi-m.github.io/Programacion-para-la-Inteligencia-Artificial/)
[![Universidad de Málaga](https://img.shields.io/badge/UMA-Ingeniería%20Informática-purple?style=flat-square)](https://www.uma.es/)

Repositorio para la asignatura Programación para la Inteligencia Artificial, de la Universidad de Málaga.

Se basa en los apuntes originales (García-González, J. (2025). Programación para la Inteligencia Artificial. Universidad de Málaga), y por tanto no es necesariamente autocontenido. Es más bien una especie de extensión: aclaro o profundizo en lo que me haya generado dudas en algún momento o me parezca por cualquier motivo que quiero desarrollar más.

[Playlist de O'Reilly](https://learning.oreilly.com/playlists/7a20950b-7581-4ae1-bcbd-7212fc8d7b01)

## Contenidos

- [Terminología usada](GLOSSARY.md) - Términos clave, y funciones, métodos y clases importantes de PyTorch.
- [Experimentos/](Experimentos/) - Puesta en práctica de los conceptos. Notebooks jupyter. (No incluye prácticas de la asignatura).
- [Apuntes/](Apuntes/) - Apuntes Markdown.
  - [Recursos](Apuntes/0_Recursos.md) - Enlaces a conceptos de Python, explicaciones, artículos, etc.
  - [Hiperparámetros](Apuntes/1_Hiperparametros.md) - Batch size, learning rate, etc.
  - [Optimizadores](Apuntes/3_Optimizadores.md)
  - [Funciones de activación](Apuntes/4_Funciones_de_activación.md) - Sobre las funciones usadas en la
    asignatura para tal propósito (aunque son, simplemente, funciones normales y corrientes sobre tensores).
- [Preguntas/](Preguntas/) - Preguntas escritas en Quarto (`qmd`), para generar la web (GitHub Pages).
- [docs/](docs/) - Sitio web (archivos html para GitHub pages).

## Cuestiones a responder
Un propósito importante de este repositorio es intentar plantear las preguntas clave a saber responder. Las preguntas son tanto teóricas como de código. No están pensadas para visualizarlas desde el repositorio sino desde esta página:
🌐 [Preguntas en formato web](https://javi-m.github.io/Programacion-para-la-Inteligencia-Artificial/) 🌐 (GitHub Pages)


Las preguntas han sido gestionadas con Quarto (archivos `.qmd`) para ser luego reenderizadas a **html**. Puede probarse a reenderizar en pdf, pero no está garantizado que funcione.

(`cd Preguntas/` y ejecutar `quarto render`, o desde la raíz del repositorio:
`quarto render Preguntas`)

> Quarto es muy quisquilloso con su sintaxis Markdown.

## Uso de LLMs
Donde se hayan utilizado LLMs se menciona muy claramente. Además todo texto incluido ha sido revisado y nunca copiado y pegado sin supervisar. Más aún cuando tiene que adecuarse a los conceptos de la asignatura y no a conceptos "cualesquiera" de Inteligencia Artificial.

- Se ha usado LLMs para generar referencias `.bib`
- Se ha usado LLMs para generar algunas preguntas, mencionado explícitamente.
- Se han usado LLMs para revisiones de ortografía, norma, etc.

Ningún texto generado por LLMs se incluye sin revisión rigurosa, entre otros para adaptarlo al temario. Se ha intentado que sea transparente, mencionando las partes generadas por cualquier modelo.

Se ha hecho uso de LLMs para:
- Generación de las referencias `.bib`
- Generar algunas preguntas, mencionado explícitamente siempre.
- Revisiones ortográficas, gramaticales, de norma, estilo, etc.

## Reenderizar con Quarto

Está pensado para Linux.

Puede que tengas que darles permisos a `post-render.sh`: `chmod +x Preguntas/post-render.sh` o bien 
`cd Preguntas/`, y `chmod +x post-render.sh`

