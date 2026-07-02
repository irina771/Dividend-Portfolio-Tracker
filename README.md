# 📈 Dividend Portfolio Tracker

Aplicación desarrollada en Python que consume la API de InvertirOnline (IOL) para obtener información financiera de CEDEARs, almacenar los datos en formato CSV y utilizarlos posteriormente en Power BI para análisis y visualización.

## 🎯 Objetivos

- Consumir la API REST de IOL.
- Obtener cotizaciones en tiempo real.
- Descargar series históricas.
- Registrar dividendos.
- Analizar una cartera de inversión.
- Crear dashboards interactivos en Power BI.


## Ejecutar el programa
- cd Dividend-Portfolio-Traker
- py main.py

## Arquitectura
```text
                +----------------+
                | InvertirOnline |
                +-------+--------+
                        |
                 OAuth Authentication
                        |
                        ▼
                Python Data Collector
                        |
        +---------------+----------------+
        |                                |
        ▼                                ▼
   prices.csv                   historical.csv
        |                                |
        +---------------+----------------+
                        |
                Portfolio Analytics
                        |
                        ▼
                Investment Simulator
                        |
                        ▼
                 simulation.csv
                        |
                        ▼
                Power BI Dashboard
```
---
## 🛠 Tecnologías

- Python
- Requests
- Pandas
- Power BI
- Git
- GitHub
- API REST
- CSV


## 📂 Estructura

```text
data/
├── ├── prices.csv
|   ├── historical.csv
|   ├── portfolio.csv
|   ├── simulation.csv
src/
├── auth.py
├── csv_manager.py
├── simulator.py
├── portfolio.py
├── api.py
```


## Pipeline
```
            API Invertir Online
                     │
                     ▼
            Extracción (Python)
                     │
                     ▼
          data/raw/
      ├── prices.csv
      ├── historical.csv
      └── dividends.csv
                     │
                     ▼
        Transformación (Pandas)
                     │
                     ▼
         data/processed/
      ├── portfolio.csv
      ├── simulation.csv
      └── portfolio_metrics.csv
                     │
                     ▼
             Power BI Dashboard
                     │
                     ▼
        KPIs • Dividendos • DCA
         Rendimiento • CAGR
```

---

## 📊 Funcionalidades

### ✔ Sprint 1 (Completado)
- Autenticación con API IOL
- Cotización en tiempo real
- Exportación a CSV

### ✔ Sprint 2 (Completado)
- Descarga de series históricas de cotizaciones
- Automatización y guardado de históricos

### ✔ Sprint 3 (Completado)
- **Pipeline ETL completo**: separación de datos en `raw/` y `processed/`
- **Métricas de Dividendos**: cálculo de Dividend Yield, Yield on Cost (YOC), ingreso anual proyectado y dividendos cobrados por año (2024, 2025, 2026) cruzando datos con `dividends.csv`.
- **Tipo de cambio dinámico**: consumo de la API de `dolarapi.com` para obtener el dólar CCL de referencia en tiempo real.
- **Simulador DCA con Reinversión**: simulación secuencial que incluye aportes, compras regulares, cobro de dividendos y reinversión para potenciar el interés compuesto.

### 🚧 Sprint 4 (Próximo)
- Dashboard interactivo en Power BI (KPIs, Gráficos históricos, Evolución de portafolio, DCA y Dividendos).

---

## 📌 CEDEARs analizados
- MO (Altria Group)
- PFE (Pfizer)
- T (AT&T)
- CVX (Chevron)
- VALE (Vale S.A.)

---

> [!NOTE]
> *Historical dividend data used for educational and analytical purposes.*

---

## Próximas mejoras
- Base de datos SQL
- Automatización diaria
- Dashboard web
- Análisis de riesgo