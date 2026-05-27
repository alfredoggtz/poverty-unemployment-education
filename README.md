# 📊 Poverty, Unemployment & Education Analysis
> Final Project – Universidad Autónoma de Baja California (UABC)

A data analysis system that collects, stores, and visualizes socioeconomic indicators for Mexico related to poverty, education, and unemployment. The project integrates a Python data pipeline, a MySQL relational database, a Streamlit dashboard, and a MongoDB NoSQL layer.

---

## 👥 Team Members

| Name |
|------|
| Galvan Gutierrez Alfredo |
| García Navarro Samir |
| Severiano Venegas Donnie |
| Valle Benetts Nara |

---

## 🗂️ Project Structure

```
poverty-unemployment-education/
├── python/                    # Data pipeline, scripts and dashboard
│   ├── DataExtraction/        # Data collection scripts
│   │   └── DataExtraction.py  # Fetches data from INEGI & World Bank APIs
│   ├── MySQL/                 # MySQL insertion scripts
│   │   ├── InsertMySQL.py     # Loads CSV and inserts rows via stored procedures
│   │   └── DataBaseBackup.sql # DB backup used to auto-recreate the schema
│   ├── MongoBD/               # MongoDB export scripts
│   │   └── ExportMongoDB.py   # Mirrors MySQL data into MongoDB collections
│   ├── config.txt             # Connection credentials for MySQL and MongoDB
│   └── gui/                   # Streamlit dashboard
│       ├── welcome_gui.py     # Welcome/landing page
│       ├── run.bat            # Double-click launcher (installs deps + starts dashboard)
│       ├── requirements.txt   # Python dependencies
│       ├── components/        # Reusable UI components
│       │   └── filters.py     # Sidebar year-range filter (global)
│       ├── data/              # Data loading helpers
│       │   └── loader.py      # Cached CSV loader
│       └── pages/             # Dashboard pages (auto-detected by Streamlit)
│           ├── 1_📈_Tendencias.py       # Global trends page
│           ├── 2_💼_Empleo_Economia.py  # Employment & economy page
│           ├── 3_🎓_Educacion_Gasto.py  # Education & social spending page
│           └── 4_⚙️_Control.py          # Control panel (pipeline, data, config, views)
└── database/                  # All database-related files
    ├── EER_Diagram.mwb        # Entity-Relationship diagram (MySQL Workbench)
    ├── DataBaseStructure.sql  # DB creation, tables, and permissions
    ├── Triggers.sql           # Audit triggers for all main tables
    ├── StoredProcedures.sql   # Stored procedures for CRUD and reporting
    ├── Views.sql              # Views for analysis and dashboards
    └── ViewsProcedures.sql    # Stored procedures that wrap each view
```

---

## 🛠️ Technologies Used

| Layer | Technology |
|-------|-----------|
| Dashboard | Python, Streamlit |
| Data Pipeline | Python |
| Relational DB | MySQL, MySQL Workbench |
| NoSQL | MongoDB |

---

## 🗄️ Database

### Schema Overview

The `pobreza` database stores annual socioeconomic indicators across four tables:

```
period
  └── education_indicator
  └── economy_indicator
  └── employment_indicator

audit_log  (populated automatically by triggers)
```

**`period`** — base table; each row represents a year.

**`education_indicator`** — average years of schooling, literacy rate, education spending.

**`economy_indicator`** — Gini index, per capita income, inflation, GDP per worker, poverty rate, health spending.

**`employment_indicator`** — employed/unemployed/total population, labor activity rate, unemployment rate.

**`audit_log`** — automatically records every INSERT, UPDATE, and DELETE across all main tables.

### Running the Scripts

Execute the SQL files **in this order**:

```
1. DataBaseStructure.sql    # Creates the database and all tables
2. Triggers.sql             # Adds audit triggers
3. StoredProcedures.sql     # Registers stored procedures
4. Views.sql                # Creates analytical views
5. ViewsProcedures.sql      # Registers stored procedures for each view
```

---

## ⚙️ Stored Procedures

