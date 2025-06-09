from chiefpay import Client, ChiefPayClient

# Initialize the client
client = Client(api_key="your_api_key")

try:
    # Get exchange rates
    rates = client.get_rates()
    print("Exchange rates:", rates)

    # Create an invoice
    invoice = client.create_invoice(
        order_id="564cca2e-30d5-4c69-90d5-fa3f368aea90",  # Order ID in your system
        description="Test Invoice",
        amount="15.4",  # If the amount is not specified, the payer can choose the amount themselves
        currency="RUB",  # Currently supported: USD and RUB (default is USD)
        fee_included=False,  # True to pass the commission to the payer
        accuracy="0.01",  # Consider the payment successful if at least 99% of the amount is paid
    )
    print("Created invoice:", invoice)

    # Get invoice details
    invoice_details = client.get_invoice(id=invoice.id)
    print("Invoice details:", invoice_details)

    # Get invoice history
    invoice_history = client.get_invoices(from_date="2025-03-01T15:18:00.000Z")
    print("Invoice history:", invoice_history)

    # Check if more requests are needed
    if invoice_history.total_count > len(invoice_history.invoices):
        print("Fetching more invoices...")
        more_invoices = client.get_invoices(
            from_date=invoice_history.invoices[0].created_at,  # Invoices are in descending order
            to_date="2025-03-02T11:41:00.000Z",
            limit=100,
        )
        print("Additional invoices:", more_invoices)

except Exception as e:
    print("Error:", e)

# Initialize ChiefPayClient (combines REST and WebSocket)
try:
    chief_client = ChiefPayClient(api_key="your_api_key")

    # Get wallet details
    wallet = chief_client.rest.get_wallet(id="123", order_id="456")
    print("Wallet details:", wallet)

    # Get transaction history
    transaction_history = chief_client.rest.get_transactions(from_date="2025-03-01T15:18:00.000Z")
    print("Transaction history:", transaction_history)

    # Check if more requests are needed
    if transaction_history.total_count > len(transaction_history.transactions):
        print("Fetching more transactions...")
        more_transactions = chief_client.rest.get_transactions(
            from_date=transaction_history.transactions[0].created_at,  # Transactions are in descending order
            to_date="2025-03-02T11:41:00.000Z",
            limit=100,
        )
        print("Additional transactions:", more_transactions)

except Exception as e:
    print("Error:", e)