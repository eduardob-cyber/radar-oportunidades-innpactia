# Convocatorias Radar (Starter)

Este es un MVP **sin costo** para automatizar la **búsqueda básica** de convocatorias usando:
- **GitHub Actions (cron)** para correr automáticamente cada 6–12 horas
- **Python** para leer fuentes **RSS** (evitamos scraping complejo)
- **CSV** como salida lista para revisar o importar a tu base/Sheets

> Meta de este MVP: tener **alertas automáticas** con oportunidades nuevas de fuentes confiables, sin pagar suscripciones y sin configurar servidores.

---

## ⚡ Qué hace
1. Lee las fuentes listadas en `sources.json` (preferiblemente **RSS** de organismos multilaterales, ONU, UE, bancos de desarrollo, fundaciones).
2. Descarga los ítems nuevos (título, link, fecha, resumen).
3. Hace **deduplicación** por URL.
4. Intenta extraer **fecha de cierre** y **emails** por reglas simples (si existen).
5. Guarda un `output/convocatorias_YYYYMMDD.csv` con las novedades del día.

> Nota: Este MVP **NO** usa LLMs ni scraping avanzado. Es a propósito: empezar rápido y gratis. Luego se puede evolucionar con clasificación (16 tipos), embeddings y RAG.

---

## 🧰 Requisitos rápidos
- Cuenta de **GitHub** (gratis)
- Nada más. GitHub corre el flujo por ti.

---

## 🚀 Pasos (20–30 min)

### 1) Crea tu cuenta en GitHub
- Ir a https://github.com/ → **Sign up** → confirma email.

### 2) Crea un repositorio desde este ZIP
1. Descarga el ZIP desde ChatGPT.
2. En GitHub, arriba a la izquierda: **+ → New repository** → pon nombre: `convocatorias-radar`.
3. Sube el contenido del ZIP (**Add file → Upload files**) y **Commit**.

### 3) Activa GitHub Actions
- Ve a la pestaña **Actions** del repo → te pedirá confirmar que confías en el workflow → **I understand… Enable**.

### 4) Edita tus fuentes en `sources.json`
- Abre `sources.json` y **reemplaza** o agrega tus RSS (ejemplos incluidos).
- Empieza con 5–10 fuentes para probar.

### 5) (Opcional) Cambia la frecuencia del cron
- Abre `.github/workflows/convocatorias.yml` y ajusta la línea `cron: "0 */12 * * *"`:
  - Cada 6 horas: `0 */6 * * *`
  - Cada día a las 7am: `0 7 * * *`

### 6) Revisa resultados
- Cuando corra la acción, verás el archivo `output/convocatorias_YYYYMMDD.csv` en el repo (o en la pestaña **Actions → Artifacts**).
- Descárgalo y compártelo con tu equipo.

---

## 📁 Estructura
```
.
├── pipeline.py
├── sources.json
├── extractor.py
├── requirements.txt
├── output/                  # resultados (se crea en runtime)
├── .github/workflows/convocatorias.yml
└── .gitignore
```

---

## 🔧 Cómo agregar fuentes (rápido)
Edita `sources.json` y agrega objetos con `"type": "rss"` y `"url": "..."`. Ejemplo:
```json
{
  "sources": [
    {"name": "UNDP Procurement", "type": "rss", "url": "https://example.org/undp/procurement/rss"},
    {"name": "EU Funding & Tenders", "type": "rss", "url": "https://example.org/eu/funding/rss"}
  ]
}
```

> Tip: muchas webs tienen el icono de RSS o la palabra “feed”, “rss”, “atom”. Si solo tienen newsletter por email, puedes usar su RSS si lo ofrecen, o dejarla para una fase 2.

---

## 🧪 Prueba local (opcional)
Si quieres correr en tu máquina:
```bash
python -m venv .venv
source .venv/bin/activate  # en Windows: .venv\Scripts\activate
pip install -r requirements.txt
python pipeline.py
```

---

## ➡️ Próximos pasos (cuando esto funcione)
- **Clasificación** a 16 tipos con zero-shot (HuggingFace).
- **Embeddings + Vector DB** (Chroma/FAISS) para búsquedas.
- **Push a Google Sheets/Airtable** con API.
- **Reportes por email/Slack**.
- **Validación de campos** (tu checklist de Marketplace) y flags de “no especificado”.

Hecho con cariño para INNPACTIA. ✨
