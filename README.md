# 📊 Poverty, Unemployment & Education Analysis
> Final Project – Universidad Autónoma de Baja California (UABC)

A full-stack data analysis system that collects, stores, and visualizes socioeconomic indicators for Mexico related to poverty, education, and unemployment. The project integrates a Python data pipeline, a MySQL relational database, a React frontend, and a MongoDB NoSQL layer.

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
├── python/                    # Data collection, DB connection scripts and frontend
│   ├── frontend/              # React + Vite web application
│   │   ├── src/
│   │   ├── public/
│   │   ├── package.json
│   │   └── vite.config.js
│   ├── backend/               # FastAPI backend (REST API + SSE pipeline)
│   │   ├── main.py            # API entry point
│   │   └── requirements.txt   # Python dependencies
│   ├── DataExtraction/        # Data collection scripts
│   │   └── DataExtraction.py  # Fetches data from INEGI & World Bank APIs
│   ├── MySQL/                 # MySQL insertion scripts
│   │   ├── InsertMySQL.py     # Loads CSV and inserts rows via stored procedures
│   │   └── DataBaseBackup.sql # DB backup used to auto-recreate the schema
│   ├── MongoBD/               # MongoDB export scripts
│   │   └── ExportMongoDB.py   # Mirrors MySQL data into MongoDB collections
│   └── gui/                   # Streamlit dashboard
│       ├── welcome_gui.py     # Welcome/landing page
│       ├── components/        # Reusable UI components
│       │   └── filters.py     # Sidebar year-range filter
│       ├── data/              # Data loading helpers
│       │   └── loader.py      # Cached CSV loader
│       └── pages/             # Dashboard pages (auto-detected by Streamlit)
│           ├── 1_📈_Tendencias.py       # Global trends page
│           ├── 2_💼_Empleo_Economia.py  # Employment & economy page
│           └── 3_🎓_Educacion_Gasto.py  # Education & social spending page
└── database/                  # All database-related files
    ├── EER_Diagram.mwb        # Entity-Relationship diagram (MySQL Workbench)
    ├── DataBaseStructure.sql  # DB creation, tables, and permissions
    ├── Triggers.sql           # Audit triggers for all main tables
    ├── StoredProcedures.sql   # Stored procedures for CRUD and reporting
    └── Views.sql              # Views for analysis and dashboards
```

---

## 🛠️ Technologies Used

| Layer | Technology |
|-------|-----------|
| Frontend | React, Vite |
| Dashboard | Python, Streamlit |
| Backend / API | Python, FastAPI, Uvicorn |
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

```bash
1. DataBaseStructure.sql    # Creates the database and all tables
2. Triggers.sql             # Adds audit triggers
3. StoredProcedures.sql     # Registers stored procedures
4. Views.sql                # Creates analytical views
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

| View | Description |
|------|-------------|
| `v_full_indicators` | All indicators joined by year |
| `v_education_vs_unemployment` | Education metrics cross-referenced with unemployment |
| `v_unemployment_vs_economy` | Unemployment rates vs economic indicators |
| `v_poverty_trend` | Poverty rate evolution over time |
| `v_audit_activity` | Full audit log ordered by date |
| `v_indicator_averages` | Historical averages for all key metrics |
| `v_year_over_year` | Year-by-year comparison of main indicators |
| `v_spending_vs_outcomes` | Education/health spending vs social outcomes |
| `v_population_distribution` | Employed, unemployed, and total population per year |

---

## 🔄 Data Pipeline

The pipeline is split into three sequential scripts, each triggered via the backend API:

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

Reads `df_pobreza.csv` and inserts each row into MySQL using individual stored procedures per table. If the `pobreza` database does not exist, it is automatically recreated from `DataBaseBackup.sql` before inserting.

Insertion order per row (single atomic transaction):
1. `sp_insert_period` → returns `id_period`
2. `sp_insert_education` → uses `id_period`
3. `sp_insert_economy` → uses `id_period`
4. `sp_insert_employment` → uses `id_period`

