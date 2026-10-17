# 🧪 End-to-End Integration Test Suite

Covers full cross-application operational chains between Bigin, Zoho Books, Google Workspace, and WhatsApp.

---

## Scenario: Sales-to-Receipt End-to-End Flow

### Pre-conditions
- Deal `Deal_Test_001` exists in Bigin with Amount $2,500.
- Customer `Acme Corp` has verified email and WhatsApp opt-in.

### Execution Sequence
1. **Transition Deal to "Contract Signed"**:
   - `PUT /v2/Pipelines/{deal_id}` updates stage.
2. **Anti-Duplicate Check & Invoice Creation**:
   - `financial_guard.py check_duplicate` verifies no invoice exists.
   - `financial_guard.py calculate_tax` computes tax (e.g. 18% IGST).
   - Draft invoice created in Zoho Books (`reference_number = Deal_Test_001`).
3. **Approval Gate**:
   - Agent presents itemized invoice summary to user and waits for confirmation.
4. **Notification Dispatch**:
   - Upon confirmation, invoice PDF link is dispatched via WhatsApp Business Cloud API.
5. **Payment Simulation & Verification**:
   - Bank webhook records payment in Zoho Books.
   - `financial_guard.py verify_payment` asserts payment status is `cleared`.
6. **Receipt Generation**:
   - Official receipt PDF downloaded from Books API and sent to customer.
   - Bigin deal updated to `Closed Won / Paid`.

### Pass Criteria
- No duplicate records created.
- Receipt issued **only** after status verified as `cleared`.
- Bigin deal contains full audit trail in Notes.
