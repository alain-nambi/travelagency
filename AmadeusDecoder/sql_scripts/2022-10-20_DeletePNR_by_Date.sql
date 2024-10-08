DO $$
DECLARE
	day INTEGER := 19;
	month INTEGER := 10;
	year INTEGER := 2022;
BEGIN
	delete from t_pnr_contact where pnr_id in (select id from t_pnr where extract(DAY from system_creation_date) = day and extract(MONTH from system_creation_date) = month);
	delete from t_pnr_passengers where pnr_id in (select id from t_pnr where extract(DAY from system_creation_date) = day and extract(MONTH from system_creation_date) = month);
	-- delete from t_invoice_detail where invoice_id in (select id from t_invoice where pnr_id in (select id from t_pnr where extract(DAY from system_creation_date) = day and extract(MONTH from system_creation_date) = month));
	-- delete from t_invoice where pnr_id in (select id from t_pnr where extract(DAY from system_creation_date) = day and extract(MONTH from system_creation_date) = month);
	delete from t_histories;
	delete from t_taxes;
	delete from t_ticket_passenger_segment where ticket_id in (select id from t_ticket where pnr_id in (select id from t_pnr where extract(DAY from system_creation_date) = day and extract(MONTH from system_creation_date) = month));
	delete from t_fee where pnr_id in (select id from t_pnr where extract(DAY from system_creation_date) = day and extract(MONTH from system_creation_date) = month);
	delete from t_ssr_passenger where parent_ssr_id in (select id from t_ssr_base where pnr_id in (select id from t_pnr where extract(DAY from system_creation_date) = day and extract(MONTH from system_creation_date) = month));
	delete from t_ssr_segment where parent_ssr_id in (select id from t_ssr_base where pnr_id in (select id from t_pnr where extract(DAY from system_creation_date) = day and extract(MONTH from system_creation_date) = month));
	delete from t_ticket_ssr where ticket_id in (select id from t_ticket where pnr_id in (select id from t_pnr where extract(DAY from system_creation_date) = day and extract(MONTH from system_creation_date) = month));
	delete from t_confirmation_deadline where segment_id in (select id from t_pnrairsegments where pnr_id in (select id from t_pnr where extract(DAY from system_creation_date) = day and extract(MONTH from system_creation_date) = month));
	delete from t_pnrairsegments where pnr_id in (select id from t_pnr where extract(DAY from system_creation_date) = day and extract(MONTH from system_creation_date) = month);
	delete from t_ssr_base where pnr_id in (select id from t_pnr where extract(DAY from system_creation_date) = day and extract(MONTH from system_creation_date) = month);
	delete from t_pnr_remark where pnr_id in (select id from t_pnr where extract(DAY from system_creation_date) = day and extract(MONTH from system_creation_date) = month);
	delete from t_ticket where pnr_id in (select id from t_pnr where extract(DAY from system_creation_date) = day and extract(MONTH from system_creation_date) = month);
	-- delete from t_passengers;
	-- delete from t_pnr where id=pnr_id_;
END $$;

insert into t_invoice (select id from t_pnr where id not in (select pnr_id from t_invoice));
