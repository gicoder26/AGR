# Astara Growth Radar

App web móvil para revisar señales públicas del mercado automotriz peruano, marcas Astara, competencia y acciones sugeridas.

## Archivos

- `index.html`: app completa en HTML/CSS/JS.
- `data.json`: datos que consume la app.
- `scripts/update-data.py`: actualiza noticias desde fuentes públicas.
- `.github/workflows/update-data.yml`: corre la actualización todos los días a las 8:00 a.m. Perú.

## Cómo publicarla en GitHub Pages

1. Crea un repositorio nuevo.
2. Sube todos estos archivos respetando las carpetas.
3. En GitHub entra a `Settings > Pages`.
4. En `Build and deployment`, elige `Deploy from a branch`.
5. Selecciona branch `main` y carpeta `/root`.
6. Guarda.

La app quedará como link web y se podrá abrir desde celular. En iPhone/Android se puede agregar a la pantalla de inicio.

## Automatización

El workflow actualiza `data.json` todos los días usando Google News RSS y fuentes públicas. Los KPIs oficiales de AAP/SUNARP se mantienen como base hasta que se conecte una fuente estructurada mensual.
