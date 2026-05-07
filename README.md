# Astara Growth Radar

App web móvil/PWA para revisar señales públicas del mercado automotriz peruano desde el celular.

## Qué cambió en esta versión

- `Hoy` queda como resumen ejecutivo de datos, sin tarjetas falsas que parezcan desplegables.
- Las cards de KPI se ajustan a mobile y no se salen de pantalla.
- `Mercado` tiene lectura más senior: volumen, SUV, electrificados, flotas/pickups y tipo de cambio.
- `Marcas` compara números públicos por marca cuando existen en AAP/SUNARP.
- `Competencia` muestra ranking, unidades, participación, crecimiento e insight.
- `Fuentes públicas` queda escondido dentro de un desplegable.
- Se agrega autoría: “Desarrollado por Giulliana Mantilla · 2026”.
- Se agrega `manifest.json`, favicon, apple-touch-icon y service worker para que aparezca como app al guardarla en el inicio del celular.

## Archivos

- `index.html`: app completa en HTML/CSS/JS.
- `data.json`: datos que consume la app.
- `manifest.json`: nombre, ícono y configuración para instalarla en pantalla de inicio.
- `sw.js`: service worker básico para comportamiento tipo app.
- `assets/`: íconos de la app.
- `scripts/update-data.py`: actualiza timestamp real, noticias públicas y tipo de cambio referencial.
- `.github/workflows/update-data.yml`: corre la actualización todos los días a las 8:00 a.m. Perú.

## Cómo publicarla en GitHub Pages

1. Crea un repositorio nuevo.
2. Sube todos estos archivos respetando las carpetas.
3. En GitHub entra a `Settings > Pages`.
4. En `Build and deployment`, elige `Deploy from a branch`.
5. Selecciona branch `main` y carpeta `/root`.
6. Guarda.

## Cómo agregarla al inicio del celular

### iPhone
Abre el link en Safari > botón compartir > `Agregar a pantalla de inicio`.

### Android
Abre el link en Chrome > menú de tres puntos > `Agregar a pantalla principal` o `Instalar app`.

El nombre aparecerá como **Astara Radar** y el ícono usará la marca visual de Astara.

## Automatización

El workflow actualiza `data.json` diariamente. Los KPIs oficiales de AAP/SUNARP se mantienen como base hasta que se publique un nuevo reporte mensual, porque esa data no sale todos los días.
