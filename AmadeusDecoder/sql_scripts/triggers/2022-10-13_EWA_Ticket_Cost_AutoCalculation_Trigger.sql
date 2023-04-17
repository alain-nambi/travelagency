-- automatically calculate ticket [fare, tax, total] after insert on table t_ticket_passenger_segment (EWA Only)
create or replace function f_auto_update_ticket_cost_ewa() returns trigger as
$body$
declare
	total_fare double precision;
	old_total_fare double precision;
	total_tax double precision;
	old_total_tax double precision;
	total_total double precision;
	old_total_total double precision;
	ticket_id_ integer;
begin
	select ticket_id into ticket_id_ from t_ticket_passenger_segment where id = new.id;
	select coalesce(sum(transport_cost), 0) into old_total_fare from t_ticket where id = ticket_id_;
	select coalesce(sum(tax), 0) into old_total_tax from t_ticket where id = ticket_id_;
	select coalesce(sum(total), 0) into old_total_total from t_ticket where id = ticket_id_;
	
	select coalesce(sum(fare), 0) into total_fare from t_ticket_passenger_segment where id = new.id and ticket_id = ticket_id_;
	select coalesce(sum(tax), 0) into total_tax from t_ticket_passenger_segment where id = new.id and ticket_id = ticket_id_;
	select coalesce(sum(total), 0) into total_total from t_ticket_passenger_segment where id = new.id and ticket_id = ticket_id_;
	
	update t_ticket set transport_cost = total_fare + old_total_fare, tax = total_tax + old_total_tax, total = total_total + old_total_total where id = ticket_id_;
	return new;
end;
$body$
language plpgsql;

create trigger t_auto_update_ticket_cost_ewa
	after insert or update on t_ticket_passenger_segment
	for each row
	execute procedure f_auto_update_ticket_cost_ewa();