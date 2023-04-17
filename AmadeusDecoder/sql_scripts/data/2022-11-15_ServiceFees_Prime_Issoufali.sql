-- Service fees on Prime Ticket for Issoufali
-- type: 0 = regional, 1 = international, metropole
-- Udpate 1
delete from t_service_fees_prime;
insert into t_service_fees_prime (type, fee_value, company_id) values
(0, 30, (select id from t_company_info where company_name = 'Issoufali')),
(1, 40, (select id from t_company_info where company_name = 'Issoufali'));
-- Update 2
delete from t_service_fees_prime;
insert into t_service_fees_prime (type, fee_value, company_id) values
(0, 35, (select id from t_company_info where company_name = 'Issoufali')),
(1, 45, (select id from t_company_info where company_name = 'Issoufali'));
-- Update 3
delete from t_service_fees_prime;
insert into t_service_fees_prime (type, fee_value, company_id) values
(0, 40, (select id from t_company_info where company_name = 'Issoufali')),
(1, 40, (select id from t_company_info where company_name = 'Issoufali'));