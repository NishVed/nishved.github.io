---
title: "Building the Trust Fabric: Why Zero Trust Alone Isn't Enough in the AI Era"
date: 2026-08-11
description: "Zero Trust was designed for a world where humans authenticate. It was not designed for a world where AI agents reason over sensitive data, make decisions, and call other agents — without a human in the loop."
tags: ["Zero Trust", "AI Governance", "Agentic AI", "NIST 800-207", "Enterprise Security", "Trust Fabric"]
ShowToc: true
TocOpen: false
---

When I was asked to design the security architecture for a national-scale insurance data ecosystem
— one that aggregates sensitive data from every insurance company across an entire country — I
quickly realised that Zero Trust, as most organisations implement it, would not be sufficient.

Zero Trust was designed for a world where humans authenticate and access systems. It was not
designed for a world where AI agents authenticate, reason over sensitive data, make decisions, and
call other agents — all within milliseconds, at scale, without a human in the loop.

That gap is what led me to develop what I now call the **AI Trust Fabric**: a security architecture
that extends Zero Trust with an AI-awareness layer — one that governs not just who accesses data,
but *how AI systems access it, what decisions they make with it, and whether those decisions can
be explained and audited*.

## The Problem with Perimeter Security

Traditional enterprise security is built on a flawed premise: trust everything inside the network,
verify nothing. Once an attacker — or a compromised AI agent — is inside, they have broad access.

Zero Trust (NIST 800-207) was the right response to this. Never trust, always verify. Every access
request is authenticated and authorised, regardless of network location. In theory, this closes the
perimeter problem.

But here's what most Zero Trust implementations still miss: **they are binary**.

An access request is either allowed or denied. There is no concept of contextual trust — the idea
that the same user, with the same credentials, accessing the same data, at 2am from an unusual
location on an unmanaged device, should receive a different level of access than they would at 9am
from their usual device on a corporate network.

And they are static. Once a session is established, trust is not continuously re-evaluated.

When you add AI agents to this picture — agents that may have broad permissions, that act
autonomously, and that can chain tool calls in ways no human designed — the stakes of a static,
binary trust model become very high.

## The Trust Fabric Architecture

The Trust Fabric is not a replacement for Zero Trust. It is Zero Trust, extended.

It is built on four structural principles:

### 1. Policy-driven access, not role-driven access

Every access decision — by a human or an AI agent — is evaluated against a live policy at the
time of the request. Policies live in a Policy Administration Point (PAP). Decisions are made by
a Policy Decision Point (PDP). Enforcement happens at a Policy Enforcement Point (PEP) that
intercepts every request before it reaches the data or application. Context is supplied to the
PDP by a Policy Information Point (PIP) — device posture, identity confidence, data sensitivity,
time of day, behaviour history, threat intelligence.

This is the NIST ABAC model, taken seriously. Most organisations have a PEP and a PDP. Very few
have a functioning PAP that manages policy lifecycle, or a PIP that feeds rich context to the
decision engine.

### 2. Adaptive, not static, trust scoring

The key innovation in the Trust Fabric is the Adaptive Trust Engine. Instead of a binary
allow/deny decision, the PDP receives a continuous trust score — a number that reflects the
current risk of granting access.

The score integrates multiple signals:

- Identity confidence (what authentication method was used, was MFA satisfied?)
- Device posture (is the device managed, patched, compliant?)
- Behavioural baseline (is this access pattern consistent with what this identity normally does?)
- Data sensitivity (what classification is the target data?)
- Contextual signals (time of day, geographic location, prior actions in the session)
- Threat intelligence (are there active indicators of compromise for this identity or device?)

A high trust score produces a normal allow decision. A borderline score triggers a step-up
authentication challenge. A low score triggers a deny and an alert. The thresholds are
configurable per data classification and action type.

This means the same identity gets different levels of access under different conditions — which
is how real-world risk actually works.

### 3. AI agent identity as a first-class citizen

In most enterprise architectures, AI agents either impersonate users (inheriting their credentials
and permissions) or operate as service accounts with static, over-provisioned access.

Neither is acceptable in a high-sensitivity environment.

In the Trust Fabric, AI agents have their own workload identity — credentials tied to the agent,
not the user or the service account. Every action an agent takes is attributed to that agent
identity. The PDP evaluates agent requests using the same adaptive scoring as human requests,
with additional signals specific to AI agents: which tools has this agent called in this session,
does the combination of tool calls suggest unexpected behaviour, does the agent's request pattern
match its declared purpose?

This makes AI agent actions distinguishable from human actions in the audit log — which is
essential for compliance and incident investigation.

### 4. Explainability wired into every decision

The Trust Fabric requires that every access decision — especially those made with AI involvement
— carries a traceable rationale. Which policy matched. Which trust signals were considered. What
score was computed. What the outcome was.

This is not just good security practice. In regulated industries, it is becoming a compliance
requirement. AI governance frameworks increasingly demand that decisions affecting sensitive data
be explainable, not just defensible in principle.

