-- PNR history trigger
drop function f_pnr_history CASCADE;
create or replace function f_pnr_history()
returns trigger
as
$body$
declare
	old_pnr_id integer;
	old_agent_id integer;
	old_agent_code character varying(100);
	old_agent_username character varying(100);
	old_agency_code character varying(100);
	old_agency_code_name character varying(100);
	old_currency_code character varying(5);
	old_currency_code_name character varying(100);
	old_state integer;
	old_number character varying(100);
	old_gds_creation_date timestamp with time zone;
	old_system_creation_date timestamp with time zone;
	old_status character varying(100);
	old_status_value integer;
	old_exportdate timestamp with time zone;
	old_type character varying(100);
	old_validationstatus integer;
	old_dateexport timestamp with time zone;
	old_changedate date;
	old_lasttransactiondate date;
	old_otherinformations character varying(200)[];
	old_ssr hstore;
	old_openingstatus boolean;
	old_is_splitted boolean;
	old_is_duplicated boolean;
	old_is_parent boolean;
	old_is_child boolean;
	old_is_read boolean;
	old_parent_pnr character varying(10)[];
	old_children_pnr character varying(10)[];
begin
	select
		id, number, gds_creation_date, exportdate, type,
		validationstatus, dateexport, changedate, lasttransactiondate,
		currency_code, agent_id, state, status, agency_code, otherinformations,
		ssr, openingstatus, is_child, is_parent, is_duplicated, is_splitted, 
		status_value, system_creation_date, is_read, agent_code, 
		parent_pnr, children_pnr
		into 
		old_pnr_id, old_number, old_gds_creation_date, old_exportdate, old_type,
		old_validationstatus, old_dateexport, old_changedate, old_lasttransactiondate,
		old_currency_code, old_agent_id, old_state, old_status, old_agency_code, old_otherinformations,
		old_ssr, old_openingstatus, old_is_child, old_is_parent, old_is_duplicated, old_is_splitted, 
		old_status_value, old_system_creation_date, old_is_read, old_agent_code,
		old_parent_pnr, old_children_pnr
	from
		t_pnr
	where
		id = new.id;
	
	select 
		coalesce(t_user.username, Null) into old_agent_username
	from
		t_user, t_pnr
	where
		t_user.id = t_pnr.agent_id
		and
	 	t_pnr.id = new.id;
	 
	select
		coalesce(t_office.code, Null) into old_agency_code_name
	from
		t_office, t_pnr
	where
		t_office.code = t_pnr.agency_code
		and
		t_pnr.id = new.id;
	
	select
		coalesce(t_currency.code, Null) into  old_currency_code_name
	from
		t_currency, t_pnr
	where
		t_currency.code = t_pnr.currency_code
		and
		t_pnr.id = new.id;
	
	insert into t_pnr_history
		(pnr_id, agent_id, agent_code, agent_username, agency_code
		,agency_code_name, currency_code, currency_code_name, state, number, gds_creation_date, 
		system_creation_date, status, status_value, exportdate, type, validationstatus, dateexport, 
		changedate, lasttransactiondate, otherinformations, ssr, openingstatus, is_splitted, is_duplicated, 
		is_parent, is_child, is_read, parent_pnr, children_pnr, history_datetime)
	values
		(old_pnr_id, old_agent_id, old_agent_code, old_agent_username, old_agency_code, 
		old_agency_code_name, old_currency_code, old_currency_code_name, old_state, old_number, old_gds_creation_date, 
		old_system_creation_date, old_status, old_status_value, old_exportdate, old_type, old_validationstatus, old_dateexport, 
		old_changedate, old_lasttransactiondate, old_otherinformations, old_ssr, old_openingstatus, old_is_splitted, old_is_duplicated, 
		old_is_parent, old_is_child, old_is_read, old_parent_pnr, old_children_pnr, current_timestamp);
	return new;
end;
$body$
language plpgsql;

create trigger t_pnr_history
	before update on t_pnr
	for each row
	execute procedure f_pnr_history();
	
-- OPC and OPW history trigger
drop function f_opw_opc_history CASCADE;
create or replace function f_opw_opc_history()
returns trigger
as
$body$
declare
	old_segment_id integer;
	old_ssr_id integer;
	old_type character varying(200);
	old_free_flow_text character varying(200);
	old_doc_date timestamp with time zone;
	old_pnr_number character varying(6);
begin
	select
		coalesce(segment_id, Null), coalesce(ssr_id, Null), 
		coalesce(type, Null), coalesce(free_flow_text, Null), coalesce(doc_date, Null)
		into
		old_segment_id, old_ssr_id, old_type, old_free_flow_text, old_doc_date
	from
		t_confirmation_deadline
	where
		id = new.id;
		
	case
		when exists(select segment_id from t_confirmation_deadline where id = new.id) then
			select coalesce(t_pnr.number, Null) into old_pnr_number from t_pnr where id=(select pnr_id from t_pnrairsegments where id=(select segment_id from t_confirmation_deadline where id = new.id));
		when exists(select ssr_id from t_confirmation_deadline where id = new.id) then
			select coalesce(t_pnr.number, Null) into old_pnr_number from t_pnr where id=(select pnr_id from t_ssr_base where id=(select ssr_id from t_confirmation_deadline where id = new.id));
		else
			old_pnr_number := Null;
	end case;
	
	insert into t_confirmation_deadline_history
		(pnr_number, type, free_flow_text, 
		doc_date, history_datetime, segment_id, ssr_id)
		values
		(old_pnr_number, old_type, old_free_flow_text,
		old_doc_date, current_timestamp, old_segment_id, old_ssr_id);
	return new;	
end;
$body$
language plpgsql;

create trigger t_confirmation_deadline_history
	before update or delete on t_confirmation_deadline
	for each row
	execute procedure f_opw_opc_history();
