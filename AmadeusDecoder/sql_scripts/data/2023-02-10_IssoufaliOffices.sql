-- delete from t_office;
DO $$
DECLARE
	company character varying := 'Issoufali';
	companyID integer;
BEGIN
select id into companyID from t_company_info where  company_name=company;
-- insert into t_office (name, location, code, company_id) values
-- ('Office 1', 'Society', 'DZAUU0006', companyID),
-- ('Office 2', 'Mamoudzou', 'DZAUU01A3', companyID),
-- ('Office 3', 'Jumbo Score', 'DZAUU01A4', companyID),
-- ('Office 4', 'Dzaoudzi', 'DZAUU01A1', companyID),
-- ('Office 5', 'Airport', 'DZAUU000B', companyID),
-- ('Office 6', 'Agence Mayotte Tourisme Voyages', 'DZAA12114', companyID),
-- ('Office 7', 'Agence Air Mayotte Voyages', 'DZAA12102', companyID),
-- ('Office 8', 'Xanadu Paris', 'PARFT278Z', companyID);

update t_office set company_id=companyID where code in ('DZAUU0006', 'DZAUU01A3', 'DZAUU01A4', 'DZAUU01A1', 'DZAUU000B', 'DZAA12114', 'DZAA12102', 'PARFT278Z');
END $$;
