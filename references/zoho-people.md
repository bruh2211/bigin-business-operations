# 👥 Zoho People & HR Integration Reference

This document covers the technical integration between Zoho Bigin CRM and Zoho People, synchronization mechanisms, and role-based operational assignment.

---

## 1. Architectural Reality & Integration Mechanism

> [!IMPORTANT]
> **No Native Toggle Exists**: Zoho Bigin does **NOT** feature a built-in native integration toggle for Zoho People in its standard settings.
> 
> The official supported mechanism for integrating Zoho Bigin and Zoho People is via **Zoho Flow** or direct REST API webhooks.

### CRM Users vs. HR Employees: Core Distinction
- **Bigin CRM User (`Users` module)**: A licensed seat with login access to Bigin who can own deals, view contacts, and execute CRM tasks.
- **Zoho People Employee (`Employee` module)**: An internal employee profile containing departmental details, designation, reporting manager, attendance, and leave status.
- *Rule*: Never attempt to create a CRM licensed user by merely inserting a record into Zoho People, and vice versa.

---

## 2. Supported Cross-Application Workflows (via Zoho Flow)

### Workflow 1: Employee Onboarding & Bigin Account Setup
- **Trigger**: New employee record created in Zoho People.
- **Flow Logic**:
  1. Check employee department. If `Department == "Sales"` or `"Customer Success"`:
  2. Send invitation / create user profile in Bigin CRM via Bigin Admin API or email notification.
  3. Assign employee to the relevant Team Pipeline (e.g. "Enterprise Sales").

### Workflow 2: Deal Ownership Re-routing on Leave / Vacation
- **Trigger**: Employee status changes to "On Leave" in Zoho People.
- **Flow Logic**:
  1. Query Bigin for active deals owned by `Employee_Email`.
  2. Temporarily reassign open follow-up tasks to the designated reporting manager or backup teammate.

---

## 3. Zoho People REST API Details

- **Base URL**: `https://people.zoho.com/people/api`
- **Employee Lookup**:
  `GET /forms/json/employee/getRecordByID?recordId=<EMPLOYEE_ID>`
- **Scopes**: `ZohoPeople.employee.ALL`
