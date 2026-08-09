"""
Healthcare Document Engine API.

Run from the project root:
    uvicorn api.main:app --reload --port 8000
"""

from __future__ import annotations

import asyncio
import logging
import time
import json
import os
import uuid
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from framework.agents.clinical.clinical_summary_agent import ClinicalSummaryAgent
from framework.agents.document.document_structure_agent import DocumentStructureAgent
from framework.agents.entity.entity_extraction_agent import EntityExtractionAgent
from framework.agents.entity.entity_normalization_agent import EntityNormalizationAgent
from framework.agents.entity.entity_validation_agent import EntityValidationAgent
from framework.agents.relation.relation_extraction_agent import RelationExtractionAgent
from framework.agents.relation.relation_normalization_agent import RelationNormalizationAgent
from framework.agents.relation.relation_validation_agent import RelationValidationAgent
from framework.agents.report.final_report_agent import FinalReportAgent

from framework.orchestrator.healthcare_orchestrator import HealthcareOrchestrator
from framework.prompts.prompt_registry import PromptRegistry
from framework.prompts.document_structure_prompt import DocumentStructurePrompt
from framework.prompts.entity_extraction_prompt import EntityExtractionPrompt
from framework.prompts.entity_normalization_prompt import EntityNormalizationPrompt
from framework.prompts.entity_validation_prompt import EntityValidationPrompt
from framework.prompts.relation_extraction_prompt import RelationExtractionPrompt
from framework.prompts.relation_normalization_prompt import RelationNormalizationPrompt
from framework.prompts.relation_validation_prompt import RelationValidationPrompt
from framework.prompts.clinical_summary_prompt import ClinicalSummaryPrompt
from framework.prompts.final_report_prompt import FinalReportPrompt

from framework.providers.openrouter_provider import OpenRouterProvider
from framework.registry.agent_registry import AgentRegistry
from framework.registry.provider_registry import ProviderRegistry
from framework.router.model_router import ModelRouter

from framework.state.workflow_state import WorkflowState
from framework.state.execution_state import ExecutionState
from framework.state.document_state import DocumentState, PageState
from framework.state.layout_state import LayoutState
from framework.state.entity_state import EntityState
from framework.state.validation_state import ValidationState
from framework.state.model_state import ModelState
from framework.state.metrics_state import MetricsState
from framework.state.clinical_summary_state import ClinicalSummaryState

from api.logging_config import configure_logging, APP_LOG, ERROR_LOG

logger = configure_logging()


