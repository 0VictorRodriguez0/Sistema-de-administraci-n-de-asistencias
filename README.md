# Sistema-de-administraci-n
Proyecto de ingeniería en software para el desarrollo de un sistema de administración de empleados.
## 1. Configuración del Entorno Virtual
Primero, debes crear y activar un entorno virtual para aislar las dependencias del proyecto. 
Ejecuta los siguientes comandos en tu terminal **dentro de la carpeta** <span style="color:blue">`Asistente_Academico_`</span>:



1. **Crear un entorno virtual:**
    ```bash
    python -m venv venv
    ```

2. **Si estás en PowerShell, asegúrate de permitir la ejecución de scripts:**
    ```bash
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
    ```

3. **Activar el entorno virtual:**
    ```bash
    .\venv\Scripts\activate
    ```


Al activar el entorno, verás que el prompt de la terminal cambia, indicando que estás trabajando dentro del entorno virtual.

## 2. Instalación de Librerías
Una vez que el entorno virtual esté activo, instala las librerías necesarias para ejecutar el asistente virtual. Es recomendable que las dependencias estén definidas en un archivo `requirements.txt`. Para instalar las librerías, ejecuta:

```bash
pip install -r requirements.txt
```
