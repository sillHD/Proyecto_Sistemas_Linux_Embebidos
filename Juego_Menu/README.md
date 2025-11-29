# Juego_Menu

Lanzador sencillo para elegir entre `Juego_1` y `Juego_2`.

Cómo usar:

- Abre PowerShell en la raíz del workspace (la carpeta que contiene `Juego_1` y `Juego_2`).
- Ejecuta:

```powershell
python .\Juego_Menu\main_menu.py
```

El menú detecta si `Juego_1/main_opl.py` y `Juego_2/main.py` existen y habilita/deshabilita los botones.

Notas:
- El lanzador arranca los juegos como procesos separados usando el mismo intérprete Python.
- Cerrar el juego vuelve al menú.
- Si prefieres, puedo añadir iconos, atajos o ejecutar los juegos en ventanas separadas/terminales.
