-- new issoufali office
insert into t_office (name, code, company_id) values
('Office DZAAF0103', 'DZAAF0103', (select id from t_company_info where company_name='Issoufali'));