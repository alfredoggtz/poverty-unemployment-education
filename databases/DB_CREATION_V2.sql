create database pobreza;
use pobreza;

-- Give user privilegies to connect whit the Python script
grant all privileges on pobreza.* to samir@localhost;

create table period(
id_period int primary key auto_increment,
year_ year
);

create table education_indicator(
id_edu int primary key auto_increment,
id_period int,
average_years_of_schooling decimal,
literacy_rate decimal,
foreign key (id_period) references period(id_period)
);

create table economy_indicator(
id_eco int primary key auto_increment,
id_period int,
gini_index decimal,
per_capita_income decimal,
foreign key (id_period) references period(id_period)
);

create table employment_indicator(
id_emp int primary key auto_increment,
id_period int, 
employed_population bigint, 
unemployed_population bigint,
unemployment_rate decimal,
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
