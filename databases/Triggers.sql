use pobreza;

delimiter $$

-- period --
create trigger insert_aud_period
after insert on period for each row
begin
    insert into audit_log (log_date, log_user, log_table, operation)
    values (now(), user(), 'period', 'insert');
end$$

create trigger update_aud_period
before update on period for each row
begin
    insert into audit_log (log_date, log_user, log_table, operation)
    values (now(), user(), 'period', 'update');
end$$

create trigger delete_aud_period
after delete on period for each row
begin
    insert into audit_log (log_date, log_user, log_table, operation)
    values (now(), user(), 'period', 'delete');
end$$

-- education_indicator --
create trigger insert_aud_education_indicator
after insert on education_indicator for each row
begin
    insert into audit_log (log_date, log_user, log_table, operation)
    values (now(), user(), 'education_indicator', 'insert');
end$$

create trigger update_aud_education_indicator
before update on education_indicator for each row
begin
    insert into audit_log (log_date, log_user, log_table, operation)
    values (now(), user(), 'education_indicator', 'update');
end$$

create trigger delete_aud_education_indicator
after delete on education_indicator for each row
begin
    insert into audit_log (log_date, log_user, log_table, operation)
    values (now(), user(), 'education_indicator', 'delete');
end$$


-- economy_indicator --
create trigger insert_aud_economy_indicator
after insert on economy_indicator for each row
begin
    insert into audit_log (log_date, log_user, log_table, operation)
    values (now(), user(), 'economy_indicator', 'insert');
end$$

create trigger update_aud_economy_indicator
before update on economy_indicator for each row
begin
    insert into audit_log (log_date, log_user, log_table, operation)
    values (now(), user(), 'economy_indicator', 'update');
end$$

create trigger delete_aud_economy_indicator
after delete on economy_indicator for each row
begin
    insert into audit_log (log_date, log_user, log_table, operation)
    values (now(), user(), 'economy_indicator', 'delete');
end$$

-- employment_indicator --
create trigger insert_aud_employment_indicator
after insert on employment_indicator for each row
begin
    insert into audit_log (log_date, log_user, log_table, operation)
    values (now(), user(), 'employment_indicator', 'insert');
end$$

create trigger update_aud_employment_indicator
before update on employment_indicator for each row
begin
    insert into audit_log (log_date, log_user, log_table, operation)
    values (now(), user(), 'employment_indicator', 'update');
end$$

create trigger delete_aud_employment_indicator
after delete on employment_indicator for each row
begin
    insert into audit_log (log_date, log_user, log_table, operation)
    values (now(), user(), 'employment_indicator', 'delete');
end$$

delimiter ;

-- View the function of each trigger via CRUD
show triggers from pobreza;

-- view database movements 
select * from audit_log;