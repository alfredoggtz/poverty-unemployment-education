"""
4_⚙️_Control.py
-----------------
Control panel page for the Streamlit dashboard.
Connects directly to MySQL and MongoDB without needing FastAPI or React.
    - Pipeline: run data extraction, MySQL insertion, and MongoDB export scripts
    - Data: query MySQL tables and MongoDB collections
    - Config: read and update config.txt
    - Views: query MySQL views
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import subprocess
import streamlit as st
import pandas as pd
from decimal import Decimal
import mysql.connector
from mysql.connector import Error as MySQLError
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from components.filters import render_filters
from data.loader import load_data


def browse_file():
    """Opens a native file dialog and returns the selected path."""
    try:
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk()
        root.withdraw()
        root.wm_attributes('-topmost', True)
        path = filedialog.askopenfilename(
            title="Select mysql.exe",
            filetypes=[("Executable", "*.exe"), ("All files", "*.*")]
        )
        root.destroy()
        return path
    except Exception:
        return None

st.set_page_config(page_title="Control Panel", layout="wide")

BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, '..', '..', 'config.txt')

SCRIPTS = {
    "extraction": os.path.join(BASE_DIR, '..', '..', 'DataExtraction', 'DataExtraction.py'),
    "mysql": os.path.join(BASE_DIR, '..', '..', 'MySQL', 'InsertMySQL.py'),
    "mongodb": os.path.join(BASE_DIR, '..', '..', 'MongoBD', 'ExportMongoDB.py'),
}

VIEWS = {
    '📋 Full Indicators': 'sp_get_full_indicators',
    '🎓 Education vs Unemployment': 'sp_get_education_vs_unemployment',
    '💹 Unemployment vs Economy': 'sp_get_unemployment_vs_economy',
    '📉 Poverty Trend': 'sp_get_poverty_trend',
    '🔍 Audit Activity': 'sp_get_audit_activity',
    '📊 Indicator Averages': 'sp_get_indicator_averages',
    '📅 Year Over Year': 'sp_get_year_over_year',
    '💰 Spending vs Outcomes': 'sp_get_spending_vs_outcomes',
    '👥 Population Distribution': 'sp_get_population_distribution',
}

MYSQL_KEYS = ['host', 'user', 'password', 'database']
MONGO_KEYS = ['mongo_host', 'mongo_port', 'mongo_user', 'mongo_password', 'mongo_database']


def load_config():
    config = {}
    try:
        with open(CONFIG_PATH, 'r') as f:
            for line in f:
                line = line.strip()
                if line and '=' in line:
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip()
    except FileNotFoundError:
        st.error(f"config.txt not found at {CONFIG_PATH}")
    return config


def save_config(data: dict):
    with open(CONFIG_PATH, 'w') as f:
        for key, value in data.items():
            f.write(f"{key}={value}\n")


def get_mysql_connection(cfg):
    return mysql.connector.connect(
        host=cfg['host'],
        user=cfg['user'],
        password=cfg['password'],
        database=cfg['database']
    )


def get_mongo_db(cfg):
    client = MongoClient(
        host=cfg['mongo_host'],
        port=int(cfg['mongo_port']),
        username=cfg.get('mongo_user') or None,
        password=cfg.get('mongo_password') or None
    )
    return client[cfg['mongo_database']]


def convert_decimal(val):
    if isinstance(val, Decimal):
        return float(val)
    return val


def query_by_sp(cfg, sp_name):
    conn   = get_mysql_connection(cfg)
    cursor = conn.cursor()
    cursor.callproc(sp_name)
    rows = []
    for result in cursor.stored_results():
        cols = [c[0] for c in result.description]
        for row in result.fetchall():
            rows.append({c: convert_decimal(v) for c, v in zip(cols, row)})
    cursor.close()
    conn.close()
    return rows


def query_mongo_collection(cfg, collection):
    db = get_mongo_db(cfg)
    return list(db[collection].find({}, {"_id": 0}))


# ── Sidebar & header ──────────────────────────────────────────────────────────
df = load_data()
render_filters(df)

st.markdown("## ⚙️ Control Panel")
st.markdown("---")

tab_config, tab_pipeline, tab_data, tab_views = st.tabs([
    "⚙️ Config", "⚔️ Pipeline", "📊 Data", "👁️ Views"
])

# ── Pipeline ──────────────────────────────────────────────────────────────────
with tab_pipeline:
    st.markdown("### ⚔️ Run Pipeline Scripts")
    st.markdown("Execute each step of the data pipeline in order.")
    st.markdown("---")

    scripts = [
        {"key": "extraction", "label": "🌐 Extraction", "sublabel": "INEGI & World Bank → CSV"},
        {"key": "mysql", "label": "🗄️ MySQL", "sublabel": "CSV → MySQL database"},
        {"key": "mongodb", "label": "🍃 MongoDB", "sublabel": "MySQL → MongoDB export"},
    ]

    cols = st.columns(3, gap="medium")
    for col, script in zip(cols, scripts):
        with col:
            st.markdown(f"**{script['label']}**")
            st.caption(script["sublabel"])
            if st.button("▶ Run", key=f"btn_{script['key']}", use_container_width=True):
                script_path = SCRIPTS[script["key"]]
                if not os.path.exists(script_path):
                    st.error(f"Script not found:\n{script_path}")
                else:
                    placeholder = st.empty()
                    lines = []
                    process = subprocess.Popen(
                        [sys.executable, script_path],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        text=True,
                        encoding="utf-8",
                        errors="replace"
                    )
                    for line in process.stdout:
                        lines.append(line.rstrip())
                        placeholder.code("\n".join(lines), language="bash")
                    process.wait()
                    if process.returncode == 0:
                        st.success("✔ Script finished successfully.")
                    else:
                        st.error(f"❌ Script exited with code {process.returncode}.")

# ── Data ──────────────────────────────────────────────────────────────────────
with tab_data:
    st.markdown("### 📊 Query Data")
    st.markdown("---")

    cfg = load_config()
    data_source = st.radio("Source", ["MySQL", "MongoDB"], horizontal=True)

    TABLE_SP = {
        'Period': 'sp_get_all_periods',
        'Education Indicators': 'sp_get_all_education',
        'Economy Indicators': 'sp_get_all_economy',
        'Employment Indicators': 'sp_get_all_employment',
    }

    MONGO_LABELS = {
        'Period': 'period',
        'Education Indicators': 'education_indicator',
        'Economy Indicators': 'economy_indicator',
        'Employment Indicators': 'employment_indicator',
    }

    if data_source == "MySQL":
        for label, sp in TABLE_SP.items():
            with st.expander(f"📄 {label}", expanded=True):
                try:
                    rows = query_by_sp(cfg, sp)
                    if rows:
                        st.dataframe(pd.DataFrame(rows), use_container_width=True)
                    else:
                        st.warning("No data found.")
                except MySQLError as e:
                    st.error(f"❌ MySQL error: {e}")
                except Exception as e:
                    st.error(f"❌ Error: {e}")
    else:
        for label, collection in MONGO_LABELS.items():
            with st.expander(f"📄 {label}", expanded=True):
                try:
                    docs = query_mongo_collection(cfg, collection)
                    if docs:
                        st.dataframe(pd.DataFrame(docs), use_container_width=True)
                    else:
                        st.warning("No documents found.")
                except PyMongoError as e:
                    st.error(f"❌ MongoDB error: {e}")
                except Exception as e:
                    st.error(f"❌ Error: {e}")

# ── Config ────────────────────────────────────────────────────────────────────
with tab_config:
    st.markdown("### ⚙️ Connection Settings")
    st.markdown("Read and update the `config.txt` file used by all pipeline scripts.")
    st.markdown("---")

    cfg = load_config()
    col_mysql, col_mongo = st.columns(2, gap="large")

    with col_mysql:
        st.markdown("**🗄️ MySQL**")
        for key in MYSQL_KEYS:
            if key == 'database':
                # Database name is read-only — edit config.txt directly to change it.
                st.text_input(
                    key, value=cfg.get(key, ""),
                    disabled=True,
                    key=f"cfg_{key}",
                    help="To change the database name, edit config.txt directly."
                )
            else:
                cfg[key] = st.text_input(
                    key, value=cfg.get(key, ""),
                    type="password" if key == "password" else "default",
                    key=f"cfg_{key}"
                )

    with col_mongo:
        st.markdown("**🍃 MongoDB**")
        for key in MONGO_KEYS:
            if key == 'mongo_database':
                # Database name is read-only — edit config.txt directly to change it.
                st.text_input(
                    key, value=cfg.get(key, ""),
                    disabled=True,
                    key=f"cfg_{key}",
                    help="To change the database name, edit config.txt directly."
                )
            else:
                cfg[key] = st.text_input(
                    key, value=cfg.get(key, ""),
                    type="password" if key == "mongo_password" else "default",
                    key=f"cfg_{key}"
                )

    st.markdown("---")
    if st.button("▶ Save Settings", type="primary"):
        try:
            # Preserve the original database names from config.txt —
            # they are read-only in the UI and must not be overwritten.
            original = load_config()
            cfg['database'] = original.get('database', cfg.get('database', ''))
            cfg['mongo_database'] = original.get('mongo_database', cfg.get('mongo_database', ''))
            save_config(cfg)
            st.success("✔ Settings saved to config.txt.")
        except Exception as e:
            st.error(f"❌ Could not save config: {e}")

# ── Views ─────────────────────────────────────────────────────────────────────
with tab_views:
    st.markdown("### 👁️ MySQL Views")
    st.markdown("Query pre-built views that combine and summarize data from all tables.")
    st.markdown("---")

    cfg = load_config()
    view_label = st.selectbox("Select view", list(VIEWS.keys()))
    view_key   = VIEWS[view_label]

    if st.button("▶ Query View", type="primary"):
        try:
            rows = query_by_sp(cfg, view_key)
            if rows:
                st.success(f"✔ {len(rows)} rows returned.")
                df_view = pd.DataFrame(rows)
                st.dataframe(df_view, use_container_width=True)
                csv = df_view.to_csv(index=False).encode("utf-8")
                st.download_button(
                    "⬇️ Download CSV", data=csv,
                    file_name=f"{view_label.split(' ', 1)[-1].strip().lower().replace(' ', '_')}.csv",
                    mime="text/csv"
                )
            else:
                st.warning("No data found in this view.")
        except MySQLError as e:
            st.error(f"❌ MySQL error: {e}")
        except Exception as e:
            st.error(f"❌ Error: {e}")