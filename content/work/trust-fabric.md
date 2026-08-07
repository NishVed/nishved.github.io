---
title: "AI Trust Fabric"
description: "Levo.ai · AI Enterprise Architect · Jan 2025 – Dec 2025 · Client: Insurance Information Bureau of India"
weight: 1
hidemeta: true
ShowReadingTime: false
---

The Insurance Information Bureau of India aggregates sensitive data from every insurance company
in the country. Perimeter security doesn't address insider threat or an AI-era access pattern:
autonomous agents, not just people, now request access to that data. Binary role-based access
control has no way to reason about that.
<!--more-->

I was sole architect for the AI Trust Fabric: a Zero Trust framework (NIST 800-207) structured as
PAP / PDP / PEP / PIP — policy authoring, real-time policy decisions, enforcement at every access
point, and context aggregation (identity, device posture, location, time, data classification,
session history). On top of that sits an **Adaptive Trust Engine**, computing a continuous trust
score per request rather than a binary allow/deny, driving ALLOW / STEP-UP-AUTH / DENY decisions.

A RAG policy-intelligence layer (LangGraph orchestration, running on Ollama) lets analysts and
agents query IRDAI regulations in natural language — fully offline, because certain IIB
environments have no internet egress. That was a hard constraint, not a preference: without
offline inference, the AI governance layer couldn't have shipped at all.

Every AI-assisted access decision carries a traceable rationale — which policy matched, which
trust signals fired — and AI agents have their own workload identity, distinguishable from human
actions in the audit trail.

This work is now a [registered design](/publications/) with the Government of India and the
basis of a paper in progress on national-scale insurance security in the AI era.

**Stack:** Microsoft Entra ID, ZTNA, IAM, CrewAI, LangGraph, Ollama, MCP, Kubernetes.
