-- Service Fees on EMD
-- Update 1
delete from t_service_fees_emd;
insert into t_service_fees_emd (fee_value, company_id) values
(5, (select id from t_company_info where company_name = 'Issoufali'));
-- Update 2
delete from t_service_fees_emd;
insert into t_service_fees_emd (fee_value, company_id) values
(10, (select id from t_company_info where company_name = 'Issoufali'));