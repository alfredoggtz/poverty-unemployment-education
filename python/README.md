# README – Python Project #

## 📋 Description

This module of the project aims to extract, process, and analyze data related to poverty, education, and unemployment using Python.

Within this section, the following tools are implemented:
- Web scraping
- API Consumption
- Data Processing
- MySQL Connection
- Data Migration
- Data Preparation for Visualization

The main purpose is to collect reliable information that allows the analysis of the relationship between education level, economy, and poverty rates.

## 🛠️ Technologies/Libraries Used
- Python (PyCharm)
- Requests
- Pandas
- MySQL Connector
- Public APIs

## 📌 Main Features
- Data extraction through web scraping.
- API consumption related to poverty and education.
- Data cleaning and transformation.
- Connection to MySQL database.
- Database data insertion.
- Data preparation for dashboards and analysis.

## 📊 Analysis Objective

Analyze the relationship between:

- Poverty
- Education level
- Economy
- Unemployment

With the purpose of identifying patterns and generating useful information for decision-making.

# ⚙️ Program Functionality ⚙️
## 📂 Extraccion de datos.py

This Python program builds a socioeconomic indicators dataset for Mexico using information obtained from the APIs of the National Institute of Statistics and Geography (INEGI) and the World Bank.

The script downloads data related to:

- Employed and unemployed population
- Gini Index
- Per capita income
- Literacy rate
- Expected years of schooling

After collecting the information, the program organizes all data into a single DataFrame using pandas, performs data cleaning and transformation processes, fills missing values through linear interpolation, and finally generates a CSV file named:

#df_pobreza.csv#

This file is ready to be used for:
- Data analysis
- Data visualization
- Business Intelligence models

## 📂 conexionBD.py

This Python program is responsible for loading the df_pobreza.csv dataset and storing its information into a MySQL database.

First, the program establishes a connection to the database using mysql.connector. Then, it reads the CSV file with pandas and calculates a new variable called:

#tasa_desempleo#

This variable is obtained from employed and unemployed population data.

Afterward, the program iterates through each row of the DataFrame and inserts the information into different related tables such as:

- period
- education_indicator
- economy_indicator
- employment_indicator

The data is organized by year and by educational, economic, and employment indicators.

Finally, the program saves all changes into the database using commit(), and closes the connection, leaving the information ready for:

- Queries
- Analysis
- Visualization
# ⚠️ IMPORTANT

To connect Python with MySQL, it is necessary to modify the database configuration before running the code.

The following parameters must be changed according to your local MySQL configuration:

- User
- Host
- Database (the database must already exist in MySQL)
- Password

These settings are required in order to connect correctly to the MySQL server and execute the program successfully.

## 👥 Team members
- Galvan Gutierrez Alfredo
- García Navarro Samir
- Severiano Venegas Donnie
- Valle Benetts Nara

# 📄 License

Academic use for the final project – Universidad Autónoma de Baja California (UABC)
