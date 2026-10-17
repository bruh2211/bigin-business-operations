# 📊 Zoho Bigin Subscription Limits & Edition Constraints

This reference specifies hard quotas, architectural limits, and feature availability across Bigin tiers. Use this to validate configuration requests before execution.

---

## 1. Plan Comparison Matrix

| Quota / Feature | Free Tier | Express Tier ($7/user/mo) | Premier Tier ($12/user/mo) | Bigin 360 Tier ($20/user/mo) |
| :--- | :--- | :--- | :--- | :--- |
| **Team Pipelines** | 1 (Fixed) | 3 | 5 | 15 (includes 4 defaults) |
| **Additional Team Pipelines** | Not available | $5/month add-on | $5/month add-on | Included / add-on |
| **Sub-Pipelines** | 1 | 15 (3 default) | 25 (5 default) | 75 (15 default) |
| **Stages per Sub-Pipeline** | Up to 25 | Up to 25 | Up to 25 | Up to 25 |
| **Custom Fields per Pipeline** | 5 | 10 | 25 | 50 |
| **Record Storage Capacity** | 500 records | 50,000 records | 100,000 records | 500,000 records |
| **Data Storage** | 20 MB | 1 GB | 2 GB | 5 GB |
| **File Storage** | 100 MB | 1 GB | 5 GB | 10 GB |
| **Workflow Rules / Module** | 3 | 10 | 30 | 50 |
| **Webhooks Support** | ❌ No | ✅ Yes (1,000/day) | ✅ Yes (5,000/day) | ✅ Yes (10,000/day) |
| **Email-In Topping** | ❌ No | ✅ Yes | ✅ Yes | ✅ Yes |
| **WhatsApp Topping** | ❌ No | ✅ Yes | ✅ Yes | ✅ Yes |
| **Zoho Books Topping** | ❌ No | ✅ Yes | ✅ Yes | ✅ Yes |

---

## 2. Pre-flight Validation Checklist

Before proposing or attempting to create a Team Pipeline or sub-pipeline, the agent MUST run:

1. **Pipeline Count Check**:
   Count existing Team Pipelines in the organization:
   $$\text{Current Pipelines} + 1 \le \text{Edition Limit}$$
   If limit is reached, advise user to either purchase a \$5 add-on or upgrade edition.
2. **Sub-Pipeline Check**:
   $$\text{Current Sub-Pipelines in Pipeline} + 1 \le \text{Max Sub-Pipelines}$$
3. **Stage Count Validation**:
   Enforce $\le 25$ stages per sub-pipeline.
4. **Custom Field Capacity**:
   Enforce $\le \text{Custom Fields per Pipeline}$ for the target tier.
