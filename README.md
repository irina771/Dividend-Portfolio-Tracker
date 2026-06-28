# 📈 Dividend Portfolio Tracker

Aplicación desarrollada en Python que consume la API de InvertirOnline (IOL) para obtener información financiera de CEDEARs, almacenar los datos en formato CSV y utilizarlos posteriormente en Power BI para análisis y visualización.

## 🎯 Objetivos

- Consumir la API REST de IOL.
- Obtener cotizaciones en tiempo real.
- Descargar series históricas.
- Registrar dividendos.
- Analizar una cartera de inversión.
- Crear dashboards interactivos en Power BI.

---

## 🛠 Tecnologías

- Python
- Requests
- Pandas
- Power BI
- Git
- GitHub
- API REST

---

## 📂 Estructura

```text
data/
│
├── prices.csv
├── historical.csv
├── portfolio.csv
├── dividends.csv
└── companies.csv

src/
│
├── auth.py
├── api.py
├── csv_manager.py
├── historical.py
├── portfolio.py
└── utils.py
```

---

## 📊 Funcionalidades

### ✔ Sprint 1

- Autenticación con API IOL
- Cotización en tiempo real
- Exportación a CSV

### 🚧 Sprint 2

- Series históricas
- Automatización

### 🚧 Sprint 3

- Dividendos
- Indicadores financieros

### 🚧 Sprint 4

- Dashboard Power BI

### 🚧 Sprint 5

- Simulador de inversiones

---

## 📌 CEDEARs analizados

- MO
- PFE
- T
- CVX
- VALE

---

## Próximas mejoras

- Base de datos SQL
- Automatización diaria
- Dashboard web
- Simulador de dividendos
- Análisis de riesgo