Each row is committed independently. On failure, only that row is rolled back and the error is logged, allowing the remaining rows to continue.

> ⚠️ Requires `mysql_path` in `config.txt` pointing to the `mysql` CLI executable (e.g. `C:/Program Files/MySQL/MySQL Server 8.0/bin/mysql.exe`).

### 3. `MongoBD/ExportMongoDB.py`

Reads all data from MySQL via stored procedures and inserts it into four MongoDB collections, mirroring the relational structure:

| Stored Procedure | MongoDB Collection |
|------------------|--------------------|
| `sp_get_all_periods` | `period` |
| `sp_get_all_education` | `education_indicator` |
| `sp_get_all_economy` | `economy_indicator` |
| `sp_get_all_employment` | `employment_indicator` |

Each collection is cleared before insertion to prevent duplicates on re-runs.

---

## 🚀 Backend (FastAPI)

The backend is a **FastAPI** application that acts as the bridge between the React frontend, the Python pipeline scripts, MySQL, and MongoDB.

### Setup & Run

```bash
cd python/backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`. Interactive docs at `http://localhost:8000/docs`.

### Endpoints

**Pipeline execution** — streams real-time output via Server-Sent Events (SSE):

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/run/extraction` | Runs the data extraction script |
| `POST` | `/run/mysql` | Runs the MySQL insertion script |
| `POST` | `/run/mongodb` | Runs the MongoDB export script |

**Configuration:**

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/config` | Read current `config.txt` |
| `PUT` | `/config` | Update `config.txt` |

**MySQL data:**

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/data/mysql/{table}` | Query a table via its stored procedure |
| `GET` | `/views` | List available views |
| `GET` | `/views/{view_name}` | Query a MySQL view |

Valid `{table}` values: `period`, `education_indicator`, `economy_indicator`, `employment_indicator`.

**MongoDB data:**

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/data/mongodb/{collection}` | Query a MongoDB collection |

### config.txt

The backend reads connection credentials from a `config.txt` file located one level above `backend/`. Expected keys:

```
host=localhost
user=your_mysql_user
password=your_password
database=pobreza
mysql_path=C:/Program Files/MySQL/MySQL Server 8.0/bin/mysql.exe
mongo_host=localhost
mongo_port=27017
mongo_user=
mongo_password=
mongo_database=pobreza
```

---

## 📊 Dashboard (Streamlit)

The `gui/` folder contains an interactive **Streamlit** dashboard that serves as the visualization layer of the system — the space where raw indicators become readable charts, comparable across years and variables.

### Structure

| File | Description |
|------|-------------|
| `welcome_gui.py` | Landing page with project overview and objectives |
| `components/filters.py` | Sidebar slider that filters all pages by year range |
| `data/loader.py` | Cached `@st.cache_data` loader that reads `df_pobreza.csv` |
| `pages/1_📈_Tendencias.py` | Global trends: poverty rate, unemployment, Gini index, per capita income — line/area charts + normalized comparison |
| `pages/2_💼_Empleo_Economia.py` | Employment & economy: employed vs unemployed population, GDP per worker, labor activity rate, inflation vs unemployment scatter, Gini vs income regression |
| `pages/3_🎓_Educacion_Gasto.py` | Education & social spending: years of schooling, literacy rate, education/health spending vs PIB, scatter regressions vs poverty and unemployment |

All pages share the same sidebar filter (`filters.py`) and data source (`loader.py`), which reads directly from `DataExtraction/df_pobreza.csv`.

### Setup & Run

```bash
cd python/gui
pip install streamlit plotly statsmodels
streamlit run welcome_gui.py
```

The dashboard will open automatically at `http://localhost:8501`. Streamlit auto-detects the `pages/` folder and adds each page to the sidebar navigation.

---

## 🌐 Frontend

The web interface is built with **React + Vite**.

### Setup & Run

```bash
cd python/frontend
npm install
npm run dev
```

The app will be available at `http://localhost:5173` by default.

---

## 📄 License

Academic use only — Final Project, Universidad Autónoma de Baja California (UABC).