app = FastAPI(
    title="Healthcare Document Engine",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_orchestrator: HealthcareOrchestrator | None = None
_provider: OpenRouterProvider | None = None


class ProcessTextRequest(BaseModel):
    text: str
    file_name: str = "clinical_document.txt"
    document_id: str | None = None


def _register_prompts() -> PromptRegistry:
    registry = PromptRegistry()

    registry.register("document_structure", DocumentStructurePrompt())
    registry.register("entity_extraction", EntityExtractionPrompt())
    registry.register("entity_normalization", EntityNormalizationPrompt())
    registry.register("entity_validation", EntityValidationPrompt())
    registry.register("relation_extraction", RelationExtractionPrompt())
    registry.register("relation_normalization", RelationNormalizationPrompt())
    registry.register("relation_validation", RelationValidationPrompt())
    registry.register("clinical_summary", ClinicalSummaryPrompt())
    registry.register("final_report", FinalReportPrompt())

    return registry


def _build_agent_registry(router: ModelRouter, prompts: PromptRegistry) -> AgentRegistry:
    registry = AgentRegistry()

    registry.register(
        "document_structure",
        DocumentStructureAgent(router, prompts),
    )
    registry.register(
        "entity_extraction",
        EntityExtractionAgent(router, prompts),
    )
    registry.register(
        "entity_normalization",
        EntityNormalizationAgent(router, prompts),
    )
    registry.register(
        "entity_validation",
        EntityValidationAgent(router, prompts),
    )
    registry.register(
        "relation_extraction",
        RelationExtractionAgent(router),
    )
    registry.register(
        "relation_normalization",
        RelationNormalizationAgent(router, prompts),
    )
    registry.register(
        "relation_validation",
        RelationValidationAgent(router, prompts),
    )
    registry.register(
        "clinical_summary",
        ClinicalSummaryAgent(router, prompts),
    )
    registry.register(
        "final_report",
        FinalReportAgent(router, prompts),
    )

    # BaseAgent/BaseComponent expose a logger slot. Inject named loggers so
    # the existing agent lifecycle logs are written to the central log file.
    for name, agent in registry.items():
        agent.logger = logging.getLogger(f"healthcare.agent.{name}")

    return registry


def _build_state(
    text: str,
    file_name: str,
    document_id: str,
) -> WorkflowState:
    return WorkflowState(
        execution=ExecutionState(
            run_id=str(uuid.uuid4()),
            workflow_id="healthcare-document-workflow",
        ),
        document=DocumentState(
            document_id=document_id,
            file_name=file_name,
            file_path="ui-upload",
            file_type=Path(file_name).suffix.lstrip(".") or "txt",
            pages=[
                PageState(
                    page_number=1,
                    content=text,
                )
            ],
            metadata={
                "source": "healthcare-document-engine-ui",
            },
        ),
        layout=LayoutState(),
        entities=EntityState(),
        validation=ValidationState(),
        clinical_summary=ClinicalSummaryState(),
        model=ModelState(),
        metrics=MetricsState(),
    )


def _serialize_state(state: WorkflowState) -> dict[str, Any]:
    data = state.model_dump(mode="json")

    # Keep the API response useful and avoid returning the full source text
    # twice in the browser response.
    if "document" in data:
        document = data["document"]
        for page in document.get("pages", []):
            if len(page.get("content", "")) > 5000:
                page["content"] = page["content"][:5000] + "\n...[truncated]"

    return data


async def _run(text: str, file_name: str, document_id: str | None = None):
    global _orchestrator

    if _orchestrator is None:
        raise RuntimeError("API application has not been initialized.")

    run_id = document_id or str(uuid.uuid4())
    state = _build_state(
        text=text,
        file_name=file_name,
        document_id=run_id,
    )
    state.execution.run_id = run_id

    started = time.perf_counter()
    logger.info(
        "Workflow started | run_id=%s | file=%s | chars=%d",
        run_id, file_name, len(text),
    )

    try:
        result = await _orchestrator.run(state)
    except Exception:
        logger.exception("Workflow failed | run_id=%s | file=%s", run_id, file_name)
        raise

    elapsed = time.perf_counter() - started
    logger.info(
        "Workflow completed | run_id=%s | duration=%.3fs | checkpoint=%s",
        run_id, elapsed, result.checkpoint.stage,
    )
    return _serialize_state(result)


async def _extract_uploaded_text(upload: UploadFile) -> str:
    suffix = Path(upload.filename or "").suffix.lower()
    content = await upload.read()

    if not content:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    if suffix in {".txt", ".md", ".csv"}:
        return content.decode("utf-8", errors="replace")

    if suffix == ".pdf":
        try:
            from pypdf import PdfReader
        except ImportError as exc:
            raise HTTPException(
                status_code=500,
                detail="PDF support requires pypdf. Install it with: pip install pypdf",
            ) from exc

        with NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            tmp.write(content)
            path = tmp.name

        try:
            reader = PdfReader(path)
            return "\n\n".join(
                page.extract_text() or ""
                for page in reader.pages
            )
        finally:
            os.unlink(path)

    if suffix == ".docx":
        try:
            from docx import Document
        except ImportError as exc:
            raise HTTPException(
                status_code=500,
                detail="DOCX support requires python-docx. Install it with: pip install python-docx",
            ) from exc

        with NamedTemporaryFile(suffix=".docx", delete=False) as tmp:
            tmp.write(content)
            path = tmp.name

        try:
            document = Document(path)
            return "\n".join(
                paragraph.text
                for paragraph in document.paragraphs
                if paragraph.text.strip()
            )
        finally:
            os.unlink(path)

    raise HTTPException(
        status_code=400,
        detail="Supported files: .txt, .md, .csv, .pdf, .docx",
    )


@app.on_event("startup")
async def startup() -> None:
    global _orchestrator, _provider

    _provider = OpenRouterProvider()
    _provider.logger = logging.getLogger("healthcare.provider.openrouter")

    provider_registry = ProviderRegistry()
    provider_registry.register("openrouter", _provider)

    router = ModelRouter(provider_registry)
    prompts = _register_prompts()
    agents = _build_agent_registry(router, prompts)

    _orchestrator = HealthcareOrchestrator(
        agent_registry=agents,
        provider_registry=provider_registry,
    )

    await _orchestrator.initialize()
    logger.info("Healthcare API initialized | agents=%s", _orchestrator.agent_registry.list())


@app.on_event("shutdown")
async def shutdown() -> None:
    global _orchestrator, _provider

    if _orchestrator is not None:
        await _orchestrator.shutdown()
        _orchestrator = None

    if _provider is not None:
        await _provider.disconnect()
        _provider = None

    logger.info("Healthcare API shutdown completed")


@app.get("/health")
async def health():
    if _provider is None:
        return {"status": "starting"}

    return {
        "status": "ok",
        "provider": "openrouter",
        "provider_health": await _provider.health_check(),
    }


@app.get("/workflow")
async def workflow():
    if _orchestrator is None or _orchestrator.workflow is None:
        raise HTTPException(status_code=503, detail="Workflow is not initialized.")

    return {
        "workflow": [
            "document_structure",
            "entity_extraction",
            "entity_normalization",
            "entity_validation",
            "relation_extraction",
            "relation_normalization",
            "relation_validation",
            "clinical_summary",
            "final_report",
        ],
        "agents": _orchestrator.agent_registry.list(),
    }


@app.get("/logs")
async def logs(lines: int = 200):
    """Return the most recent application log lines for the dashboard."""
    lines = max(1, min(lines, 2000))

    if not APP_LOG.exists():
        return {"lines": [], "file": str(APP_LOG)}

    with APP_LOG.open("r", encoding="utf-8", errors="replace") as handle:
        recent = handle.readlines()[-lines:]

    return {"lines": [line.rstrip("\n") for line in recent], "file": str(APP_LOG)}


@app.get("/logs/errors")
async def error_logs(lines: int = 100):
    lines = max(1, min(lines, 1000))

    if not ERROR_LOG.exists():
        return {"lines": [], "file": str(ERROR_LOG)}

    with ERROR_LOG.open("r", encoding="utf-8", errors="replace") as handle:
        recent = handle.readlines()[-lines:]

    return {"lines": [line.rstrip("\n") for line in recent], "file": str(ERROR_LOG)}


@app.post("/process/text")
async def process_text(request: ProcessTextRequest):
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty.")

    logger.info("Text processing request | file=%s", request.file_name)
    try:
        return {
            "status": "completed",
            "result": await _run(
                request.text,
                request.file_name,
                request.document_id,
            ),
        }
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Workflow execution failed: {exc}",
        ) from exc


@app.post("/process/file")
async def process_file(file: UploadFile = File(...)):
    logger.info("File upload received | filename=%s | content_type=%s", file.filename, file.content_type)
    text = await _extract_uploaded_text(file)

    if not text.strip():
        raise HTTPException(
            status_code=400,
            detail="No extractable text was found in the uploaded document.",
        )

    try:
        return {
            "status": "completed",
            "result": await _run(
                text,
                file.filename or "uploaded_document",
            ),
        }
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Workflow execution failed: {exc}",
        ) from exc