## What This Looks Like in Practice

When I implemented this architecture for a national-scale insurance ecosystem, the deployment
covered multiple insurance verticals — life, health, motor, and property & casualty — with a
hybrid infrastructure spanning on-premises data centres and cloud-hosted application tiers.

The identity layer combined an enterprise identity provider with on-premises directory services,
federated through an OAuth 2.0/OIDC flow, with multi-factor authentication enforced at every
external access point. Zero Trust Network Access (ZTNA) replaced traditional VPN, meaning network
access was scoped to specific applications — not the entire network.

The PEP was deployed as an API gateway intercept layer, meaning every API call — whether from a
human-facing portal or an AI agent's tool call — passed through the enforcement point. The PDP
evaluated requests in real-time, with the PIP aggregating live signals from the SIEM, the identity
provider, the device management layer, and the data classification system.

The Adaptive Trust Engine computed trust scores from this signal feed. Scores were cached for
short windows — seconds, not minutes — to balance latency against freshness. High-sensitivity
decisions, particularly those involving AI agents accessing bulk data, triggered human-in-the-loop
approval flows before execution.

Data was protected in layers: application-layer encryption for PII fields, transparent data
encryption for structured databases, block-level encryption for storage arrays, and a centralised
key management system, with modern TLS enforced across all API and replication traffic.

Threat intelligence fed into the PIP continuously, meaning a new indicator of compromise affecting
an identity or device would propagate into trust score calculations within minutes — dynamically
reducing access without waiting for a policy update or a manual revocation.

## The AI Governance Layer

The Trust Fabric is not only about access control. It also includes what I call the AI Governance
Layer: controls that operate above the access decision, on the AI agent's behaviour itself.

This layer enforces:

- **Rate limiting per agent** — an AI agent should not be able to make unlimited tool calls in
  a session. Rate limits are configurable per agent identity and per tool.
- **Action scope enforcement** — agents can only call tools within their declared capability
  scope. An agent designed for policy analysis cannot call data export tools.
- **Prompt injection detection** — inbound user inputs that attempt to override system
  instructions are flagged and blocked.
- **Decision audit trail** — every agent turn, tool call, input, and output is logged with
  the agent's identity, timestamp, and the trust context at the time of execution.
- **Human escalation** — for actions above a configurable risk threshold, the agent pauses
  and requests human approval before proceeding.

The combination of Zero Trust at the access layer and AI governance above it is what makes the
system robust. Zero Trust ensures no unauthorised access. The AI governance layer ensures that
authorised AI agents behave within the boundaries of their intent.

## Lessons From National-Scale Implementation

**Zero Trust fails without a functioning PIP.** The most common enterprise Zero Trust
implementation has a PEP (the firewall or API gateway) and a basic PDP (the identity provider).
What it lacks is a PIP that delivers rich, real-time context. Without behavioural signals and
threat intelligence feeding the PDP, trust scoring degrades to little more than identity
verification. That's necessary, but not sufficient.

**AI agents need a different trust model than users.** Human access patterns are relatively
predictable. AI agents can make hundreds of tool calls per minute, in patterns no human would
generate. Applying human-designed access controls directly to AI agents produces either
over-restriction (agents can't do their job) or under-restriction (agents have too much latitude).
The agent-specific behavioural baseline is what makes adaptive scoring work for AI.

**Explainability is an operational requirement, not just a compliance one.** When an AI agent's
access is denied at 2am and an alarm fires, the security team needs to understand immediately why
the trust score dropped and what triggered it. A system that makes good decisions but cannot
explain them creates operational overhead. Wiring explainability into the decision layer — not
as an afterthought — was one of the most practically valuable design choices.

**Policy lifecycle matters as much as policy enforcement.** The most sophisticated PDP in the
world is only as good as the policies in the PAP. Policies that are authored once and never
reviewed become stale. Building a policy review cadence — and treating the PAP as a governed,
versioned system rather than a configuration file — is the operational discipline that sustains
the architecture over time.

## Conclusion

The AI Trust Fabric is my answer to a question that most enterprise security teams have not yet
fully confronted: *what does Zero Trust look like when AI agents are the primary actors in your
system?*

The pattern — policy-driven access, adaptive trust scoring, AI agent identity, and explainable
decisions — applies beyond insurance. Any regulated industry handling sensitive data, deploying
AI agents with access to that data, and needing to demonstrate governance to regulators will face
the same architectural challenges.

The core insight is simple: trust is not binary, and it should not be static. An architecture
that reflects this — that computes trust continuously, adapts to context, and attributes every
action to an accountable identity — is more resilient, more auditable, and more honest about
the risk environment we actually operate in.

---

*This architecture is the basis of [Registered Design No. 485611-001](/publications/)
(Government of India). Related: [MCP Guardian: A Security-First Layer for Safeguarding MCP-Based
AI Systems](/publications/) (CS & IT, 2025).*
