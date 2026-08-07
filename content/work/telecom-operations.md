---
title: "Telecom Operations Intelligence Assistant"
description: "NTT DATA engagement · AI Engineer Advisor · Dec 2025 – Present"
weight: 5
hidemeta: true
ShowReadingTime: false
---

Telecom operations teams manage domain-specific OSS systems — RAN, Core, Transport, Inventory,
Assurance — that don't surface cross-domain correlations on their own. A degraded RAN KPI might
trace back to a Core issue or a Transport link, and finding out required manually querying
multiple systems and pulling in multiple domain specialists.
<!--more-->

Each OSS domain has its own data model, API, and metric vocabulary — a single agent trying to
hold all of that in context makes query planning unreliable. So the architecture is multi-agent
by domain: a query-planning agent decomposes a natural-language question and dispatches it to
domain-specialist agents (RAN, Core, Transport, Inventory/Assurance), each with its own OSS-API
tool access. A correlation layer then assembles an evidence-backed answer — cited by system,
network element, metric, and timestamp — rather than letting the model summarize without
grounding.

**My role:** architected the cross-domain operational analytics and evidence-based response
design; designed the multi-agent orchestration, the correlation engine, and the OSS integration
architecture across all five domains.

**Stack:** Azure OpenAI, multi-agent orchestration, semantic search, REST APIs, OpenTelemetry.
