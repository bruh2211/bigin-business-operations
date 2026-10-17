# 📋 Workflow: Invoice & Verified Payment Receipt

This runbook guides the agent through creating a Zoho Books invoice and safely verifying payments before issuing official payment receipts.

---

## ⚠️ Financial Guardrail Invariant
- **Creating an invoice DOES NOT equal receipt of payment.**
- **A payment receipt is issued ONLY upon confirming a cleared payment record in Zoho Books.**

---

## Procedure Steps

### 1. Invoice Pre-Check & Anti-Duplication
Run the financial guard to ensure no duplicate invoice exists for this Bigin Deal:
```bash
python scripts/configuration-tools/financial_guard.py check_duplicate --deal-id BIGIN_DEAL_12345
```

### 2. Generate Draft Invoice
1. Structure line items, rates, and tax calculations.
2. Call Zoho Books API to create the invoice:
   ```bash
   python scripts/configuration-tools/financial_guard.py create_invoice --deal-id BIGIN_DEAL_12345 --customer-id CUST_987 --amount 5000.00
   ```
3. Request human approval to send the invoice to the customer.

### 3. Payment Verification Polling
When notified of client payment, do not assume money is received:
1. Poll Zoho Books for confirmed payment:
   ```bash
   python scripts/configuration-tools/financial_guard.py verify_payment --invoice-id INV_554433
   ```
2. Verify:
   - `status == "success"`
   - `amount_received >= invoice_total`

### 4. Issue Official Payment Receipt & Update CRM
1. Once confirmed, retrieve the official payment receipt PDF from Zoho Books.
2. Send receipt to client via email/WhatsApp.
3. Update the Bigin deal stage to `Closed Won / Paid` and attach the payment transaction reference.
