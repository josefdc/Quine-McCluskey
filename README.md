# Quine-McCluskey
Simplificador Quine-McCluskey con Interfaz Gráfica
-------------------------------------------------

Este proyecto proporciona una herramienta gráfica para simplificar expresiones booleanas utilizando el método Quine-McCluskey.

#### Componentes Principales:

1. **Interfaz Gráfica (epic_gui.py):**
   - Desarrollado usando la biblioteca PyQt5.
   - Proporciona una ventana principal (`QMApp`) desde donde los usuarios pueden interactuar con la aplicación.
   
2. **Simplificador Quine-McCluskey (qm_auto.py):**
   - Implementa el método Quine-McCluskey para simplificar expresiones booleanas.
   - Utiliza la biblioteca `pyeda` para manipulación y simplificación de expresiones booleanas.
   
#### Cómo Usar:

1. Asegúrate de tener PyQt5 y pyeda instalados en tu entorno virtual o sistema.
2. Ejecuta el archivo `epic_gui.py` para iniciar la interfaz gráfica.
3. Introduce la expresión booleana y los minterms en los campos correspondientes en la interfaz.
4. Haz clic en el botón correspondiente para obtener la expresión simplificada.

#### Dependencias:

- PyQt5
- pyeda

#### Contribuciones:

Las contribuciones son bienvenidas. Por favor, abre un "pull request" con mejoras o reporta problemas/bugs en la sección de "issues".
