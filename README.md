# Mini Smart Projector — 3D Model Project

A dimensioned 3D reconstruction of the supplied mini LCD smart projector reference: 214 × 168 × 88 mm. The project includes:

- `assets/mini-smart-projector.stp` — neutral STEP AP214 solid exchange model for Creo import.
- `scripts/generate_step.py` — reproducible generator for the STEP body, lens, feet and rear I/O features.
- `web/` — an interactive Three.js preview with orbit controls, sectional callouts and preset views.

## Run the preview

```bash
python3 -m http.server 8080 --directory web
```

Open `http://localhost:8080`. The viewer imports Three.js from an ES-module CDN, so the browser needs internet access the first time.

## CAD notes

The coordinate system used by the STEP generator is millimetres. The front face is at **Y = -84 mm** and the model is centred about X = 0. The product envelope (including feet) is 214 × 168 × 88 mm. The `scripts/generate_step.py` output is a valid ISO 10303-21 / AP214 faceted B-rep; open it in Creo with **File → Open**, choosing STEP.
