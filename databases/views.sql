use pobreza;
-- 1 full indicators
create view v_full_indicators as
select
    p.year_,
    e.average_years_of_schooling,
    e.literacy_rate,
    e.education_spend,
    ec.gini_index,
    ec.per_capita_income,
    ec.inflation,
    ec.gdp_per_worker,
    ec.poverty_rate,
    ec.health_spending_pct,
    emp.employed_population,
    emp.unemployed_population,
    emp.total_population,
    emp.labor_activity_rate,
    emp.unemployment_rate
from period p
join education_indicator e on e.id_period = p.id_period
join economy_indicator ec on ec.id_period = p.id_period
join employment_indicator emp on emp.id_period = p.id_period;
-- 2 education vs unemployment
create view v_education_vs_unemployment as
select
    p.year_,
    e.average_years_of_schooling,
    e.literacy_rate,
    e.education_spend,
    emp.unemployment_rate,
    emp.employed_population,
    emp.unemployed_population
from period p
join education_indicator e on e.id_period = p.id_period
join employment_indicator emp on emp.id_period = p.id_period;
-- 3 unemployment vs economy
create view v_unemployment_vs_economy as
select
    p.year_,
    emp.unemployment_rate,
    emp.labor_activity_rate,
    ec.gini_index,
    ec.per_capita_income,
    ec.poverty_rate,
    ec.inflation,
    ec.gdp_per_worker
from period p
join employment_indicator emp on emp.id_period = p.id_period
join economy_indicator ec on ec.id_period = p.id_period;
-- 4 poverty trend
create view v_poverty_trend as
select
    p.year_,
    ec.poverty_rate,
    ec.gini_index,
    ec.per_capita_income,
    e.literacy_rate,
    emp.unemployment_rate
from period p
join economy_indicator ec on ec.id_period = p.id_period
join education_indicator e on e.id_period = p.id_period
join employment_indicator emp on emp.id_period = p.id_period;
-- 5 audit activity
create view v_audit_activity as
select
    log_date,
    log_user,
    log_table,
    operation
from audit_log
order by log_date desc;
-- 6 indicator averages
create view v_indicator_averages as
select
    avg(e.literacy_rate) as avg_literacy_rate,
    avg(e.average_years_of_schooling) as avg_schooling_years,
    avg(e.education_spend) as avg_education_spend,
    avg(ec.gini_index) as avg_gini_index,
    avg(ec.per_capita_income) as avg_per_capita_income,
    avg(ec.poverty_rate) as avg_poverty_rate,
    avg(ec.inflation) as avg_inflation,
    avg(emp.unemployment_rate) as avg_unemployment_rate,
    avg(emp.labor_activity_rate) as avg_labor_activity_rate
from period p
join education_indicator e on e.id_period = p.id_period
join economy_indicator ec on ec.id_period = p.id_period
join employment_indicator emp on emp.id_period = p.id_period;
-- 7 year over year
create view v_year_over_year as
select
    p.year_,
    emp.unemployment_rate,
    ec.poverty_rate,
    ec.gini_index,
    e.literacy_rate,
    ec.per_capita_income
from period p
join employment_indicator emp on emp.id_period = p.id_period
join economy_indicator ec on ec.id_period = p.id_period
join education_indicator e on e.id_period = p.id_period;
-- 8 spending vs outcomes
create view v_spending_vs_outcomes as
select
    p.year_,
    e.education_spend,
    ec.health_spending_pct,
    e.literacy_rate,
    e.average_years_of_schooling,
    emp.unemployment_rate,
    ec.poverty_rate
from period p
join education_indicator e on e.id_period = p.id_period
join economy_indicator ec on ec.id_period = p.id_period
join employment_indicator emp on emp.id_period = p.id_period;
-- 9 population distribution
create view v_population_distribution as
select
    p.year_,
    emp.total_population,
    emp.employed_population,
    emp.unemployed_population
from period p
join employment_indicator emp on emp.id_period = p.id_period;


-- selects
select * from v_full_indicators order by year_;
select * from v_education_vs_unemployment order by year_;
select * from v_unemployment_vs_economy order by year_;
select * from v_poverty_trend order by year_;
select * from v_audit_activity;
select * from v_indicator_averages;
select * from v_year_over_year order by year_;
select * from v_spending_vs_outcomes order by year_;
select * from v_population_distribution order by year_;