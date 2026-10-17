# 💰 Zoho Books & Financial Operations Reference

This document governs financial workflows, Zoho Books API integration, tax calculations (GST/VAT), anti-duplication mechanisms, and strict financial security invariants.

---

## 1. Non-Negotiable Financial Invariants

> [!CAUTION]
> **Financial Safeguard Rules for AI Agents:**
> 1. **An invoice is NEVER proof of payment.** An invoice represents an account receivable (money owed), not money collected.
> 2. **Never mark a deal "Closed Won / Paid" or generate a payment receipt upon invoice creation.**
> 3. **Payment Receipt Generation**: A receipt can ONLY be generated after the agent queries Zoho Books (`GET /api/v3/customerpayments/{id}`) and verifies that:
>    - The payment record exists and is linked to the invoice.
>    - Payment status is `cleared` / `success`.
>    - Payment amount matches or exceeds the due invoice amount.
> 4. **Anti-Duplication**: Every invoice creation request must include the Bigin Deal ID in the `reference_number` field. The agent must search existing invoices by `reference_number` before sending a `POST` request.
> 5. **Human Approval**: The agent must present the itemized invoice draft to the user and obtain explicit approval before transmitting it to the customer.

---

## 2. Zoho Books API Endpoints & Operations

Base URL: `https://www.zohoapis.com/books/v3` (Regional domains apply: `.eu`, `.in`, `.com.au`, etc.)
Headers: `Authorization: Zoho-oauthtoken <ACCESS_TOKEN>`, `X-com-zoho-books-organizationid: <ORG_ID>`

### Invoice Creation (`POST /api/v3/invoices`)
```json
{
  "customer_id": "481000000029312",
  "reference_number": "BIGIN-DEAL-481000000184712",
  "date": "2026-10-17",
  "due_date": "2026-10-31",
  "line_items": [
    {
      "item_id": "481000000098001",
      "name": "Enterprise Implementation Services",
      "rate": 5000.00,
      "quantity": 1,
      "tax_id": "481000000005111"
    }
  ],
  "is_inclusive_tax": false,
  "notes": "Thank you for partnering with us. Please reference BIGIN-DEAL-481000000184712 on your wire transfer."
}
```

### Retrieving Customer Payments & Receipts
1. **Search Payments for Invoice**:
   `GET /api/v3/customerpayments?invoice_id=481000000199045`
2. **Retrieve Payment Record**:
   `GET /api/v3/customerpayments/{payment_id}`
   *Verify that `status == "success"` or `amount == invoice_total`.*
3. **Download PDF Receipt**:
   `GET /api/v3/customerpayments/{payment_id}/pdf`

---

## 3. GST, Tax & E-Invoicing Compliance (India / Global)

- **GST Rules (India)**:
  - Intra-state transaction (Same State Code): Apply **CGST** ($9\%$) + **SGST** ($9\%$).
  - Inter-state transaction (Different State Code): Apply **IGST** ($18\%$).
  - Mandatory HSN/SAC code validation for all line items.
- **E-Invoicing Eligibility**:
  - If organization turnover exceeds government threshold (e.g. ₹5 Cr in India), generate IRN (Invoice Reference Number) and QR code via Zoho Books e-Invoicing integration before sending PDF to client.