| Procedure | Description |
|-----------|-------------|
| `sp_insert_full_period` | Inserts a complete year record across all indicator tables |
| `sp_insert_period` | Inserts a single year into the period table |
| `sp_insert_education` | Inserts education indicators for a given period |
| `sp_insert_economy` | Inserts economy indicators for a given period |
| `sp_insert_employment` | Inserts employment indicators for a given period |
| `sp_get_indicators_by_year` | Returns all indicators for a specific year |
| `sp_compare_periods` | Compares key indicators between two years |
| `sp_get_audit_summary` | Returns filtered audit log entries |
| `sp_get_all_periods` | Lists all registered periods |
| `sp_get_all_education` | Returns all education indicator records |
| `sp_get_all_economy` | Returns all economy indicator records |
| `sp_get_all_employment` | Returns all employment indicator records |
| `sp_get_full_indicators` | Queries the full indicators view |
| `sp_get_education_vs_unemployment` | Queries the education vs unemployment view |
| `sp_get_unemployment_vs_economy` | Queries the unemployment vs economy view |
| `sp_get_poverty_trend` | Queries the poverty trend view |
| `sp_get_audit_activity` | Queries the audit activity view |
| `sp_get_indicator_averages` | Queries the indicator averages view |
| `sp_get_year_over_year` | Queries the year over year view |
| `sp_get_spending_vs_outcomes` | Queries the spending vs outcomes view |
| `sp_get_population_distribution` | Queries the population distribution view |

---

## 🔁 Triggers

Audit triggers automatically log every operation to the `audit_log` table. Covered tables and operations:

| Table | INSERT | UPDATE | DELETE |
|-------|--------|--------|--------|
| `period` | ✅ | ✅ | ✅ |
| `education_indicator` | ✅ | ✅ | ✅ |
| `economy_indicator` | ✅ | ✅ | ✅ |
| `employment_indicator` | ✅ | ✅ | ✅ |

Each log entry captures the date, the MySQL user, the affected table, and the operation type.

---

## 👁️ Views

Each view is accessed exclusively through its stored procedure (defined in `ViewsProcedures.sql`), never by direct query, to avoid exposing internal schema details.

| View | Stored Procedure | Description |
|------|-----------------|-------------|
| `v_full_indicators` | `sp_get_full_indicators` | All indicators joined by year |
| `v_education_vs_unemployment` | `sp_get_education_vs_unemployment` | Education metrics vs unemployment |
| `v_unemployment_vs_economy` | `sp_get_unemployment_vs_economy` | Unemployment rates vs economic indicators |
| `v_poverty_trend` | `sp_get_poverty_trend` | Poverty rate evolution over time |
| `v_audit_activity` | `sp_get_audit_activity` | Full audit log ordered by date |
| `v_indicator_averages` | `sp_get_indicator_averages` | Historical averages for all key metrics |
| `v_year_over_year` | `sp_get_year_over_year` | Year-by-year comparison of main indicators |
| `v_spending_vs_outcomes` | `sp_get_spending_vs_outcomes` | Education/health spending vs social outcomes |
| `v_population_distribution` | `sp_get_population_distribution` | Employed, unemployed, and total population per year |

---

## 🔄 Data Pipeline

The pipeline is split into three sequential scripts, all triggered from the Control Panel in the dashboard.

### 1. `DataExtraction/DataExtraction.py`

Fetches socioeconomic indicators for Mexico from two public APIs:

| Source | Indicators |
|--------|-----------|
| **INEGI** | Employed population, unemployed population |
| **World Bank** | Gini index, per capita income (PPP), literacy rate, years of schooling, total population, unemployment rate, GDP per worker, inflation, labor activity rate, health spending, education spending, poverty rate |

Pipeline steps:
1. Calls INEGI and World Bank APIs
2. Merges both sources into a single long-format DataFrame
3. Pivots to wide format (one row per year)
4. Filters to the **2005–2025** range
5. Interpolates missing values linearly (forward and backward)
6. Exports the result to `df_pobreza.csv` in the same directory

### 2. `MySQL/InsertMySQL.py`

Reads `df_pobreza.csv` and inserts each row into MySQL using stored procedures. The `mysql` CLI executable is detected automatically — it checks the system PATH first, then falls back to common Windows installation directories (MySQL 5.7, 8.0, 8.4, XAMPP, WAMP). If the database does not exist, it is recreated automatically from `DataBaseBackup.sql`.

