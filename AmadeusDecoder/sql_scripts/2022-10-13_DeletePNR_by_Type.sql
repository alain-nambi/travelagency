DO $$
DECLARE
	pnr_type_ character varying := 'Zenith';
BEGIN
	delete from t_pnr_contact where pnr_id in (select id from t_pnr where type=pnr_type_);
	delete from t_pnr_passengers where pnr_id in (select id from t_pnr where type=pnr_type_);
	delete from t_invoice_detail where invoice_id in (select id from t_invoice where pnr_id in (select id from t_pnr where type=pnr_type_));
	delete from t_invoice where pnr_id in (select id from t_pnr where type=pnr_type_);
	delete from t_histories;
	delete from t_taxes;
	delete from t_ticket_passenger_segment where ticket_id in (select id from t_ticket where pnr_id in (select id from t_pnr where type=pnr_type_));
	delete from t_fee where pnr_id in (select id from t_pnr where type=pnr_type_);
	delete from t_ssr_passenger where parent_ssr_id in (select id from t_ssr_base where pnr_id in (select id from t_pnr where type=pnr_type_));
	delete from t_ssr_segment where parent_ssr_id in (select id from t_ssr_base where pnr_id in (select id from t_pnr where type=pnr_type_));
	delete from t_ticket_ssr where ticket_id in (select id from t_ticket where pnr_id in (select id from t_pnr where type=pnr_type_));
	delete from t_confirmation_deadline where segment_id in (select id from t_pnrairsegments where pnr_id in (select id from t_pnr where type=pnr_type_));
	delete from t_pnrairsegments where pnr_id in (select id from t_pnr where type=pnr_type_);
	delete from t_ssr_base where pnr_id in (select id from t_pnr where type=pnr_type_);
	delete from t_pnr_remark where pnr_id in (select id from t_pnr where type=pnr_type_);
	delete from t_ticket where pnr_id in (select id from t_pnr where type=pnr_type_);
	-- delete from t_passengers;
	delete from t_pnr where type=pnr_type_;
END $$;

DO $$
DECLARE
	pnr_id_ integer := 5376;
BEGIN
	delete from t_passenger_invoice where pnr_id = pnr_id_;
	delete from t_fee where ticket_id in (select id from t_ticket where pnr_id = pnr_id_);
	delete from "t_ticket_passenger_segment" where ticket_id in (select id from t_ticket where pnr_id = pnr_id_);
	delete from "t_ticket_passenger_tst" where ticket_id in (select id from t_ticket where pnr_id = pnr_id_);
	delete from t_ticket_ssr where ticket_id in (select id from t_ticket where pnr_id = pnr_id_);
	delete from t_ticket where pnr_id = pnr_id_;
	
	delete from t_ssr_segment where segment_id in (select id from t_pnrairsegments where pnr_id = pnr_id_);
	delete from t_confirmation_deadline where segment_id in (select id from t_pnrairsegments where pnr_id = pnr_id_);
	delete from t_pnrairsegments where pnr_id = pnr_id_;
END $$;

DO $$
DECLARE
	ticket_id_ integer := 895;
BEGIN
	delete from t_ticket_passenger_segment where ticket_id = ticket_id_;
	delete from t_ticket_passenger_tst where ticket_id = ticket_id_;
	delete from t_fee where ticket_id = ticket_id_;
	delete from t_ticket where id = ticket_id_;
END $$;