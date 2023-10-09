-- auto create service fees on Flight after ticket insertion or update
drop function if exists f_service_fees_issoufali  cascade;
create or replace function f_service_fees_issoufali()
returns trigger
as
$body$
declare
	pnr_id_ integer;
	pnr_type_ character varying(100);
	passenger_type_ character varying(100);
	ticket_type_ character varying(100);
	ticket_passenger_type_ character varying(10);
	ticket_gp_status_ boolean;
	ticket_is_regional_status_ boolean;
	ticket_is_prime_status_ boolean;
	ticket_status_ integer;
	ticket_fare double precision;
	fee_value double precision;
	is_saved boolean;
	ticket_is_adc boolean;
	ticket_is_subjected_to_fees boolean;
	is_updated boolean;
	current_fee double precision;
	old_fee double precision;
begin
	select t_ticket.transport_cost into ticket_fare from t_ticket where t_ticket.id = new.id;
	select t_ticket.pnr_id into pnr_id_ from t_ticket where t_ticket.id = new.id;
	select t_pnr.type into pnr_type_ from t_pnr where t_pnr.id = pnr_id_;
	select t_passengers.types into passenger_type_ from t_passengers where id = (select passenger_id from t_ticket where id = new.id);
	select t_ticket.ticket_type into ticket_type_ from t_ticket where t_ticket.id = new.id;
	select t_ticket.is_gp into ticket_gp_status_ from t_ticket where t_ticket.id = new.id;
	select t_ticket.is_regional into ticket_is_regional_status_ from t_ticket where t_ticket.id = new.id;
	select t_ticket.is_prime into ticket_is_prime_status_ from t_ticket where t_ticket.id = new.id;
	select t_ticket.ticket_status into ticket_status_ from t_ticket where t_ticket.id = new.id;
	select t_ticket.passenger_type into ticket_passenger_type_ from t_ticket where t_ticket.id = new.id;
	select t_ticket.is_no_adc, t_ticket.is_subjected_to_fees into ticket_is_adc, ticket_is_subjected_to_fees from t_ticket where t_ticket.id = new.id;
	select coalesce(t_fee.total, 0), coalesce(t_fee.newest_cost, 0) into current_fee, old_fee from t_fee where ticket_id=new.id;
	case
		when ticket_is_prime_status_ then
			case
				-- ticket is regional
				when ticket_is_regional_status_ then
					select t_service_fees_prime.fee_value into fee_value from t_service_fees_prime where t_service_fees_prime.type = 0 and t_service_fees_prime.company_id = (select id from t_company_info where t_company_info.company_name='Issoufali');
				else
					select t_service_fees_prime.fee_value into fee_value from t_service_fees_prime where t_service_fees_prime.type = 1 and t_service_fees_prime.company_id = (select id from t_company_info where t_company_info.company_name='Issoufali');
			end case;
		else
			case
				when ticket_type_ = 'EMD' then
					select t_service_fees_emd.fee_value into fee_value from t_service_fees_emd where t_service_fees_emd.company_id = (select id from t_company_info where t_company_info.company_name='Issoufali');
				when ticket_passenger_type_ = 'INF' and passenger_type_ = 'INF_ASSOC' then
					fee_value := 35;
				when pnr_type_ = 'EWA' and passenger_type_ = 'Bébé(s)' then
					fee_value := 15;
				else
					select t_servicefees_amount_based.fee into fee_value from t_servicefees_amount_based where ticket_fare >= t_servicefees_amount_based.min_interval and ( case when t_servicefees_amount_based.max_interval = 0 then 9999999999 else t_servicefees_amount_based.max_interval end ) >= floor(ticket_fare);
			end case;
	end case;
	case
		when exists(select 1 from t_fee where t_fee.ticket_id=new.id and t_fee.pnr_id=pnr_id_ and t_fee.type = 'FRAIS DE SERVICE') then
			is_saved := true;
		else
			is_saved := false;
	end case;
	case
		when exists(select 1 from t_reduce_pnr_fee_request where fee_id in (select id from t_fee where ticket_id=new.id) and status = 1) or current_fee > fee_value or current_fee < fee_value or old_fee > current_fee or old_fee < current_fee then
			is_updated := true;
	else
		is_updated := false;
	end case;
	case
		-- when ticket_type_  = 'TKT' or ticket_type_ = 'TST' then 
		when (ticket_type_  = 'TKT' or ticket_type_ = 'TST' or ticket_type_ = 'EMD') and ticket_is_subjected_to_fees then 
			case 
				-- when ticket arrived from pnr
				-- when (ticket_fare > 0 or ticket_is_prime_status_ or ticket_type_ = 'EMD')  and not is_saved and ticket_gp_status_ not like 'SA' then
				when (ticket_fare > 0 or ticket_is_prime_status_ or ticket_is_adc) and not is_saved and not ticket_gp_status_ then
					insert into t_fee(pnr_id, ticket_id, type, designation, cost, tax, total, newest_cost, old_cost, is_invoiced) values (pnr_id_, new.id, 'FRAIS DE SERVICE', ' ', fee_value, 0, fee_value, fee_value, fee_value, false);
				-- gp
				when (ticket_fare > 0 or ticket_is_prime_status_ or ticket_is_adc) and not is_saved and ticket_gp_status_ then
					insert into t_fee(pnr_id, ticket_id, type, designation, cost, tax, total, newest_cost, old_cost, is_invoiced) values (pnr_id_, new.id, 'FRAIS DE SERVICE', ' ', 0, 0, 0, 0, 0, false);
				-- when is_saved and (ticket_gp_status_ like 'SA' or ticket_status_ = 0) then
				-- when is_saved and (ticket_gp_status_ like 'SA' or ticket_status_ = 0 or ticket_status_ = 3) then
					-- delete from t_passenger_invoice where fee_id = (select id from t_fee where pnr_id=pnr_id_ and ticket_id=new.id and type='FRAIS DE SERVICE');
					-- delete from t_fee where pnr_id=pnr_id_ and ticket_id=new.id and type='FRAIS DE SERVICE';
				when is_saved and fee_value is not null and not is_updated then
				-- when is_saved and fee_value is not null then
					update t_fee set cost=fee_value, total=fee_value, tax=0, newest_cost=fee_value, old_cost=fee_value where pnr_id=pnr_id_ and ticket_id=new.id and type='FRAIS DE SERVICE';
				else
					return new;
			end case;
		when (ticket_type_  = 'TKT' or ticket_type_ = 'TST' or ticket_type_ = 'EMD') and not ticket_is_subjected_to_fees then 
			case 
				when (ticket_fare > 0 or ticket_is_prime_status_ or ticket_is_adc) and not is_saved and not ticket_gp_status_ then
					insert into t_fee(pnr_id, ticket_id, type, designation, cost, tax, total, newest_cost, old_cost, is_invoiced) values (pnr_id_, new.id, 'FRAIS DE SERVICE', ' ', 0, 0, 0, 0, 0, false);
				else
					return new;
			end case;
		else 
			return new;
	end case;
	return new;
