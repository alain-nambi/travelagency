-- drop all if exist
drop function if exists update_total_ht  cascade;
drop function if exists update_total_ht_1  cascade;
drop function if exists update_total_ht_2  cascade;

--auto update total ht after update or insert t_ticket
create or replace function update_total_ht() returns trigger as
$body$
declare
	ticket_status_ integer;
	sum_totalticket double precision;
	sum_totalticket_ht double precision;
	sum_fees double precision;
	sum_ticket_tax  double precision;
	pnrid integer;
	invoiceid integer;
	total_ht double precision;
	sum_other_fees double precision;
	sum_other_fees_fee double precision;
	all_service_fees double precision;
begin
	select t_ticket.pnr_id into pnrid from t_ticket where id = new.id;
	select t_ticket.ticket_status into ticket_status_ from t_ticket where id = new.id;
	select coalesce(sum(transport_cost), 0) into sum_totalticket_ht from t_ticket where t_ticket.pnr_id = pnrid and t_ticket.ticket_status = 1 and (t_ticket.state=0 or t_ticket.state=1);
	select coalesce(sum(total), 0) into sum_totalticket from t_ticket where t_ticket.pnr_id = pnrid and t_ticket.ticket_status = 1 and (t_ticket.state=0 or t_ticket.state=1);
	select coalesce(sum(tax), 0) into sum_ticket_tax from t_ticket where t_ticket.pnr_id = pnrid and t_ticket.ticket_status = 1 and (t_ticket.state=0 or t_ticket.state=1);
	select coalesce(sum(total), 0) into sum_fees from t_fee where t_fee.pnr_id = pnrid and ticket_id in (select id from t_ticket where ticket_status = 1  and (t_ticket.state=0 or t_ticket.state=1) and pnr_id = pnrid);
	select id into invoiceid from t_invoice where t_invoice.pnr_id = pnrid;
	select coalesce(sum(total), 0) into sum_other_fees from t_other_fee where pnr_id=pnrid and other_fee_status=1;
	select coalesce(sum(t_fee.total), 0) into sum_other_fees_fee from t_fee where t_fee.pnr_id = pnrid and other_fee_id in (select id from t_other_fee where pnr_id = pnrid and other_fee_status=1);
	
	all_service_fees := sum_fees + sum_other_fees_fee;
	total_ht = sum_totalticket + all_service_fees + sum_other_fees;
	update t_invoice_detail set totalht = sum_totalticket_ht, total = coalesce(total_ht, 0) + coalesce(tva_sce, 0), total_fees = coalesce(all_service_fees, 0), total_tax = sum_ticket_tax where t_invoice_detail.invoice_id = invoiceid;
	return new;
end;
$body$
language plpgsql;

create trigger t_update_total_ht
	after insert or update or delete on t_ticket
	for each row
	execute procedure update_total_ht();

--auto update total ht after update or insert t_fee
create or replace function update_total_ht_1() returns trigger as
$body$
declare
	sum_totalticket double precision;
	sum_totalticket_ht double precision;
	sum_fees double precision;
	sum_ticket_tax  double precision;
	pnr_id_ integer;
	invoice_id_ integer;
	total_ht double precision;
	sum_other_fees double precision;
	sum_other_fees_fee double precision;
	all_service_fees double precision;
