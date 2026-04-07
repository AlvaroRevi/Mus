# Build Windows

## Requisitos

- Tener el entorno virtual `.venv`
- Tener instalado `pyinstaller` en ese entorno

## Generar el ejecutable

Desde la raiz del proyecto:

```powershell
.\scripts\build_windows.ps1
```

Si quieres regenerarlo limpiando `build/` y `dist/` antes:

```powershell
.\scripts\build_windows.ps1 -Clean
```

## Salida

El ejecutable se genera en:

```text
dist\MusSimulator\MusSimulator.exe
```

La carpeta de imagenes que usara el `.exe` estara en:

```text
dist\MusSimulator\card_images
```

## Flujo recomendado cuando cambies la app

1. Cambia el codigo.
2. Sustituye las cartas en `card_images\` si hace falta.
3. Ejecuta `.\scripts\build_windows.ps1 -Clean`.
4. Prueba `dist\MusSimulator\MusSimulator.exe`.

## Nombres de cartas

Debes mantener estos nombres dentro de `card_images\`:

- `R.png`
- `C.png`
- `S.png`
- `A.png`
- `7.png`
- `6.png`
- `5.png`
- `4.png`
