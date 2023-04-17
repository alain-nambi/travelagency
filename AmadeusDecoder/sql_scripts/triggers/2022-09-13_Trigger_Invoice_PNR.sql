drop function new_invoice, new_invoice_detail, new_client_detail cascade;

--auto create invoice on pnr creation
CREATE OR REPLACE FUNCTION new_invoice() RETURNS TRIGGER AS
$BODY$
BEGIN
    INSERT INTO
        t_invoice(pnr_id)
        VALUES(new.id);

           RETURN new;
END;
$BODY$
language plpgsql;

CREATE TRIGGER trig_invoice_pnr
     AFTER INSERT ON t_pnr
     FOR EACH ROW
     EXECUTE PROCEDURE new_invoice();
    
--auto create invoice detail on invoice creation 
CREATE OR REPLACE FUNCTION new_invoice_detail() RETURNS TRIGGER AS
$BODY$
BEGIN
	INSERT INTO
		t_invoice_detail(invoice_id, totalht, tva_sce, total, total_fees, total_tax)
	VALUES
		(new.id, 0, 0, 0, 0, 0);
		
		RETURN new;
END;
$BODY$
language plpgsql;

CREATE TRIGGER trigger_invoice_detail
	AFTER INSERT ON t_invoice
	FOR EACH ROW
	EXECUTE PROCEDURE new_invoice_detail();

--auto create client on invoice creation
CREATE OR REPLACE FUNCTION new_client_detail() returns trigger as
$body$
begin
	insert into
		t_client_address(clientid)
	values
		(new.id);
		return new;
end;
$body$
language plpgsql;

create trigger trigger_new_client_detail
	after insert on t_client
	for each row
	execute procedure new_client_detail();
	
