# Build macOS

## Importante

- La app para macOS debe generarse en un Mac.
- No se puede generar un `.app` fiable de macOS desde este Windows.

## Requisitos en el Mac

- Python 3.11 o similar
- un entorno virtual `.venv`
- dependencias del proyecto instaladas
- `pyinstaller` instalado en ese entorno

## Generar la app

Desde la raiz del proyecto en macOS:

```bash
chmod +x ./scripts/build_macos.sh
./scripts/build_macos.sh --clean
```

## Salida

La app se genera en:

```text
dist/MusSimulator.app
```

Las imagenes editables de cartas quedan tambien fuera del bundle en:

```text
dist/card_images
```

La aplicacion buscara las cartas en este orden:

1. `card_images` junto al ejecutable o junto al `.app`
2. `card_images` incluido dentro del bundle

## Flujo recomendado

1. Cambia el codigo.
2. Sustituye las cartas en `card_images/`.
3. Ejecuta `./scripts/build_macos.sh --clean` en un Mac.
4. Prueba `dist/MusSimulator.app`.

## Nombres de cartas

Mantiene estos nombres:

- `R.png`
- `C.png`
- `S.png`
- `A.png`
- `7.png`
- `6.png`
- `5.png`
- `4.png`
