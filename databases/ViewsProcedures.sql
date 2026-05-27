use pobreza;
delimiter $$

-- 1. Full indicators
create procedure sp_get_full_indicators()
begin
    select * from v_full_indicators order by year_;
end$$

-- 2. Education vs unemployment
create procedure sp_get_education_vs_unemployment()
begin
    select * from v_education_vs_unemployment order by year_;
end$$

-- 3. Unemployment vs economy
create procedure sp_get_unemployment_vs_economy()
begin
    select * from v_unemployment_vs_economy order by year_;
end$$

-- 4. Poverty trend
create procedure sp_get_poverty_trend()
begin
    select * from v_poverty_trend order by year_;
end$$

-- 5. Audit activity
create procedure sp_get_audit_activity()
begin
    select * from v_audit_activity;
end$$

-- 6. Indicator averages
create procedure sp_get_indicator_averages()
begin
    select * from v_indicator_averages;
end$$

-- 7. Year over year
create procedure sp_get_year_over_year()
begin
    select * from v_year_over_year order by year_;
end$$

-- 8. Spending vs outcomes
create procedure sp_get_spending_vs_outcomes()
begin
    select * from v_spending_vs_outcomes order by year_;
end$$

-- 9. Population distribution
create procedure sp_get_population_distribution()
begin
    select * from v_population_distribution order by year_;
end$$

delimiter ;
