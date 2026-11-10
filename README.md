# Alarm
Alarma

## Descripción

**Alarm** es un proyecto personal de Python para realizar cuentas atrás, organizar actividades y avisar con una sirena cuando termina el tiempo. El repositorio conserva una versión inicial de consola de **2020**, una segunda versión con interfaz gráfica fechada en **2025**, el sonido original y archivos generados por **PyInstaller**.

Esta documentación describe el material conservado, sin cambiar el código ni presentar los ejecutables como aplicaciones verificadas.

## Versión original: `alarms_v1.py` (2020)

El encabezado del archivo indica **28 de noviembre de 2020**. La aplicación funciona en consola: muestra un menú, permite escoger una actividad o introducir una duración personalizada, imprime el tiempo restante y reproduce `sirena.mp3` al finalizar. Utiliza `time.perf_counter`, `pygame.mixer` y `pyautogui`.

| Opción | Actividad | Duración |
| --- | --- | --- |
| 1 | Abdominales | 28 minutos |
| 2 | Flexiones | 20 minutos |
| 3 | Flexibilidad | 10 minutos |
| 4 | Muslos | 10 minutos |
| 5 | Preparación | 4 minutos |
| 6 | Machine Learning | 90 minutos |
| 7 | Python | 90 minutos |
| 8 | Languages | 90 minutos |
| 9 | TFG | 120 minutos |
| 10 | Tiempo personalizado | Horas, minutos y segundos |
| 11 | Hover Mouse | Tiempo personalizado y movimiento del ratón |
| 12 | Salir | Cierra el programa |

En el modo normal, el sonido se activa durante los últimos diez segundos. El modo **Hover Mouse** mueve el cursor periódicamente para intentar evitar el bloqueo por inactividad y, al finalizar el tiempo, ejecuta una alarma adicional de diez segundos.

El programa separa las tareas en funciones: `menu`, `to_seconds`, `eleccion`, `user_time`, `alarm` y `hover_mouse`.

## Segunda versión: `alarms_v2.py` (2025)

El encabezado indica **10 de noviembre de 2025** y atribuye la actualización a **Avtomat Agentics**. Esta versión añade una interfaz de escritorio mediante **Tkinter**:

- Selector de actividades predefinidas y tiempo manual.
- Botones **Start**, **Pause**, **Resume** y **Reset**.
- Cuenta atrás en formato horas:minutos:segundos y barra de progreso.
- Casilla para activar el movimiento periódico del ratón.
- Aviso visual y reproducción de la sirena al terminar.

La lógica está organizada en las clases `CountdownTimer` (temporizador) y `TimerApp` (interfaz). La cuenta atrás se ejecuta en un hilo independiente.

Las funcionalidades anteriores se han identificado leyendo el código; **no se ha probado la aplicación en ejecución**.

## Estructura del repositorio

| Archivo | Contenido |
| --- | --- |
| [`alarms_v1.py`](alarms_v1.py) | Temporizador original por consola |
| [`alarms_v2.py`](alarms_v2.py) | Temporizador posterior con ventana |
| [`sirena.mp3`](sirena.mp3) | Sonido de alarma |
| [`alarms.spec`](alarms.spec) | Configuración histórica de PyInstaller |
| `Analysis-00.toc`, `EXE-00.toc`, `PKG-00.toc`, `PYZ-00.pyz`, `PYZ-00.toc`, `Tree-*.toc` | Archivos intermedios de compilación |
| `base_library.zip`, `pyimod*.pyc`, `struct.pyc` | Componentes auxiliares generados |
| `warn-alarms.txt`, `xref-alarms.html` | Informes de PyInstaller sobre importaciones y dependencias |

La configuración `alarms.spec` apunta a un archivo `alarms.py` en una ruta absoluta de un ordenador Windows antiguo. **Ese archivo no figura en la raíz actual del repositorio**, que contiene `alarms_v1.py` y `alarms_v2.py`. La configuración no es directamente reutilizable sin adaptarla.

## Cómo ejecutar el código fuente

Se requiere Python con las bibliotecas `pygame` y `pyautogui`; para la versión gráfica también se necesita `tkinter`.

```bash
pip install pygame pyautogui
python alarms_v1.py
```

Para la segunda versión, ejecutar `python alarms_v2.py` en lugar del comando anterior. El archivo `sirena.mp3` debe encontrarse en el directorio de trabajo desde el que se lanza el programa.

El movimiento automático del ratón requiere acceso a un escritorio gráfico.

## Archivos grandes: GitHub Releases

Los archivos de distribución no están en el árbol principal del repositorio, sino en el **[Release «Uploading .exe and .pkg»](https://github.com/alvgar23/Alarm/releases/tag/Test)**:

- `alarms.exe` — 272,7 MB.
- `alarms.pkg` — 272,4 MB.

Ambos se conservan como archivos históricos. No se ha verificado su funcionamiento ni qué versión concreta del código contienen. El `.pkg` procede del material de empaquetado; **su extensión no demuestra que sea un instalador de macOS**.

## Observaciones sobre el código original

El objetivo es conservar el proyecto, no refactorizarlo. En la lectura del código aparecen algunas cuestiones que conviene tener presentes:

- En la primera versión se muestra el menú dos veces al inicio.
- Durante los últimos diez segundos de `alarms_v1.py`, el mezclador y el archivo de audio se vuelven a inicializar/cargar repetidamente.
- En `alarms_v2.py`, el hilo de la cuenta atrás actualiza directamente elementos de Tkinter; esto podría ocasionar problemas, pues las actualizaciones de interfaz suelen requerir el hilo principal.
- Los archivos de PyInstaller contienen rutas y dependencias del entorno original.

No se han ejecutado pruebas, no se ha actualizado ninguna dependencia y **no se ha modificado ningún archivo original salvo este README**.

## Contexto

El proyecto refleja una etapa de aprendizaje de Python aplicada a una necesidad práctica: controlar sesiones de ejercicio y estudio con avisos sonoros. La primera versión exploró funciones, temporización, reproducción de audio y automatización del ratón; la segunda incorporó una interfaz gráfica y controles de pausa y reinicio. Los scripts, el audio y los archivos de compilación se conservan como registro de ambas etapas.
