# 💬 Email & WhatsApp Business Communications Reference

This document covers communication channels, WhatsApp Business API rules, approved message templates, and CRM integration within Zoho Bigin.

---

## 1. Bigin WhatsApp Business Topping

Zoho Bigin provides an official **WhatsApp Topping** that connects WhatsApp Business to the CRM:

### Key Features
- **Shared Team Inbox**: Multiple sales/support reps can manage WhatsApp messages from a single centralized business phone number.
- **Two-Way Messaging from Record**: Initiate chats and send messages directly from a Contact or Deal record.
- **Automated Stage Notifications**: Trigger template-based WhatsApp alerts when deals enter specific pipeline stages.

---

## 2. Meta WhatsApp Business Compliance Rules

When automating WhatsApp messaging via Bigin or Meta Cloud API:

1. **Pre-Approved Templates for Business-Initiated Messages**:
   - Any message initiated by the business (outside the active 24-hour customer care window) **MUST** use an officially approved Meta WhatsApp Template.
   - Free-form text can only be sent if the customer replied within the last 24 hours.
2. **Explicit Opt-In Required**:
   - The contact in Bigin must have an explicit `WhatsApp_Opt_In == true` flag before any automated message is dispatched.
   - Storing opt-in source and timestamp is mandatory for regulatory compliance (GDPR / TCPA).

---

## 3. Email-In & Automated Email Sequences

- **Email-In Topping**: Forwards emails sent to a dedicated alias (e.g. `deals@yourcompany.bigin.com`) and automatically creates a new Deal or Contact in a designated sub-pipeline.
- **Email Templates**:
  - Must use merge fields: `${Contacts.First Name}`, `${Pipelines.Deal Name}`, `${Users.First Name}`.
  - All automated outreach must provide a clear unsubscribe or opt-out mechanism.
