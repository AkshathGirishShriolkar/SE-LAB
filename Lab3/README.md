# Lab 3 — Component Modelling & Architectural Pattern Selection
**Problem Statement #43 — Feature Flag & Dynamic Config Manager**

## Contents
- `Lab3_Component_Diagram.png` / `.pdf` — UML component diagram (Microservices architecture)
- `Lab3_Justification.docx` / `.pdf` — 1-page architecture justification

## Architecture chosen
**Microservices Architecture** — see `Lab3_Justification.pdf` for the two scenario-based reasons,
the security advantage, and the performance benefit.

## Components identified
1. API Gateway
2. Flag Evaluation Service
3. Config Management Service
4. Real-Time Sync Service
5. Authentication & Access Control Service
6. Audit & Logging Service

(Client SDK and Admin Dashboard are shown as external systems for context.)

## Interfaces shown
`IGatewayAPI`, `IFlagEvaluation`, `IConfigManagement`, `IConfigSnapshot`, `IFlagUpdates`, `IAuth`, `IAuditLog`
