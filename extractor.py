import re
import dateparser

# Muy básico: busca patrones de fechas comunes (ES/EN) en texto de resumen
DATE_PATTERNS = [
    r'\b\d{4}-\d{2}-\d{2}\b',  # 2025-09-12
    r'\b\d{1,2}/\d{1,2}/\d{2,4}\b',  # 12/09/2025
    r'\b\d{1,2}\s+de\s+\w+\s+de\s+\d{4}\b',  # 12 de septiembre de 2025
    r'\b(?:Septiembre|Setiembre|Octubre|Noviembre|Diciembre|Enero|Febrero|Marzo|Abril|Mayo|Junio|Julio|Agosto)\s+\d{1,2},\s+\d{4}\b',  # Septiembre 12, 2025
    r'\b(?:September|October|November|December|January|February|March|April|May|June|July|August)\s+\d{1,2},\s+\d{4}\b'
]

EMAIL_PATTERN = r'[\w\.-]+@[\w\.-]+\.\w+'

def extract_dates(text):
    candidates = []
    for pat in DATE_PATTERNS:
        candidates += re.findall(pat, text, flags=re.IGNORECASE)
    parsed = []
    for c in candidates:
        dt = dateparser.parse(c, languages=["es","en"])
        if dt:
            parsed.append(dt.date().isoformat())
    # quitar duplicados pero conservar orden
    seen = set()
    out = []
    for d in parsed:
        if d not in seen:
            seen.add(d)
            out.append(d)
    return out

def extract_emails(text):
    emails = re.findall(EMAIL_PATTERN, text)
    return list(dict.fromkeys(emails))
