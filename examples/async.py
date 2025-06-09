import asyncio
from chiefpay import AsyncClient, AsyncChiefPayClient

async def main():
    # Initialize the async client
    client = AsyncClient(api_key="your_api_key")

    try:
        # Get exchange rates
        rates = await client.get_rates()
        print("Exchange rates:", rates)

        # Create an invoice
        invoice = await client.create_invoice(
            order_id="564cca2e-30d5-4c69-90d5-fa3f368aea90",  # Order ID in your system
            description="Test Invoice",
            amount="15.4",  # If the amount is not specified, the payer can choose the amount themselves
            currency="RUB",  # Currently supported: USD and RUB (default is USD)
            fee_included=False,  # True to pass the commission to the payer
            accuracy="0.01",  # Consider the payment successful if at least 99% of the amount is paid
        )
        print("Created invoice:", invoice)

        # Get invoice details
        invoice_details = await client.get_invoice(id=invoice.id, order_id=invoice.order_id)
        print("Invoice details:", invoice_details)

        # Get invoice history
        invoice_history = await client.get_invoices(from_date="2025-03-01T15:18:00.000Z")
        print("Invoice history:", invoice_history)

        # Check if more requests are needed
        if invoice_history.total_count > len(invoice_history.invoices):
            print("Fetching more invoices...")
            more_invoices = await client.get_invoices(
                from_date=invoice_history.invoices[0].created_at,  # Invoices are in descending order
                to_date="2025-03-02T11:41:00.000Z",
                limit=100,
            )
            print("Additional invoices:", more_invoices)

    except Exception as e:
        print("Error:", e)

    # Initialize AsyncChiefPayClient (combines REST and WebSocket)
    try:
        chief_client = AsyncChiefPayClient(api_key="your_api_key")

        # Get wallet details
        wallet = await chief_client.rest.get_wallet(id="123", order_id="456")
        print("Wallet details:", wallet)

        # Get transaction history
        transaction_history = await chief_client.rest.get_transactions(from_date="2025-03-01T15:18:00.000Z")
        print("Transaction history:", transaction_history)

        # Check if more requests are needed
        if transaction_history.total_count > len(transaction_history.transactions):
            print("Fetching more transactions...")
            more_transactions = await chief_client.rest.get_transactions(
                from_date=transaction_history.transactions[0].created_at,  # Transactions are in descending order
                to_date="2025-03-02T11:41:00.000Z",
                limit=100,
            )
            print("Additional transactions:", more_transactions)

    except Exception as e:
        print("Error:", e)

# Run the async main function
if __name__ == "__main__":
    asyncio.run(main())