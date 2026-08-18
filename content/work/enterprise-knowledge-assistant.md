---
title: "Enterprise Knowledge Assistant (SCAI)"
description: "Internal platform · AI Engineer Advisor · Dec 2025 – Present"
weight: 3
hidemeta: true
ShowReadingTime: false
---

Institutional knowledge was fragmented across BI dashboards (metrics), document repositories
(technical docs), training content, and case-study archives — no single entry point, and business
teams had no time to connect the dots under pressure.
<!--more-->

The design uses two distinct paths rather than one RAG pipeline, because the query types are
fundamentally different. Live metrics are answered by querying Power BI semantic models directly
through Microsoft Fabric, with Row-Level Security passed through using the calling user's
identity — metrics are never embedded into a vector store, because stale or hallucinated numbers
are worse than no answer in an enterprise context. Document and knowledge queries go through
Azure AI Search over Microsoft Graph–indexed content, which enforces the same permissions users
already have in the document repository natively. An LLM query classifier routes each question to the right
path, or both, when a query spans metrics and documentation.

{{< dual-path >}}

**My role:** sole architect for the end-to-end design — the dual-path agent architecture, the
query classification approach, the RAG ingestion pipeline, and the Power BI RLS passthrough.

**Stack:** Azure OpenAI (GPT-4o), Azure AI Search, Microsoft Fabric / Power BI, Microsoft Graph,
Cosmos DB, Azure Entra ID.
