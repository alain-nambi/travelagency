-- Stored procedure for creating log after each modification on fees

-- fetch ticket number or other fee designation
create or replace function f_get_ticket_or_other_fee(fee_id integer)
returns character varying(100)
as 
$body$
declare
	ticket_id integer;
	other_fee_id integer;
	return_val character varying(100);
begin
	select t_fee.other_fee_id into other_fee_id from t_fee where  t_fee.id = fee_id;
	select t_fee.ticket_id into ticket_id from t_fee where t_fee.id = fee_id;
	case
		when other_fee_id is not null then
			select t_other_fee.designation into return_val from t_other_fee where t_other_fee.id = other_fee_id;
		when ticket_id is not null then
			select t_ticket.number into return_val from t_ticket where t_ticket.id = ticket_id;
		else
			return null;
	end case;
	return return_val;
end;
$body$
language plpgsql;

-- create fee history
create or replace function f_create_fee_history(pnrId integer, user_id integer, fee_id integer, initial_cost double precision, new_cost double precision, initial_total double precision)
returns void
as 
$body$
declare
	curtime timestamp := now();
	pnr_number character varying(10);
	target_object character varying(100);
	user_name character varying(100);
	modif_type character varying(100) := 'Fee';
	current_total double precision;
begin
	select number into pnr_number from t_pnr where id=pnrId;
	select username into user_name from t_user where id=user_id;
	select f_get_ticket_or_other_fee(fee_id) into target_object;
	select 
		t_invoice_detail.total into current_total 
	from 
		t_invoice_detail, t_invoice, t_pnr
	where
		t_invoice_detail.invoice_id = t_invoice.id
		and
		t_invoice.pnr_id = pnrId;
	-- save history
	insert into t_history (pnr_id, pnr_number, user_id, username, modification_type, modification, modification_date) values
	(
		pnrId,
		pnr_number,
		user_id,
		user_name,
		modif_type,
		hstore(array['initial_cost', 'new_cost', 'target_object', 'initial_total', 'new_total'], array[initial_cost::text, new_cost::text, target_object::text, initial_total::text, current_total::text]),
		curtime
	);
end;
$body$
language plpgsql;