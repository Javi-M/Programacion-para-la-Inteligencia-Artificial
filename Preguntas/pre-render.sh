#!/bin/sh
set -eu

# Directorio donde se encuentra este script
SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"

# Copia el glosario Markdown para que esté también en GitHub Pages.
# NO MODIFICAR GLOSSARY.qmd DIRECTAMENTE
cp "$SCRIPT_DIR/../GLOSSARY.md" "$SCRIPT_DIR/GLOSSARY.qmd"