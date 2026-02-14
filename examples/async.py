import asyncio
from chiefpay import AsyncClient, AsyncChiefPayClient
from chiefpay.types import ChainToken
from chiefpay.exceptions import APIError, ChiefPayErrorCode


async def main():
    # Initialize the async client
    async with AsyncClient(api_key="your_api_key") as client:
        # Get exchange rates (no auth required)
        try:
            rates = await client.get_rates()
            for rate in rates[:3]:
                print(f"{rate.name}: {rate.rate}")
        except Exception as e:
            print(f"Error getting rates: {e}")

        # Get available payment methods (no auth required)
        try:
            payment_methods = await client.get_payment_methods()
            for method in payment_methods.paymentMethods[:3]:  # Show first 3
                print(f"{method.methodName}: {method.chain}/{method.token}")
        except Exception as e:
            print(f"Error getting payment methods: {e}")

        # Create an invoice
        try:
            invoice = await client.create_invoice(
                order_id="564cca2e-30d5-4c69-90d5-fa3f368aea90",  # Order ID in your system
                description="Test Invoice - Payment for Order #123",
                amount="15.4",  # String format, not float. If not specified, payer can choose the amount
                fee_included=False,  # True to pass the commission to the payer
                accuracy="0.01",  # String format. Consider payment successful if at least 99% of the amount is paid
                url_success="https://example.com/success",
                url_return="https://example.com/cancel",
                # chain_token=ChainToken(chain="TRON", token="USDT"),  # Optional: pre-select payment method
            )
            print(f"Invoice ID: {invoice.id}")
            print(f"Status: {invoice.status}")
            print(f"Payment URL: {invoice.url}")

            # Get invoice details by ID
            invoice_details = await client.get_invoice(id=invoice.id)
            print(f"Order ID: {invoice_details.order_id}")
            print(f"Amount: {invoice_details.amount} USD")
            print(f"Status: {invoice_details.status}")

            # Update invoice (if amount or chain_token were not set initially)
            if not invoice.payment_details:
                updated_invoice = await client.patch_invoice(
                    id=invoice.id, chain_token=ChainToken(chain="TRON", token="USDT")
                )
                print(
                    f"Updated payment method: {updated_invoice.payment_details.chain}/{updated_invoice.payment_details.token}"
                )

            # Prolong invoice expiration
            prolonged_invoice = await client.prolongate_invoice(id=invoice.id)
            print(f"New expiration: {prolonged_invoice.expired_at}")
            print(f"Original expiration: {prolonged_invoice.original_expired_at}")

        except APIError as e:
            if e.code == ChiefPayErrorCode.ALREADY_EXISTS:
                print("Invoice with this order_id already exists")
            else:
                print(f"API Error: {e.code} - {e.errors}")
            print()
        except Exception as e:
            print(f"Error: {e}")

        # Get invoice history
        try:
            invoice_history = await client.get_invoices(
                from_date="2025-03-01T00:00:00.000Z",
                to_date="2025-03-31T23:59:59.999Z",
                limit=10,
            )
            print(f"Found {len(invoice_history.invoices)} invoices")
            print(f"Total count: {invoice_history.total_count}")

            # Show first invoice
            if invoice_history.invoices:
                first = invoice_history.invoices[0]
                print(f"Latest invoice: {first.id} - {first.status}")

            # Pagination example
            if invoice_history.total_count > len(invoice_history.invoices):
                print("Fetching next page...")
                more_invoices = await client.get_invoices(
                    from_date=invoice_history.invoices[
                        -1
                    ].created_at,  # Use last invoice date
                    to_date="2025-03-31T23:59:59.999Z",
                    limit=10,
                )
                print(f"Next page: {len(more_invoices.invoices)} invoices")

        except Exception as e:
            print(f"Error getting invoice history: {e}")

        # Create a wallet
        try:
            wallet = await client.create_wallet(order_id="wallet-order-async-123")
            print(f"Wallet ID: {wallet.id}")
            print("Addresses:")
            for address in wallet.addresses:
                print(f"{address.method_name}: {address.address}")

            # Get wallet details
            wallet_details = await client.get_wallet(id=wallet.id)
            print(f"Order ID: {wallet_details.order_id}")
            print(f"Number of addresses: {len(wallet_details.addresses)}")

        except APIError as e:
            if e.code == ChiefPayErrorCode.ALREADY_EXISTS:
                print("Wallet with this order_id already exists")
            else:
                print(f"API Error: {e.code} - {e.errors}")
            print()
        except Exception as e:
            print(f"Error: {e}\n")

        # Get transaction history
        try:
            transaction_history = await client.get_transactions(
                from_date="2025-03-01T00:00:00.000Z", limit=10
            )
            print(f"Found {len(transaction_history.transactions)} transactions")
            print(f"Total count: {transaction_history.total_count}")

            # Show first transaction
            if transaction_history.transactions:
                first_tx = transaction_history.transactions[0]
                print(f"Latest: {first_tx.txid[:16]}... - {first_tx.usd} USD")
                if first_tx.wallet:
                    print(f"Wallet: {first_tx.wallet.order_id}")

        except Exception as e:
            print(f"Error getting transaction history: {e}\n")

    #  Using AsyncChiefPayClient (combines REST and WebSocket)
    try:
        async with AsyncChiefPayClient(api_key="your_api_key").rest as chief_client:
            # REST API via AsyncChiefPayClient
            rates = await chief_client.get_rates()
            print(f"Rates via AsyncChiefPayClient: {len(rates)} rates available")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
