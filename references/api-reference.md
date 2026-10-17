# 🔌 Zoho Bigin REST API Reference

Comprehensive reference for Bigin's REST API v2, endpoints, authentication headers, error codes, and rate limits.

---

## 1. Multi-Data-Center Base URLs

Bigin accounts are hosted across multiple regional data centers. Ensure requests target the correct base URL matching your organization's domain:

| Region | Accounts Domain (OAuth) | API Domain Base URL |
| :--- | :--- | :--- |
| **United States (US)** | `https://accounts.zoho.com` | `https://www.zohoapis.com/bigin/v2` |
| **Europe (EU)** | `https://accounts.zoho.eu` | `https://www.zohoapis.eu/bigin/v2` |
| **India (IN)** | `https://accounts.zoho.in` | `https://www.zohoapis.in/bigin/v2` |
| **Australia (AU)** | `https://accounts.zoho.com.au` | `https://www.zohoapis.com.au/bigin/v2` |
| **Japan (JP)** | `https://accounts.zoho.jp` | `https://www.zohoapis.jp/bigin/v2` |
| **China (CN)** | `https://accounts.zoho.com.cn` | `https://www.zohoapis.com.cn/bigin/v2` |

---

## 2. Authentication & Headers

Bigin enforces OAuth 2.0 authentication. Every API request must pass the bearer token:

```http
Authorization: Zoho-oauthtoken <ACCESS_TOKEN>
Content-Type: application/json
```

### Essential Scopes
- **Modules Read/Write**: `ZohoBigin.modules.ALL` (or granular: `ZohoBigin.modules.pipelines.ALL`, `ZohoBigin.modules.contacts.ALL`)
- **Settings & Metadata Read**: `ZohoBigin.settings.READ`
- **User Information**: `ZohoBigin.users.READ`

### Refresh Token Flow
Access tokens expire every 60 minutes. Refresh them using:

```http
POST https://accounts.zoho.com/oauth/v2/token
Content-Type: application/x-www-form-urlencoded

refresh_token=<REFRESH_TOKEN>&
client_id=<CLIENT_ID>&
client_secret=<CLIENT_SECRET>&
grant_type=refresh_token
```

---

## 3. Core Module Endpoints

### Pipelines (Deals) Module
Module API Name: `Pipelines`

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/bigin/v2/Pipelines` | List all deals / pipeline records (paginated, 200 per page). |
| `GET` | `/bigin/v2/Pipelines/{id}` | Retrieve specific deal details including stage and sub-pipeline. |
| `POST` | `/bigin/v2/Pipelines` | Create one or more new deals. |
| `PUT` | `/bigin/v2/Pipelines/{id}` | Update an existing deal (e.g., transition stage, update amount). |
| `DELETE` | `/bigin/v2/Pipelines/{id}` | Move deal to trash. |

#### Create Record Payload Example
```json
{
  "data": [
    {
      "Deal_Name": "Enterprise Cloud Migration",
      "Amount": 75000.00,
      "Pipeline": "Cloud Solutions",
      "Sub_Pipeline": "Migration Track",
      "Stage": "Qualification",
      "Closing_Date": "2026-12-15",
      "Contact_Name": {
        "id": "481000000109012"
      }
    }
  ]
}
```

### Contacts & Companies Modules
- **Contacts**: `/bigin/v2/Contacts`
- **Companies (Accounts)**: `/bigin/v2/Accounts`
- **Products**: `/bigin/v2/Products`
- **Notes**: `/bigin/v2/Notes`
- **Tasks**: `/bigin/v2/Tasks`

---

## 4. Settings & Layout Endpoints (Read Metadata)

Use these endpoints to discover existing pipelines, stage picklist values, and field configurations:

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/bigin/v2/settings/layouts?module=Pipelines` | Get layouts, sub-pipeline metadata, and visible sections. |
| `GET` | `/bigin/v2/settings/fields?module=Pipelines` | Get all field definitions, mandatory flags, and stage picklist options. |
| `GET` | `/bigin/v2/settings/modules` | List all active modules and their API names. |

> [!WARNING]
> Bigin does **NOT** expose a `POST /v2/settings/pipeline` endpoint for creating new Team Pipeline structures or configuring sub-pipelines. Attempting a POST request returns `405 Method Not Allowed` or `INVALID_URL_PATTERN`. Pipeline creation must be handled via browser automation.

---

## 5. API Rate Limits & Quotas

- **Concurrency Limit**: Maximum 10 concurrent requests per organization.
- **Daily Call Limits**:
  - Express: 25,000 requests/day
  - Premier: 100,000 requests/day
  - Bigin 360: 250,000 requests/day
- **Pagination Limit**: Maximum 200 records per page (`?per_page=200&page=1`).
