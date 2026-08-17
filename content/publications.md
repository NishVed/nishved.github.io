---
title: "Publications & IP"
ShowReadingTime: false
ShowWordCount: false
hidemeta: true
ShowShareButtons: false
ShowBreadCrumbs: false
---

Two bodies of work, each with more than one output.

## AI Trust Fabric

The Zero Trust and AI governance architecture I designed for a national-scale insurance data
ecosystem — where the thing requesting access to sensitive records may be an autonomous agent
rather than a person. It produced two things.

### Secure Insurance Data Management Device

**Registered Design No. 485611-001**, Government of India (Designs Act 2000 / Designs Rules
2001, Class 14-02). Co-registered with Krishan Dev Nidumolu and Yoganand Tadepalli.

An industrial design registration — not a patent — covering the secure insurance data management
architecture: Zero Trust principles, adaptive trust evaluation, identity-centric access controls,
and secure data access mechanisms.

<small>The official filing records the name as "Nishant Yeduruvada," a transliteration variant of
Nishanth Veduruvada.</small>

### Building the Trust Fabric: Reinventing National-Scale Insurance Security in the AI Era

*Research paper, in progress.*

The written account of the same architecture — why Zero Trust as most organisations implement it
is binary and static, what has to change when AI agents become the primary actors, and what the
adaptive trust model looks like in practice. The argument is set out in
[this essay](/writing/trust-fabric-zero-trust-ai-era/).

---

## MCP Guardian

### MCP Guardian: A Security-First Layer for Safeguarding MCP-Based AI Systems

*Published in Computer Science & Information Technology (CS&IT), Vol.15 No.9, pp.107–121, 2025.
[DOI: 10.5121/csit.2025.150908](https://doi.org/10.5121/csit.2025.150908)*

A collaborative research paper (eight co-authors, eight companies) proposing a middleware layer
for the Model Context Protocol that adds authentication, per-token rate limiting, WAF-style
scanning for malicious tool calls, and request logging — without requiring changes to individual
MCP tool servers. The paper's own evaluation found the layer successfully blocked destructive
command patterns and unauthorized-token requests, and measured its overhead at roughly 3–4ms
median latency (10–15%) on a reference implementation.
