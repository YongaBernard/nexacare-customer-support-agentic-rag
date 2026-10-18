# AI Risk Register

## Customer Support Agentic RAG System

| ID | Risk | Category | Likelihood | Impact | Risk Level | Control / Mitigation | Owner |
|---|---|---|---|---|---|---|---|
| R001 | AI generates unsupported or incorrect information | AI Quality | Medium | High | High | RAG grounding, source retrieval, confidence checks, escalation | AI System Owner |
| R002 | AI exposes customer PII | Privacy | Medium | High | High | Data minimization, PII detection, secure logging, access controls | Security Owner |
| R003 | AI provides an inappropriate response to a sensitive customer issue | Safety | Medium | High | High | Safety rules, sentiment/urgency detection, human escalation | AI System Owner |
| R004 | Outdated knowledge-base information is retrieved | Data Governance | Medium | Medium | Medium | Document ownership, versioning, review schedule, metadata | Knowledge Owner |
| R005 | Unauthorized user accesses restricted functionality | Security | Low | High | Medium | Authentication, authorization, least privilege | Security Owner |
| R006 | API keys or secrets are exposed | Security | Low | Critical | High | Environment variables, .gitignore, secret management | Engineering Owner |
| R007 | AI fails to escalate a high-risk customer request | Human Oversight | Medium | High | High | Explicit escalation rules and automated escalation node | AI System Owner |
| R008 | Excessive logging exposes sensitive customer information | Privacy | Medium | High | High | Log sanitization, data minimization, retention controls | Security Owner |
| R009 | Prompt injection manipulates the AI agent | AI Security | Medium | High | High | Input validation, instruction hierarchy, retrieval isolation, testing | AI Security Owner |
| R010 | Retrieval returns irrelevant documents | RAG Quality | Medium | Medium | Medium | Retrieval evaluation, chunking optimization, metadata filtering | AI System Owner |
| R011 | AI produces biased or discriminatory responses | Responsible AI | Low | High | Medium | Fairness testing, evaluation datasets, monitoring | Responsible AI Owner |
| R012 | System becomes unavailable | Availability | Low | High | Medium | Health checks, error handling, monitoring, fallback responses | Engineering Owner |
| R013 | AI model or prompt changes reduce system performance | Change Management | Medium | Medium | Medium | Version control, regression testing, evaluation before deployment | Engineering Owner |
| R014 | Customer receives an answer outside the AI's authority | Governance | Medium | High | High | Scope restrictions, tool permissions, human escalation | AI System Owner |
| R015 | Lack of audit evidence for AI decisions | Governance | Medium | Medium | Medium | Structured audit logging and traceability | Compliance Owner |

---

## Risk Classification

### Low

Risks that are unlikely to cause significant customer, operational, privacy, or regulatory impact.

### Medium

Risks that could cause meaningful operational or customer impact and require monitoring and mitigation.

### High

Risks that could cause significant customer harm, privacy violations, security incidents, regulatory concerns, or major operational impact.

### Critical

Risks that could result in severe consequences and require immediate controls and escalation.

---

## Risk Treatment Principles

The system should use the following treatment strategies:

### Avoid

Do not allow the AI system to perform activities outside its approved authority.

### Mitigate

Implement technical and procedural controls to reduce the likelihood or impact of a risk.

### Transfer

Where appropriate, responsibility may be transferred through approved third-party services, contracts, or operational processes.

### Accept

Low-level residual risks may be accepted when documented and approved by the appropriate system owner.

---

## Risk Review

The risk register should be reviewed:

- Before production deployment
- After major architecture changes
- After model or prompt changes
- After significant incidents
- When new data sources are introduced
- During periodic governance reviews

New risks identified during system evaluation or production monitoring should be added to this register.