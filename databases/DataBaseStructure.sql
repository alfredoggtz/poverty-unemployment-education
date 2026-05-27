create database pobreza;
use pobreza;

-- Give user privilegies to connect with the Python script
grant all privileges on pobreza.* to samir@localhost;

create table period(
id_period int primary key auto_increment,
year_ year
);

create table education_indicator(
id_edu int primary key auto_increment,
id_period int,
average_years_of_schooling decimal(5, 2),
literacy_rate decimal(5, 2),
education_spend decimal(10, 4),
foreign key (id_period) references period(id_period)
);

create table economy_indicator(
id_eco int primary key auto_increment,
id_period int,
gini_index decimal(5, 2),
per_capita_income decimal(12, 2),
inflation decimal(7, 4),
gdp_per_worker decimal(14, 2),
poverty_rate decimal(5, 2),
health_spending_pct decimal(5, 4),
foreign key (id_period) references period(id_period)
);

create table employment_indicator(
id_emp int primary key auto_increment,
id_period int, 
employed_population bigint, 
unemployed_population bigint,
total_population bigint,
labor_activity_rate decimal(5, 2),
unemployment_rate decimal(5, 2),
foreign key (id_period) references period(id_period)
);

-- Audit table creation
create table audit_log (
id_audit int primary key auto_increment,
log_date datetime,
log_user varchar(255),
log_table varchar(255),
operation varchar(10)
);

select * from economy_indicator;
select * from education_indicator;
select * from period;
select * from employment_indicator;
