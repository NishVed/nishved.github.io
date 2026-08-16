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

Generic text chunking destroys COBOL: it splits mid-paragraph and mid-COPY statement, and loses
the structure retrieval depends on. So the core of this system is a structure-aware parser that
understands COBOL's divisions and JCL step boundaries, expands COPYBOOKs inline, and tags every
chunk with program, paragraph, and line range — because every answer has to cite exactly where it
came from. A static-analysis dependency graph (CALL statements, COPY references, JCL EXEC PGM=
links) sits alongside the vector index for structural questions like "what does this program call?"

RAG over fine-tuning was the only real option: the source corpus is client-specific, keeps
changing as modernization proceeds, and a fine-tuned model can't cite a specific line of code.
The system exposes its capabilities as MCP tools (`search_code`, `get_dependencies`,
`get_copybook`, `get_impact`) and uses A2A for the RAG agent, dependency-graph agent, and
migration-guidance agent to collaborate.

**My role:** designed the RAG architecture including the parser, chunking strategy, and
dependency-graph extraction; architected the MCP/A2A multi-agent system.

**Stack:** Azure OpenAI, MCP, A2A, custom Python COBOL/JCL parser, FastAPI.
