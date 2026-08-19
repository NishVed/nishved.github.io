---
title: "Legacy Code Modernization AI Assistant"
description: "NTT DATA · Syntphony Insurance Cloud Migration · AI Engineer Advisor · Dec 2025 – Present"
weight: 4
hidemeta: true
ShowReadingTime: false
---

Mainframe modernization normally starts with senior COBOL engineers spending weeks manually
reading code to reconstruct business logic and map dependencies — slow, expensive, and
inconsistent, and that expertise is getting scarcer every year. This assistant is part of
[Syntphony Insurance Cloud Migration](https://www.syntphony.com/), where those estates carry
decades of encoded policy and claims logic that has to survive the move to cloud intact.
<!--more-->

Generic text handling destroys COBOL: it splits mid-paragraph and mid-COPY statement and loses
the structure any useful answer depends on. So the core of this system is a structure-aware parser
that understands COBOL's divisions and JCL step boundaries, expands COPYBOOKs inline, and keeps
everything tagged with program, paragraph, and line range — because every answer has to cite
exactly where it came from. A static-analysis dependency graph (CALL statements, COPY references,
JCL EXEC PGM= links) answers the structural questions, like "what does this program call?"

**There is no vector store here, and that is the design.** Rather than embedding the estate and
retrieving by similarity, the codebase is exposed to the model as MCP tools — `search_code`,
`get_dependencies`, `get_copybook`, `get_impact` — which the model calls to fetch exactly the code
it needs and pulls back into its own context. An index would start drifting the moment it was
built, since the corpus is client-specific and changes as modernization proceeds; a tool call
reads the estate as it currently stands. It also makes citation exact rather than probabilistic —
the answer points at the program, paragraph and line the tool actually returned. A2A handles
collaboration between the agents working on top of those tools.

**My role:** designed the code-intelligence architecture — the structure-aware parser, the
dependency-graph extraction, and the MCP tool schemas the model reaches the estate through;
architected the MCP/A2A multi-agent system.

**Stack:** Azure OpenAI, MCP, A2A, custom Python COBOL/JCL parser, FastAPI.
