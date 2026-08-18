---
title: "Enterprise Agentic AI Platform"
description: "NTT DATA · AI Engineer Advisor · Dec 2025 – Present"
weight: 2
hidemeta: true
ShowReadingTime: false
---

Multiple teams were independently rebuilding the same agentic-AI plumbing for every telecom
engagement — tool integration, agent-to-agent communication, governance, audit, rate limiting —
with no shared governance model and no reuse between them.
<!--more-->

I defined the reference architecture for a reusable platform layer instead of another one-off
build. MCP is the standard tool-integration primitive — any MCP-compliant agent can call any
registered tool without custom integration — and A2A is the protocol for cross-domain agent
requests (an OSS Assurance agent asking an Inventory agent for data, for example), so domain
teams don't couple their implementations to each other.

Domain agents (OSS Assurance, Inventory, Fulfillment, RAN Automation) are built as plugins on top
of this layer and inherit its governance automatically: per-agent OAuth2 identity, full tool-call
audit logging, configurable per-agent and per-tool rate limits, a human-in-the-loop approval
gateway for high-risk actions, and OpenTelemetry tracing per agent turn and tool call.

{{< agent-stack >}}

The governance layer is what I'd call the actual deliverable here — the platform is only reusable
because every domain agent inherits the same identity, audit, and approval model instead of
reinventing it.

**Stack:** Azure OpenAI, Azure AI Foundry, MCP (FastMCP), A2A, Kubernetes (AKS), OAuth2,
OpenTelemetry.
