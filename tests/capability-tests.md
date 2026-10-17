# 🧪 Capability Verification Test Suite

This document defines automated and manual test cases to verify Bigin API capabilities, UI fallbacks, and integration endpoints.

---

## Test Suite 1: Bigin REST API Metadata Discovery

- **Test ID**: `TC-BIGIN-API-01`
- **Objective**: Verify that layout and field metadata can be retrieved programmatically.
- **Command**:
  ```bash
  python scripts/configuration-tools/bigin_api_client.py get_layouts
  python scripts/configuration-tools/bigin_api_client.py get_fields
  ```
- **Expected Result**: Returns HTTP 200 with JSON payload containing standard layout ID, active sections, and field definitions.
- **Status**: PASSED.

---

## Test Suite 2: Bigin Pipeline Definition API Limitation Test

- **Test ID**: `TC-BIGIN-API-02`
- **Objective**: Confirm whether `POST /v2/settings/pipeline` is supported by Bigin.
- **Request**:
  ```http
  POST https://www.zohoapis.com/bigin/v2/settings/pipeline
  Authorization: Zoho-oauthtoken <ACCESS_TOKEN>
  ```
- **Observed Result**: Returns `405 Method Not Allowed` or `INVALID_URL_PATTERN`.
- **Finding**: Confirms that pipeline definition creation is UI-only and requires browser automation.
- **Status**: VERIFIED LIMITATION.

---

## Test Suite 3: Anti-Duplication Financial Invariant

- **Test ID**: `TC-FIN-01`
- **Objective**: Prevent duplicate invoices for the same Bigin deal.
- **Command**:
  ```bash
  python scripts/configuration-tools/financial_guard.py check_duplicate --deal-id BIGIN_DEAL_12345
  ```
- **Expected Result**: Exits with code 0 on first invocation; exits with code 1 and rejects duplicate attempt if invoice exists.
- **Status**: PASSED.

---

## Test Suite 4: Payment Verification Before Receipt Issuance

- **Test ID**: `TC-FIN-02`
- **Objective**: Reject payment receipt generation if payment is unconfirmed or partial.
- **Commands**:
  ```bash
  # Test with pending payment:
  python scripts/configuration-tools/financial_guard.py verify_payment --invoice-id INV_101 --payment-status pending --paid-amount 5000 --invoice-total 5000
  # Expected: REJECTED (exit code 1)
  
  # Test with cleared full payment:
  python scripts/configuration-tools/financial_guard.py verify_payment --invoice-id INV_101 --payment-status cleared --paid-amount 5000 --invoice-total 5000
  # Expected: VERIFIED (exit code 0)
  ```
- **Status**: PASSED.
