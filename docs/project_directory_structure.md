healthcare-agentic-ai/
│
├── app/
│
├── api/
│   ├── routes.py
│   ├── schemas.py
│   └── dependencies.py
│
├── config/
│   ├── settings.py
│   ├── models.yaml
│   └── prompts.yaml
│
├── orchestrator/
│   ├── graph.py
│   ├── state.py
│   ├── router.py
│   ├── scheduler.py
│   ├── checkpoints.py
│   └── executor.py
│
├── parsers/
│   ├── docx_parser.py
│   ├── xml_parser.py
│   ├── markdown_parser.py
│   ├── html_parser.py
│   └── parser_factory.py
│
├── dom/
│   ├── document.py
│   ├── page.py
│   ├── section.py
│   ├── paragraph.py
│   ├── table.py
│   ├── list.py
│   ├── metadata.py
│   └── builder.py
│
├── layout/
│   ├── classifier.py
│   ├── hierarchy.py
│   ├── reading_order.py
│   └── relationships.py
│
├── extractors/
│   ├── header/
│   ├── footer/
│   ├── paragraph/
│   ├── table/
│   ├── lists/
│   ├── forms/
│   └── metadata/
│
├── named_data_product/
│   ├── builder.py
│   ├── merger.py
│   ├── validator.py
│   ├── hierarchy.py
│   └── schema.py
│
├── agents/
│
│   ├── autogen_team/
│   │      team.py
│   │
│   ├── patient_agent/
│   ├── diagnosis_agent/
│   ├── medication_agent/
│   ├── procedure_agent/
│   ├── lab_agent/
│   ├── allergy_agent/
│   ├── timeline_agent/
│   ├── terminology_agent/
│   ├── validator_agent/
│   └── consensus_agent/
│
├── llm/
│   ├── registry.py
│   ├── router.py
│   ├── openrouter.py
│   ├── gemma.py
│   ├── gpt.py
│   ├── claude.py
│   ├── llama.py
│   └── deepseek.py
│
├── prompts/
│   ├── planner/
│   ├── diagnosis/
│   ├── medication/
│   ├── validation/
│   └── terminology/
│
├── json_generator/
│   ├── schema.py
│   ├── generator.py
│   └── validator.py
│
├── storage/
│   ├── postgres.py
│   ├── mongodb.py
│   ├── filesystem.py
│   └── versioning.py
│
├── logging/
│   ├── logger.py
│   ├── telemetry.py
│   ├── trace.py
│   ├── replay.py
│   ├── metrics.py
│   └── cost.py
│
├── dashboard/
│   ├── streamlit_app.py
│   ├── pages/
│   ├── components/
│   └── assets/
│
├── tests/
│
├── docs/
│
└── requirements.txt