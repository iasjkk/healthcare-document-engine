                    HealthcareOrchestrator
                             │
                             ▼
                    HealthcareWorkflow
                             │
        ┌────────────────────┴────────────────────┐
        │                                         │
        ▼                                         │
  Entity Pipeline                                 │
        │                                         │
        ├─ entity_extraction                      │
        ├─ entity_normalization                   │
        └─ entity_validation                      │
        │                                         │
        ▼                                         │
  Relation Pipeline                               │
        │                                         │
        ├─ relation_extraction                    │
        ├─ relation_normalization                 │
        └─ relation_validation                    │
        │                                         │
        ▼                                         │
  Clinical Processing                             │
        │                                         │
        ├─ clinical_summary                       │
        └─ final_report                           │
        │                                         │
        ▼                                         │
              WorkflowState                       │
              final_report_completed ◄────────────┘