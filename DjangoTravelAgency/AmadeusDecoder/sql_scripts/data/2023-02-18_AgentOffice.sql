-- assign office to agents
DO $$
DECLARE
	officeID integer;
BEGIN
select id into officeID from t_office where  code='DZAUU000B';

update t_user set office_id = officeID where email = 'sity@agences-issoufali.com';
update t_user set office_id = officeID where email = 'fouadi@agences-issoufali.com';
update t_user set office_id = officeID where email = 'roihamina@agences-issoufali.com';
update t_user set office_id = officeID where email = 'riziki@agences-issoufali.com';

END $$;