Insertion order per row (single atomic transaction):
1. `sp_insert_period` → returns `id_period`
2. `sp_insert_education` → uses `id_period`
3. `sp_insert_economy` → uses `id_period`
4. `sp_insert_employment` → uses `id_period`

Each row is committed independently. On failure, only that row is rolled back and the error is logged.

### 3. `MongoBD/ExportMongoDB.py`

Reads all data from MySQL via stored procedures and inserts it into four MongoDB collections. The target MongoDB database is **dropped and recreated** on every run to ensure a clean migration.

| Stored Procedure | MongoDB Collection |
|------------------|--------------------|
| `sp_get_all_periods` | `period` |
| `sp_get_all_education` | `education_indicator` |
| `sp_get_all_economy` | `economy_indicator` |
| `sp_get_all_employment` | `employment_indicator` |

---

## 📊 Dashboard (Streamlit)

The `gui/` folder contains an interactive **Streamlit** dashboard that is the main interface of the system — it handles visualization, pipeline execution, database querying, and configuration.

### Setup & Run

Double-click `run.bat` inside `python/gui/` to install dependencies and start the dashboard automatically, or run manually:

```bash
cd python/gui
pip install -r requirements.txt
streamlit run welcome_gui.py
```

The dashboard opens automatically at `http://localhost:8501`.

### `requirements.txt`

All dependencies are listed in `requirements.txt` inside `python/gui/`. Running `run.bat` installs them automatically. To install manually:

```bash
pip install -r requirements.txt
```

| Library | Used for |
|---------|---------|
| `streamlit` | Dashboard UI |
| `plotly` | Interactive charts |
| `statsmodels` | OLS regression trendlines |
| `pandas` | Data loading and processing |
| `requests` | API calls (INEGI & World Bank) |
| `mysql-connector-python` | MySQL connection from dashboard |
| `pymysql` | MySQL connection from pipeline scripts |
| `pymongo` | MongoDB connection |

### Pages

| File | Description |
|------|-------------|
| `welcome_gui.py` | Landing page with project overview, metrics, and navigation cards |
| `pages/1_📈_Tendencias.py` | Global trends: poverty, unemployment, Gini index, per capita income — filterable by indicator and chart type |
| `pages/2_💼_Empleo_Economia.py` | Employment & economy: population, GDP per worker, labor activity, scatter regressions |
| `pages/3_🎓_Educacion_Gasto.py` | Education & social spending: schooling, literacy, education/health spending vs outcomes |
| `pages/4_⚙️_Control.py` | Control panel: pipeline execution, data viewer, connection settings, views query |

### Control Panel (`4_⚙️_Control.py`)

The control panel replaces the React frontend and FastAPI backend entirely. It connects directly to MySQL and MongoDB and provides four tabs:

**⚙️ Config** — read and update `config.txt` credentials for MySQL and MongoDB directly from the UI.

**⚔️ Pipeline** — run each pipeline script (Extraction, MySQL, MongoDB) with real-time output streaming.

**📊 Data** — query MySQL tables or MongoDB collections, displayed automatically in expandable sections by category.

**👁️ Views** — query any of the 9 MySQL views via their stored procedures, with CSV download.

### Shared components

| File | Description |
|------|-------------|
| `components/filters.py` | Global sidebar year-range slider shared across all pages via `st.session_state` |
| `data/loader.py` | `@st.cache_data` loader that reads `df_pobreza.csv` |

---

## ⚠️ IMPORTANT

### config.txt

Create `config.txt` in `python/` with the following keys:

```
host=localhost
user=your_mysql_user
password=your_password
database=pobreza
mongo_host=localhost
mongo_port=27017
mongo_user=
mongo_password=
mongo_database=pobreza
```

All pipeline scripts and the dashboard read from this file automatically.

### Execution Order

1. Execute SQL files in MySQL Workbench: `DataBaseStructure.sql` → `Triggers.sql` → `StoredProcedures.sql` → `Views.sql` → `ViewsProcedures.sql`
2. Configure `config.txt` with your credentials
3. Double-click `run.bat` inside `python/gui/` — it will install all dependencies automatically and launch the dashboard
4. Use the **Control Panel → Pipeline** tab to run: Extraction → MySQL → MongoDB

---

## 📄 License

Academic use only — Final Project, Universidad Autónoma de Baja California (UABC).