end;
$body$
language plpgsql;

drop trigger if exists t_auto_create_sf on t_ticket;
create trigger t_auto_create_sf
	after insert or update of transport_cost on t_ticket
	for each row
	execute procedure f_service_fees_issoufali();
	
-- auto create service fees on Flight after EMD other fees insertion or update
drop function if exists f_service_fees_emd_ewa_issoufali  cascade;
create or replace function f_service_fees_emd_ewa_issoufali()
returns trigger
as
$body$
declare
 	other_fee_type character varying(100);
 	fee_value double precision;
	pnr_id_ integer;
	other_fee_cost double precision;
	is_fee_saved boolean;
	-- Be careful
	is_updated boolean;
	current_fee double precision;
	old_fee double precision;
	is_subjected_to_fees boolean;
begin
	select t_other_fee.pnr_id, t_other_fee.cost, t_other_fee.fee_type, t_other_fee.is_subjected_to_fee into pnr_id_, other_fee_cost, other_fee_type, is_subjected_to_fees from t_other_fee where id = new.id;
	select coalesce(t_fee.total, 0), coalesce(t_fee.newest_cost, 0) into current_fee, old_fee from t_fee where other_fee_id=new.id;
	-- check if fee has been already saved
	case
		when exists(select 1 from t_fee where t_fee.other_fee_id=new.id and t_fee.pnr_id=pnr_id_ and t_fee.type = 'FRAIS DE SERVICE') then
			is_fee_saved := true;
		else
			is_fee_saved := false;
	end case;
	-- get fee
	case
		when other_fee_type = 'EMD' or other_fee_type = 'Supplement' then
			select t_service_fees_emd.fee_value into fee_value from t_service_fees_emd where t_service_fees_emd.company_id = (select id from t_company_info where t_company_info.company_name='Issoufali'); 
		when other_fee_type = 'TKT' then
			select t_servicefees_amount_based.fee into fee_value from t_servicefees_amount_based where other_fee_cost >= t_servicefees_amount_based.min_interval and ( case when t_servicefees_amount_based.max_interval = 0 then 9999999999 else t_servicefees_amount_based.max_interval end ) >= other_fee_cost;
		else
			return new;
	end case;
	-- check is updated status
	case
		when exists(select 1 from t_reduce_pnr_fee_request where fee_id in (select id from t_fee where other_fee_id=new.id) and status = 1) or current_fee > fee_value or current_fee < fee_value or old_fee > current_fee or old_fee < current_fee then
			is_updated := true;
		else
			is_updated := false;
	end case;
	-- create or update fee
	case
		-- subjected to fee
		when not is_fee_saved and (other_fee_type = 'EMD' or other_fee_type = 'TKT' or other_fee_type = 'Supplement') and is_subjected_to_fees then
			insert into t_fee(pnr_id, other_fee_id, type, designation, cost, tax, total, newest_cost, old_cost, is_invoiced) values (pnr_id_, new.id, 'FRAIS DE SERVICE', ' ', fee_value, 0, fee_value, fee_value, fee_value, false);
		-- not subjected to fee
		when not is_fee_saved and (other_fee_type = 'EMD' or other_fee_type = 'TKT' or other_fee_type = 'Supplement') and not is_subjected_to_fees then
			insert into t_fee(pnr_id, other_fee_id, type, designation, cost, tax, total, newest_cost, old_cost, is_invoiced) values (pnr_id_, new.id, 'FRAIS DE SERVICE', ' ', 0, 0, 0, 0, 0, false);
		-- update
		when is_fee_saved and (other_fee_type = 'EMD' or other_fee_type = 'TKT' or other_fee_type = 'Supplement') and not is_updated then
		-- when is_fee_saved and (other_fee_type = 'EMD' or other_fee_type = 'TKT' or other_fee_type = 'Supplement') then
			update t_fee set cost=fee_value, total=fee_value, tax=0, newest_cost=fee_value, old_cost=fee_value where pnr_id=pnr_id_ and other_fee_id=new.id and type='FRAIS DE SERVICE';
		else
			return new;
	end case;
	return new;
end;
$body$
language plpgsql;

drop trigger if exists t_auto_create_sf_on_other_fees on t_other_fee;
create trigger t_auto_create_sf_on_other_fees
	after insert or update of cost on t_other_fee
	for each row
	execute procedure f_service_fees_emd_ewa_issoufali();