                                      ┌─────────────────────────────┐
                                      │      Streamlit UI           │
                                      │  FastAPI / REST API         │
                                      └─────────────┬───────────────┘
                                                    │
                                                    ▼
                                ┌─────────────────────────────────────┐
                                │      LangGraph Orchestrator         │
                                │ (Workflow + State + Routing)        │
                                └─────────────────────────────────────┘
                                                    │
        ────────────────────────────────────────────┼────────────────────────────────────────────
                                                    │
                                                    ▼
                             ┌─────────────────────────────────────┐
                             │     Document Ingestion Layer        │
                             │ DOCX / XML / HTML / Markdown        │
                             └─────────────────────────────────────┘
                                                    │
                                                    ▼
                             ┌─────────────────────────────────────┐
                             │     Document Parsing Layer          │
                             │ python-docx / lxml / markdown       │
                             └─────────────────────────────────────┘
                                                    │
                                                    ▼
                             ┌─────────────────────────────────────┐
                             │ Canonical Document Object Model     │
                             │           (DOM)                     │
                             └─────────────────────────────────────┘
                                                    │
                                                    ▼
                             ┌─────────────────────────────────────┐
                             │ Layout Analysis Layer               │
                             │ Header/Table/List/Section/etc.      │
                             └─────────────────────────────────────┘
                                                    │
                                                    ▼
                    ┌────────────────────────────────────────────────────────────┐
                    │       Parallel Layout Extraction Agents (LangGraph)        │
                    └────────────────────────────────────────────────────────────┘
                       │          │         │         │          │
                       ▼          ▼         ▼         ▼          ▼
                    Header     Table    Paragraph   Lists    Metadata
                     Agent      Agent      Agent     Agent      Agent
                       │          │         │         │          │
                       └──────────┴─────────┴─────────┴──────────┘
                                                    │
                                                    ▼
                        ┌──────────────────────────────────────────┐
                        │ Named Data Product Builder               │
                        │ (Hierarchy + Reading Order + Context)    │
                        └──────────────────────────────────────────┘
                                                    │
                                                    ▼
                 ┌────────────────────────────────────────────────────────────┐
                 │      AutoGen Clinical Specialist Team                      │
                 └────────────────────────────────────────────────────────────┘
                         │         │          │         │         │
                         ▼         ▼          ▼         ▼         ▼
                     Patient   Diagnosis  Medication  Labs  Timeline
                      Agent      Agent       Agent    Agent    Agent
                         │
                         ▼
                  Terminology Mapping Agent
                 (ICD / SNOMED / LOINC / RxNorm)
                         │
                         ▼
                    Validator Agent
                         │
                         ▼
                  Consensus Agent
                         │
                         ▼
                  JSON Generation Layer
                         │
                         ▼
                 JSON Schema Validation
                         │
                         ▼
                     Storage Layer
               JSON / PostgreSQL / MongoDB
                         │
                         ▼
                  Streamlit Visualization