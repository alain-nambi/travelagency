delete from t_passenger_invoice;
delete from t_pnr_contact;
delete from t_pnr_flight;
delete from t_pnr_passengers;
delete from t_invoice_detail;
delete from t_invoice;
delete from t_histories;
delete from t_comment;
-- delete from t_airsegments;
delete from t_taxes;
delete from t_ticket_passenger_segment;
delete from t_reduce_pnr_fee_request;
delete from t_passenger_invoice;
delete from t_fee;
delete from t_other_fees_segment;
delete from t_other_fee;
delete from t_ssr_passenger;
delete from t_ssr_segment;
delete from t_ticket_ssr;
delete from t_confirmation_deadline;
delete from t_pnrairsegments;
delete from t_ssr_base;
delete from t_pnr_remark;
delete from t_ticket_passenger_tst;
delete from t_raw_data;
delete from t_ticket;
delete from t_customer_address;
delete from t_passengers;
-- delete from t_pnr_history;
delete from t_history;
delete from t_response;
delete from t_pnr;

delete from 
	t_fee 
where 
	ticket_id 
	in (
	select 
		t_ticket.id 
	from 
		t_ticket, t_ticket_ssr, t_ssr_base, t_pnrairsegments, t_ssr_segment 
	where 
		t_ticket.id = t_ticket_ssr.ticket_id
		and
		t_ticket_ssr.ssr_id = t_ssr_base.id
		and
		t_ssr_segment.parent_ssr_id = t_ssr_base.id
		and
		t_ssr_segment.segment_id = t_pnrairsegments.id
		and
		t_ticket.issuing_date::timestamp::date = t_pnrairsegments.departuretime::timestamp::date
	);