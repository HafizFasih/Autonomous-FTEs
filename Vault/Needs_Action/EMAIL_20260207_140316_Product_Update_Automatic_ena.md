---
type: email
from: CloudPlatform-noreply@google.com
from_name: Google Cloud
subject: [Product Update] Automatic enablement of new OpenTelemetry ingestion API
received: 2026-02-07T14:03:16.876424
priority: normal
message_id: <05850562b658e1815df50916d3971ff984f0d6f7-20392635-111816257@google.com>
status: pending
---

## Email from Google Cloud

**From:** Google Cloud <CloudPlatform-noreply@google.com>
**Subject:** [Product Update] Automatic enablement of new OpenTelemetry ingestion API
**Date:** Thu, 05 Feb 2026 04:18:32 -0800

---

## Content

Hello Aimoshah,

We’re writing to let you know that Cloud Observability has launched a new  
OpenTelemetry (OTel) ingestion API[1] that supports native OpenTelemetry  
Protocol (OTLP) logs, trace spans, and metrics. Starting March 4, 2026,  
this API will be added as a dependency for the current Cloud Logging, Cloud  
Trace, and Cloud Monitoring ingestion APIs. This change ensures a seamless  
transition as collection tools migrate to this new unified endpoint.

What you need to know

Key changes:

    - The existing Cloud Observability ingestion APIs  
(logging.googleapis.com, cloudtrace.googleapis.com, and  
monitoring.googleapis.com) are automatically activated when you create a  
Google Cloud project using the Google Cloud console or gcloud CLI. The  
behavior remains unchanged for projects created via API, which do not have  
these ingestion APIs enabled by default. Starting March 4, 2026, the new  
OTel ingestion endpoint telemetry.googleapis.com will automatically  
activate when any of these specified APIs are enabled.
    - In addition, we will automatically enable this new endpoint for all  
existing projects that already have current ingestion APIs active.

What you need to do

No action is required from you for this API enablement change, and there  
will be no disruption to your existing services. You may disable the API at  
any time by following these instructions[2].

Refer to the attachment for a list of the projects that will automatically  
enable the new endpoint.

We’re here to help

If you have any questions or require assistance, please contact Google  
Cloud Support[3].

Thanks for choosing Google Cloud Observability.

– The Google Cloud Team

[1]  
https://docs.cloud.google.com/stackdriver/docs/reference/telemetry/overview
[2] https://docs.cloud.google.com/service-usage/docs/enable-disable
[3] https://support.google.com/

© 2026 Google LLC 1600 Amphitheatre Parkway, Mountain View, CA 94043

You’ve received this mandatory service announcement to update you about  
important changes to Google Cloud or your account.

---

## Suggested Actions

- [ ] Reply to sender
- [ ] Forward to relevant party
- [ ] Archive after processing


## Metadata

- **Message ID:** <05850562b658e1815df50916d3971ff984f0d6f7-20392635-111816257@google.com>
- **Received:** Thu, 05 Feb 2026 04:18:32 -0800
