use pobreza;
delimiter $$
-- 1. full period insert
create procedure sp_insert_full_period(
    in p_year year,
    in p_avg_schooling decimal(5,2),
    in p_literacy_rate decimal(5,2),
    in p_gini_index decimal(5,4),
    in p_per_capita_income decimal(12,2),
    in p_employed bigint,
    in p_unemployed bigint,
    in p_unemployment_rate decimal(5,2)
)
begin
    declare v_id_period int;
    insert into period (year_) values (p_year);
    set v_id_period = last_insert_id();
    insert into education_indicator
        (id_period, average_years_of_schooling, literacy_rate)
    values (v_id_period, p_avg_schooling, p_literacy_rate);
    insert into economy_indicator
        (id_period, gini_index, per_capita_income)
    values (v_id_period, p_gini_index, p_per_capita_income);
    insert into employment_indicator
        (id_period, employed_population, unemployed_population, unemployment_rate)
    values (v_id_period, p_employed, p_unemployed, p_unemployment_rate);
    select v_id_period as created_period_id;
end$$
-- 2. get indicators by year
create procedure sp_get_indicators_by_year(
    in p_year year
)
begin
    select
        p.year_,
        e.average_years_of_schooling,
        e.literacy_rate,
        ec.gini_index,
        ec.per_capita_income,
        emp.employed_population,
        emp.unemployed_population,
        emp.unemployment_rate
    from period p
    join education_indicator e on e.id_period = p.id_period
    join economy_indicator ec on ec.id_period = p.id_period
    join employment_indicator emp on emp.id_period = p.id_period
    where p.year_ = p_year;
end$$
-- 3. compare two periods
create procedure sp_compare_periods(
    in p_year_a year,
    in p_year_b year
)
begin
    select
        p.year_,
        ec.gini_index,
        ec.per_capita_income,
        ed.literacy_rate,
        emp.unemployment_rate
    from period p
    join economy_indicator ec on ec.id_period = p.id_period
    join education_indicator ed on ed.id_period = p.id_period
    join employment_indicator emp on emp.id_period = p.id_period
    where p.year_ in (p_year_a, p_year_b)
    order by p.year_;
end$$
-- 4. audit log summary
create procedure sp_get_audit_summary(
    in p_table varchar(255),
    in p_operation varchar(10),
    in p_limit int
)
begin
    select
        id_audit,
        log_date,
        log_user,
        log_table,
        operation
    from audit_log
    where
        (p_table is null or log_table = p_table)
        and (p_operation is null or operation = p_operation)
    order by log_date desc
    limit p_limit;
end$$
-- 5. list periods
create procedure sp_list_periods()
begin
    select id_period, year_
    from period
    order by year_;
end$$
delimiter ;