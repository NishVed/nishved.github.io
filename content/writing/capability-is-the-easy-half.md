---
title: "Capability Is the Easy Half"
date: 2026-08-25
description: "Platform architectures for AI describe how a system does more. Almost none describe what it is permitted to do. Here is the second half — a reference architecture for the control plane of an agent platform, built along the axis of authority rather than capability."
tags: ["Agentic AI", "AI Governance", "Zero Trust", "Enterprise Security", "Platform Architecture"]
ShowToc: true
TocOpen: false
---

There is a genre of architecture writing I have learned a lot from: the reference architecture for
an AI platform. Retrieval, then guardrails, then a model gateway, then caching, then write actions.
Each layer lets the system do more than the last.

I want to describe the other half, because in the enterprise systems I work on, it is the half that
decides whether anything ships.

**Every one of those architectures builds along a capability axis. Almost none of them build along
an authority axis.** They answer *how does the system produce a better output*. They do not answer
*what is this specific output permitted to do, on whose behalf, and who carries it if it is wrong*.

That second question is not a compliance chore bolted on at the end. It has its own architecture,
its own layers, and its own failure modes — and in a regulated enterprise it is load-bearing in a
way that a better retrieval strategy is not. A system that is slightly worse at answering but
provably bounded gets deployed. A system that is brilliant and unbounded goes to a steering
committee and dies there.

So: a reference architecture for the control plane. Six layers, in dependency order, because each
one is meaningless without the one beneath it.

{{< control-plane >}}

## 1. Identity is resolved, never asserted

The bottom layer is not authentication. It is the narrower question of *how the identity of the
caller reaches the agent*.

There is a failure mode I have seen often enough to consider it the default: the calling user's
identity arrives as part of the conversation. Sometimes explicitly — a user ID passed in the
request body, or worse, interpolated into a system prompt. Sometimes implicitly, where the agent
infers who it is acting for from what the conversation has said so far.

**An identity carried in context is an identity an attacker can write.** Anything inside the model's
context window is data, and data can be influenced — by the user, by a retrieved document, by a
tool result. Prompt injection is usually discussed as a way to make a model misbehave. The more
serious version is making a model misbehave *as somebody else*.

The rule is simple and absolute: the identity of the invoking actor is resolved from trusted
server-side state — a session, a validated token — and travels with the request as structured
metadata that the model can neither see nor alter. The agent does not learn who it is acting for.
It is *told*, by something the model has no access to.

**Don't over-engineer this when** the agent has no write path and reads only public data. The cost
lands on you as an extra hop; the benefit is zero until the agent can touch something that differs
per user.

## 2. The agent's ceiling is the caller's ceiling

Once identity is structural, authorization becomes statable in one sentence: **an agent may never
exceed the authorization scope of the actor that invoked it.**

This sounds obvious. It is routinely violated, and the violation is architectural rather than
careless. Agents need broad access to be useful, so they get a service account. The service account
needs to serve every user, so it accumulates the union of everyone's permissions. Now every user,
through the agent, has an effective permission set that is the union of the whole organisation's —
mediated only by the model's willingness to refuse.

**A model's refusal is not an access control.** It is a probabilistic preference expressed in
natural language, and it is exactly the surface that adversarial input is best at moving.

There are two structural fixes and you want both. The agent holds its own workload identity — it is
a first-class principal in your IAM, not a borrowed human — so its actions are distinguishable in
an audit trail. And every downstream call is made *on behalf of* the invoking actor, with that
actor's scope, so the intersection of the two is the effective permission.

Where the data layer supports it, push the check below the application entirely. Row-level security
enforced in the data tier survives a forgotten predicate in application code; a `WHERE tenant_id =`
does not. **The difference matters because one of those failure modes is a bug and the other is a
silent cross-tenant leak that code review cannot make impossible.**

## 3. The tool surface is an allowlist, not a filter

Agents act through tools. The tool surface is therefore the actual attack surface, and it should be
constructed per invocation rather than filtered at execution time.

The distinction is not pedantic. If the agent can see every tool and you check permissions when it
calls one, then the model's plan can reference tools it may not use, the failure arrives late as a
denial, and the model will often route around it — retrying, rephrasing, decomposing the task into
steps that individually pass. **You have turned an authorization boundary into an optimisation
problem, and you have given the optimiser a lot of attempts.**

If instead the tool registry returns only what this actor, in this context, may call, then the
unauthorised action is not refused. It is *unrepresentable*. There is nothing to route around.

This also constrains something people underestimate: the number of tools. A large surface degrades
planning quality independently of security. Narrow it for authorization and you often get better
behaviour for free.

## 4. The policy decision is not a boolean

Above access sits the decision layer, and this is where most implementations flatten something
continuous into a flag.

Structuring it as separate concerns is old, well-specified, and still the right answer. Policy
administration — where rules are authored, versioned and owned. Policy decision — where a request
is evaluated. Policy enforcement — where the verdict is applied, ideally as an intercept every call
traverses rather than a library each service remembers to invoke. Policy information — the context
the decision draws on: identity confidence, device posture, data classification, time, session
history.

