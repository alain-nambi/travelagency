const { Client } = require("pg");
const prompt = require("prompt-sync")(({sigint: true}));

const client = new Client({
  host: "51.75.181.178",
  port: 5433,
  database: "db_flight_issoufali",
  user: "postgres",
  password: "MGbi@262**",
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

async function deleteTickerPassengerSegmentBy(client, pnrNumber) {
  const query = "delete from t_ticket_passenger_segment tps where tps.ticket_id in (select tt.id from t_ticket tt where tt.pnr_id = (select tp.id from t_pnr tp where tp.number = $1 ))"
  const { command, rowCount } = await client.query(query, [pnrNumber]);
  return {command, rowCount}
}

async function getPnrId(client, pnrNumber) {
  let number = String(pnrNumber).trim().toUpperCase()
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
  const query = "update t_ticket set transport_cost = 0, tax = 0, total = 0 where id = $1";
  const result = await client.query(query, [ticketId])
  return result;
}

async function getInvoiceDetails(params) {
  try {
    await client.connect();

    if (client._connected) { // Check if the client is connected
      console.info("> Client is connected");
      const { invoice_number, pnr_number } = params;
      const pnrId = await getPnrId(client, pnr_number);
      const passengerInvoiceRows = await getPassengerInvoice(client, invoice_number, pnrId);

      for (const row of passengerInvoiceRows) {
        await updateInvoiceDetails(client, row);

        // Reset cost of ticket to make it updatable
        // await resetTicketCost(client, row.ticket_id).then((result) => console.log(result))
      }

      // Remove all segment related to ticket
      // await deleteTickerPassengerSegmentBy(client, pnr_number).then((result) => console.log(result))
    } else {
      console.error("Client not connected.");
    }
  } catch (error) {
    console.error("Erreur de connexion :", error.message);
  } finally {
    if (client._connected) { // Close the client connection if it was opened
      client.end();
    }
  }
}

const readline = require('readline').createInterface({
  input: process.stdin,
  output: process.stdout
});

function setInvoiceAndPnrNumber () {
  readline.question('What is the invoice number?\n> ', (invoiceNumber) => {
    readline.question('What is the PNR number?\n> ', (pnrNumber) => {
      getInvoiceDetails({invoice_number: invoiceNumber, pnr_number: pnrNumber})
  
      // Now you can use invoiceNumber and pnrNumber in the rest of your code.
      readline.close(); // Close the readline interface after processing the input
    });
  });
}

setInvoiceAndPnrNumber()




