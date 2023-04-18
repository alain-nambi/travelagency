-- regional countries for Issoufali
DO $$
declare
	company_id_ INTEGER;
begin
	select id into company_id_ from t_company_info where company_name = 'Issoufali';
	insert into t_company_regional_flight(company_id, country_id) values
	(company_id_, (select id from t_countries where code='YT')),
	(company_id_, (select id from t_countries where code='MG')),
	(company_id_, (select id from t_countries where code='RE'));
end $$;