The reason to separate them is not architectural tidiness. It is that **the people accountable for
a policy are almost never the people who can deploy code.** If a rule lives in a conditional inside
a service, then changing it is a release, and the compliance officer who owns the rule cannot
exercise the thing they are accountable for. Policy as versioned, inspectable, separately-owned
artefact is what makes accountability real rather than nominal.

And the decision itself should be continuous rather than binary. A request carries a trust score
assembled from those signals, and the score maps to an outcome — allow, step up authentication,
deny. Binary allow/deny forces every threshold to be set for the worst case, which makes the system
either useless or permissive.

**Don't build this when** you have one class of user and one class of data. A trust engine over a
single-tenant internal tool is ceremony, and ceremony that buys nothing is removed by the first
engineer under deadline pressure.

## 5. Disposition: what happens to the output

Everything so far governs whether the agent may *act*. This layer governs what the system does with
what the agent *produced* — and it is the layer that is almost always missing.

An agent emits a claim. Something then has to decide whether that claim becomes information, a
recommendation, a tracked task, an executed action, or a human review item. In most systems that
decision was made once, at design time, as a boolean: this agent writes to the system of record, or
it does not.

I have written about this at length in
[Autonomy Is a Dial, Not a Switch](/writing/autonomy-is-a-dial-not-a-switch/), so I will state only
the architectural consequence here. **The disposition of an output is a runtime decision with four
inputs, not a design-time flag with one.** Confidence, the invoking actor's authority, the risk of
the action, and segregation-of-duties rules — the same claim at the same confidence resolves
differently depending on who asked and what it would touch.

A reference implementation of the resolver, with tests, is in
[agent-governance-patterns](https://github.com/NishVed/agent-governance-patterns).

## 6. Evidence, and the refusal to be silent

The top layer is what you can prove afterwards, and it has two halves that are usually conflated.

**Traceability** is the ability to say which component produced a given output. One correlation
identifier propagated across every agent hop, tool call and model invocation, landing in one
collector. Without it you cannot distinguish a routing failure from a retrieval failure from a
generation failure, and you will spend your incidents arguing about which team owns the bug.

**Rationale** is the ability to say *why* a decision went the way it did: which policy matched,
which trust signals fired, which model version produced the claim, what evidence it cited. This is
what makes an AI-assisted decision defensible under audit. A correct decision you cannot explain is
indistinguishable, to a regulator, from a lucky one.

Then one rule that does more work than the rest of this section combined: **an ambiguous or failed
evaluation must surface as a visible exception, never as silent continuation.**

Silent continuation is worse than a crash, because a crash is noticed. A validation pass that
quietly skipped the rule it could not evaluate produces a clean-looking report with a hole in it,
and the hole is found — if it is found — by an auditor, months later, at maximum cost. Downstream,
an omission and a pass are byte-identical. So a system that evaluates rules answers *every* rule on
*every* run, including "cannot check", and refuses to render a verdict while anything is
unresolved.

## Autonomy as configuration, not architecture

One consequence runs across all six layers and is worth stating separately, because it determines
whether any of this survives contact with a customer.

Thresholds belong in tenant configuration, not in code. A cautious customer starts advisory across
the board. As outcomes accumulate, they widen policy for the narrow, low-risk, high-volume
decisions where the system has demonstrably been right, and keep everything material on approval.
Nobody forks the product. Nobody ships a release. **The dial moves because the evidence moved.**

Build it the other way — autonomy level as an architectural property — and every customer with a
different risk appetite becomes a different deployment, and you are maintaining a distribution
rather than a product.

## What this costs

I would rather state the bill than pretend there isn't one.

Every layer here is latency and complexity. An identity resolution hop, a policy decision, a
per-invocation tool registry construction, a disposition resolution, a trace write. On a
conversational path, that is real, and users notice.

It also front-loads work. None of this makes the demo better. A demo has one user, no tenants, no
audit, and a friendly prompt — and the whole control plane is invisible in it. **This architecture
buys you nothing until the moment it is the only reason the system is allowed to run at all.** That
moment usually arrives as a security review, and it arrives late.

And it can be overbuilt. A read-only assistant over public documentation does not need a trust
engine or a disposition ladder. Every pattern here has a scope where it is ceremony rather than
control, and I have tried to say where.

## What I have left out

Deliberately: model evaluation, retrieval quality, prompt engineering, fine-tuning, serving
infrastructure, cost optimisation. Not because they do not matter — they are most of the other
half, and other people write about them better.

Also left out, more honestly: the hard part of layer five. Every disposition decision takes model
confidence as an input, and producing a *calibrated* confidence is an unsolved problem. The
architecture above is correct given a trustworthy confidence signal, and I do not have a good
general answer for how you get one. Where I have needed it, I have leaned on evidence citation and
on running the same input several times and reporting the range rather than the best result — which
is a workaround, not a solution.

That gap is the most interesting open problem in this space, and I would rather name it than let a
clean diagram imply it is solved.
