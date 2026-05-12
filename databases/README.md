# README – MySQL Database
## 📋 Description

This module contains the development and administration of the MySQL database used in the poverty, education, and unemployment analysis project.

The database aims to store, organize, and manage all information collected through Python
Additionally, the following are implemented:

- Create database
- Triggers
- Stored Procedures
- Views
- SQL Queries
- MongoDB Integration

## 🛠️ Technologies Used
- MySQL
- MySQL Workbench
- MongoDB

## 📌 Main Features
- Storage of collected data.
- Management of poverty and education-related information.
- Automation through triggers.
- Protection and optimization through stored procedures.
- Report generation using views.
- Data preparation for dashboards.
- Data migration and cloning to MongoDB.

## 📊 Database Objective
Centralize all project information to facilitate:

- Queries
- Reports
- Data visualization
- Data integrity
- System scalability}

## 🔄 MongoDB Integration

The database includes a migration process to MongoDB in order to implement a complementary NoSQL solution for flexible data management.

# ⚙️ Script Functionality ⚙️
## 📂 EER_Diagram.mwb

This file contains the Entity-Relationship Diagram (EER) of the poverty project database.

The diagram was created to visually represent the database structure and facilitate the analysis of relationships between the tables implemented within the system.

Additionally, it helps to understand:

- The main entities of the project
- Relationships between tables
- Primary and foreign keys
- The organization of information within the database

The file was developed using MySQL Workbench.

## 📂 POBREZA_DB_CREATION.sql

This SQL script creates and configures a database called:

#pobreza#

The database is designed to store socioeconomic indicators of Mexico related to poverty, education, economy, and employment.

First, the script creates the database and configures permissions for the MySQL user.
(It is important to adapt the user configuration according to the computer where the project will be executed).

Afterward, the following tables are created:

- period
- education_indicator
- economy_indicator
- employment_indicator

These tables store information related to:

- Time periods
- Educational indicators
- Economic indicators
- Employment indicators

The structure uses:

- Primary keys
- Foreign keys

in order to correctly maintain relationships between data.

Additionally, an extra table called:

#audit_log#

is created to store audit records and operations performed within the database.

Finally, the script includes SELECT queries to visualize table contents and verify that the data has been stored correctly.

## 📂 triggers_pobreza.sql

This SQL file contains the implementation of MySQL triggers used to automatically register operations performed within the database into the following table:

#audit_log%

The triggers monitor actions such as:

- Insertions (INSERT)
- Updates (UPDATE)
- Deletions (DELETE)

performed on the main system tables.

The stored information includes:

- Operation date
- User who performed the change
- Affected table
- Executed operation type

The main purpose is to implement an auditing and control mechanism that facilitates:

- Change tracking
- Data integrity supervision
- Security maintenance within the information system

## 📂 procedures.sql

This SQL file contains the implementation of Stored Procedures in MySQL to automate processes and queries within the database.

Stored procedures allow operations to be executed securely and efficiently, avoiding direct repetitive queries from external applications.

Their main purpose is to:

- Optimize queries
- Improve performance
- Centralize business logic
- Protect database integrity

Additionally, they facilitate the manipulation and administration of information related to educational, economic, and employment indicators.

## 📂 views.sql

This SQL file contains the creation of MySQL views to facilitate the querying and visualization of relevant information within the project.

Views allow combining information from multiple tables and simplifying complex queries related to:

- Education
- Economy
- Employment
- Poverty

Their main purpose is to:

- Facilitate report generation
- Improve query organization
- Optimize data analysis
- Prepare information for dashboards and visualizations

Views function as virtual tables that display processed information without modifying the original data stored in the database.

## ⚡ Execute the scripts

Run the SQL files in the following order:

- pobreza_db_creation.sql
- triggers.sql
- procedures.sql
- views.sql

## 👥 Team members
- Galvan Gutierrez Alfredo
- García Navarro Samir
- Severiano Venegas Donnie
- Valle Benetts Nara

# 📄 License

Academic use for the final project – Universidad Autónoma de Baja California (UABC)