begin
	IF (TG_OP = 'DELETE') THEN
		select t_fee.pnr_id into pnr_id_ from t_fee where id = old.id;
		select coalesce(sum(t_ticket.transport_cost), 0) into sum_totalticket_ht from t_ticket where t_ticket.pnr_id = pnr_id_ and t_ticket.ticket_status = 1 and (t_ticket.state=0 or t_ticket.state=1);
		select coalesce(sum(t_ticket.total), 0) into sum_totalticket from t_ticket where t_ticket.pnr_id = pnr_id_ and t_ticket.ticket_status = 1  and (t_ticket.state=0 or t_ticket.state=1);
		select coalesce(sum(tax), 0) into sum_ticket_tax from t_ticket where t_ticket.pnr_id = pnr_id_ and t_ticket.ticket_status = 1  and (t_ticket.state=0 or t_ticket.state=1);
		select coalesce(sum(t_fee.total), 0) into sum_fees from t_fee where t_fee.pnr_id = pnr_id_ and ticket_id in (select id from t_ticket where ticket_status = 1 and (t_ticket.state=0 or t_ticket.state=1) and pnr_id = pnr_id_);
		select t_invoice.id into invoice_id_ from t_invoice where t_invoice.pnr_id = pnr_id_;
		select coalesce(sum(total), 0) into sum_other_fees from t_other_fee where pnr_id = pnr_id_ and other_fee_status=1;
		select coalesce(sum(t_fee.total), 0) into sum_other_fees_fee from t_fee where t_fee.pnr_id = pnr_id_ and other_fee_id in (select id from t_other_fee where pnr_id = pnr_id_ and other_fee_status=1);
		
		all_service_fees := sum_fees + sum_other_fees_fee;
		total_ht = sum_totalticket + all_service_fees + sum_other_fees;
		update t_invoice_detail set totalht = sum_totalticket_ht, total = total_ht + tva_sce, total_fees = all_service_fees, total_tax = sum_ticket_tax where invoice_id = invoice_id_;
		return old;
	ELSE
		select t_fee.pnr_id into pnr_id_ from t_fee where id = new.id;
		select coalesce(sum(t_ticket.transport_cost), 0) into sum_totalticket_ht from t_ticket where t_ticket.pnr_id = pnr_id_ and t_ticket.ticket_status = 1;
		select coalesce(sum(t_ticket.total), 0) into sum_totalticket from t_ticket where t_ticket.pnr_id = pnr_id_ and t_ticket.ticket_status = 1;
		select coalesce(sum(tax), 0) into sum_ticket_tax from t_ticket where t_ticket.pnr_id = pnr_id_ and t_ticket.ticket_status = 1;
		select coalesce(sum(t_fee.total), 0) into sum_fees from t_fee where t_fee.pnr_id = pnr_id_ and ticket_id in (select id from t_ticket where ticket_status = 1 and pnr_id = pnr_id_);
		select t_invoice.id into invoice_id_ from t_invoice where t_invoice.pnr_id = pnr_id_;
		select coalesce(sum(total), 0) into sum_other_fees from t_other_fee where pnr_id = pnr_id_ and other_fee_status=1;
		select coalesce(sum(t_fee.total), 0) into sum_other_fees_fee from t_fee where t_fee.pnr_id = pnr_id_ and other_fee_id in (select id from t_other_fee where pnr_id = pnr_id_ and other_fee_status=1);
		
		all_service_fees := sum_fees + sum_other_fees_fee;
		total_ht = sum_totalticket + all_service_fees + sum_other_fees;
		update t_invoice_detail set totalht = sum_totalticket_ht, total = total_ht + tva_sce, total_fees = all_service_fees, total_tax = sum_ticket_tax where invoice_id = invoice_id_;
		return new;
	END IF;
end;
$body$
language plpgsql;

create trigger t_update_total_ht_1
	after insert or update or delete on t_fee
	for each row
	execute procedure update_total_ht_1();

-- auto update total after insert on t_other_fee
create or replace function update_total_ht_2() returns trigger as
$body$
declare
	sum_totalticket double precision;
	sum_totalticket_ht double precision;
	sum_fees double precision;
	sum_other_fees double precision;
	sum_ticket_tax  double precision;
	pnr_id_ integer;
	invoice_id_ integer;
	total_ht double precision;
	sum_other_fees_fee double precision;
	all_service_fees double precision;
begin
	select t_other_fee.pnr_id into pnr_id_ from t_other_fee where t_other_fee.id = new.id;
	select coalesce(sum(t_ticket.transport_cost), 0) into sum_totalticket_ht from t_ticket where t_ticket.pnr_id = pnr_id_ and t_ticket.ticket_status = 1 and (t_ticket.state=0 or t_ticket.state=1);
	select coalesce(sum(t_ticket.total), 0) into sum_totalticket from t_ticket where t_ticket.pnr_id = pnr_id_ and t_ticket.ticket_status = 1 and (t_ticket.state=0 or t_ticket.state=1);
	select coalesce(sum(tax), 0) into sum_ticket_tax from t_ticket where t_ticket.pnr_id = pnr_id_ and t_ticket.ticket_status = 1 and (t_ticket.state=0 or t_ticket.state=1);
	select coalesce(sum(t_other_fee.total), 0) into sum_other_fees from t_other_fee where t_other_fee.pnr_id = pnr_id_;
	select coalesce(sum(t_fee.total), 0) into sum_fees from t_fee where t_fee.pnr_id = pnr_id_ and ticket_id in (select id from t_ticket where ticket_status = 1 and (t_ticket.state=0 or t_ticket.state=1) and pnr_id = pnr_id_);
	select t_invoice.id into invoice_id_ from t_invoice where t_invoice.pnr_id = pnr_id_;
	select coalesce(sum(total), 0) into sum_other_fees from t_other_fee where pnr_id = pnr_id_ and other_fee_status=1;
	select coalesce(sum(t_fee.total), 0) into sum_other_fees_fee from t_fee where t_fee.pnr_id = pnr_id_ and other_fee_id in (select id from t_other_fee where pnr_id = pnr_id_ and other_fee_status=1);
	
	all_service_fees := sum_fees + sum_other_fees_fee;
	total_ht = sum_totalticket + sum_other_fees + all_service_fees;
	update t_invoice_detail set totalht = sum_totalticket_ht, total = total_ht + tva_sce, total_fees = all_service_fees, total_tax = sum_ticket_tax where invoice_id = invoice_id_;
	return new;
end;
$body$
language plpgsql;

create trigger t_update_total_ht_2
	after insert or update or delete on t_other_fee
	for each row
	execute procedure update_total_ht_2();