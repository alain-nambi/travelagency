const express = require('express');
const app = express();
const cors = require('cors');
const bodyParser = require('body-parser'); 
const { Pool } = require("pg");

const port = 1000;

app.use(express.json());
app.use(cors());
app.use(bodyParser.json());

// Create a pool with your database connection details
const pool = new Pool({
  host: "localhost",
  port: 5432,
  database: "db_flight_issoufali",
  user: "postgres",
  password: "maphie",
});

app.post('/api/pnr_unorder', async (req, res) => {
  try {
    // Create new client for each request
    const client = await pool.connect()

    const { invoiceNumber, pnrNumber, motif } = req.body;

    console.log(`Invoice Number: ${invoiceNumber}`);
    console.log(`PNR Number: ${pnrNumber}`);
    console.log(`Motif: ${motif}`);


    if (!invoiceNumber || !pnrNumber) {
      throw new Error("Veuillez fournir au moins deux paramètres : invoiceNumber et pnrNumber.");
    }

    const params = { invoice_number: invoiceNumber, pnr_number: pnrNumber, motif: motif };
    await getInvoiceDetails(client, params);
    // await deletePassengerInvoice(client,pnrNumber, invoiceNumber)


    res.json({
      message: "ok",
      result: { invoiceNumber, pnrNumber },
    });

    

    client.release();
  } catch (error) {
    console.error(error.message);
    res.status(400).json({ error: error.message });
  }
});

// Start the server
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});




async function updateInvoiceDetails(client, invoice) {
  const { id, client_id, ticket_id, fee_id, other_fee_id } = invoice;

  if (id) {
    await client.query(
      "UPDATE t_passenger_invoice SET is_invoiced = false WHERE id = $1",
      [id]
    );
  }

  if (ticket_id) {
    const { rowCount } = await client.query(
      "UPDATE t_ticket SET is_invoiced = false WHERE id = $1 RETURNING number",
      [ticket_id]
    );

    if (rowCount > 0) {
      const { number } = (
        await client.query(
          "SELECT tt.number FROM t_ticket tt WHERE tt.id = $1",
          [ticket_id]
        )
      ).rows[0];
      console.log(`> Ticket: ${number} has been unordered !`);
    }
  }

  if (fee_id) {
    await client.query("UPDATE t_fee SET is_invoiced = false WHERE id = $1", [
      fee_id,
    ]);
  }

  if (other_fee_id) {
    await client.query(
      "UPDATE t_other_fee SET is_invoiced = false WHERE id = $1",
      [other_fee_id]
    );
  }


  // if (client_id) {
  //   await client.query("DELETE FROM t_passenger_invoice WHERE id = $1", [id]);
  // }
}

async function get_details_invoice(client,pnr_id){
  const details = await client.query("SELECT * FROM t_passenger_invoice WHERE pnr_id = $1 ", [pnr_id]);
  return details.rows;
}

async function save_invoice_canceled(client,pnr_id,invoice_number,motif){
  const details = await get_details_invoice(client,pnr_id);
  for (const detail of details) {
    if(detail['ticket_id'] !== null || detail['other_fee_id'] !== null ){
      await client.query("INSERT INTO t_invoices_canceled (pnr_id, invoice_number, motif, date, ticket_id, other_fee_id) VALUES ($1, $2, $3, CURRENT_DATE, $4, $5)", [pnr_id, invoice_number, motif, detail['ticket_id'], detail['other_fee_id']]);
    }
    
}
  

}

async function deleteTickerPassengerSegmentBy(client, pnrNumber) {
  const query =
    "delete from t_ticket_passenger_segment tps where tps.ticket_id in (select tt.id from t_ticket tt where tt.pnr_id = (select tp.id from t_pnr tp where tp.number = $1 ))";
  const { command, rowCount } = await client.query(query, [pnrNumber]);
  return { command, rowCount };
}

async function getPnrId(client, pnrNumber) {
  let number = pnrNumber.trim();
  const query = "SELECT id from t_pnr tp where tp.number = $1";
  const result = await client.query(query, [number]);
  return result.rows[0].id;
}

async function getPassengerInvoice(client, invoiceNumber, pnrId) {
  const query =
    "SELECT * from t_passenger_invoice tpi where tpi.invoice_number = $1 and tpi.pnr_id = $2";
  const result = await client.query(query, [invoiceNumber, pnrId]);
  return result.rows;
}

async function resetTicketCost(client, ticketId) {
  const query =
    "update t_ticket set transport_cost = 0, tax = 0, total = 0 where id = $1";
  const result = await client.query(query, [ticketId]);
  return result;
}

async function getInvoiceDetails(client, params) {
  try {
    if (client._connected) {
      const { invoice_number, pnr_number, motif } = params;
      const pnrId = await getPnrId(client, pnr_number);
      const passengerInvoiceRows = await getPassengerInvoice(
        client,
        invoice_number,
        pnrId
      );

      for (const row of passengerInvoiceRows) {
        await updateInvoiceDetails(client, row);
      }
      try {
        await save_invoice_canceled(client,pnrId,invoice_number, motif)
      } catch (error) {
        console.log('Errrrorrrr: ', error.message);
      }
      
     
      // Remove all segment related to ticket
      // await deleteTickerPassengerSegmentBy(client, pnr_number).then((result) => console.log(result))
    } else {
      console.error("Client not connected.");
    }
  } catch (error) {
    console.error("Erreur de connexion :", error.message);
  }
}

