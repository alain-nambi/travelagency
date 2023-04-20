DO $$
DECLARE
	pnr_id_ INTEGER := 234;
BEGIN
	delete from t_pnr_contact where pnr_id = (select id from t_pnr where id=pnr_id_);
	delete from t_pnr_flight;
	delete from t_pnr_passengers where pnr_id = (select id from t_pnr where id=pnr_id_);
	delete from t_invoice_detail where invoice_id = (select id from t_invoice where pnr_id=pnr_id_);
	delete from t_invoice where pnr_id=pnr_id_;
	delete from t_histories;
	delete from t_taxes;
	delete from t_ticket_passenger_segment where ticket_id=(select id from t_ticket where pnr_id=pnr_id_);
	delete from t_fee;
	delete from t_ssr_passenger where parent_ssr_id = (select id from t_ssr_base where pnr_id=pnr_id_);
	delete from t_ssr_segment where parent_ssr_id = (select id from t_ssr_base where pnr_id=pnr_id_);
	delete from t_ticket_ssr where ticket_id=(select id from t_ticket where pnr_id=pnr_id_);
	delete from t_confirmation_deadline where segment_id=(select id from t_pnrairsegments where pnr_id=pnr_id_);
	delete from t_pnrairsegments where pnr_id=pnr_id_;
	delete from t_ssr_base where pnr_id=pnr_id_;
	delete from t_pnr_remark where pnr_id=pnr_id_;
	delete from t_ticket where pnr_id=pnr_id_;
	-- delete from t_passengers;
	delete from t_pnr where id=pnr_id_;
END $$;