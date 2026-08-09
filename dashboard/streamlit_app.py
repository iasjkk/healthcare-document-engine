"""
Healthcare Document Engine Streamlit UI.

Run from the project root:
    streamlit run dashboard/streamlit_app.py
"""

from __future__ import annotations

import json
import os
from typing import Any

import requests
import streamlit as st


API_URL = os.getenv("HEALTHCARE_API_URL", "http://127.0.0.1:8000")


st.set_page_config(
    page_title="Healthcare Document Engine",
    page_icon="🏥",
    layout="wide",
)


WORKFLOW = [
    "document_structure",
    "entity_extraction",
    "entity_normalization",
    "entity_validation",
    "relation_extraction",
    "relation_normalization",
    "relation_validation",
    "clinical_summary",
    "final_report",
]


def api_get(path: str) -> dict[str, Any]:
    response = requests.get(
        f"{API_URL}{path}",
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def fetch_logs(lines: int = 200) -> list[str]:
    data = api_get(f"/logs?lines={lines}")
    return data.get("lines", [])


def api_post_json(path: str, payload: dict[str, Any]) -> dict[str, Any]:
    response = requests.post(
        f"{API_URL}{path}",
        json=payload,
        timeout=600,
    )
    response.raise_for_status()
    return response.json()


def api_post_file(path: str, uploaded_file) -> dict[str, Any]:
    response = requests.post(
        f"{API_URL}{path}",
        files={
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                uploaded_file.type or "application/octet-stream",
            )
        },
        timeout=600,
    )
    response.raise_for_status()
    return response.json()


def render_workflow():
    st.subheader("Workflow")

    cols = st.columns(3)

    for index, stage in enumerate(WORKFLOW):
        with cols[index % 3]:
            st.markdown(
                f"""
                <div style="
                    border:1px solid #334155;
                    border-radius:10px;
                    padding:12px;
                    margin-bottom:10px;
                    background:#0f172a;
                    color:#e2e8f0;
                ">
                    <b>{index + 1}. {stage.replace("_", " ").title()}</b>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_result(result: dict[str, Any]):
    data = result.get("result", result)

    document = data.get("document", {})
    entities = data.get("entities", {}).get("entities", [])
    relations = data.get("relations", {}).get("relations", [])
    layout = data.get("layout", {}).get("nodes", [])
    checkpoint = data.get("checkpoint", {})
    summary = data.get("clinical_summary", {})

    st.success(
        f"Workflow completed — checkpoint: "
        f"{checkpoint.get('stage', 'unknown')}"
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Pages", len(document.get("pages", [])))
    c2.metric("Layout Nodes", len(layout))
    c3.metric("Entities", len(entities))
    c4.metric("Relations", len(relations))

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "Clinical Summary",
            "Entities",
            "Relations",
            "Layout",
            "Raw State",
        ]
    )

    with tab1:
        metadata = summary.get("metadata", {})
        if metadata:
            st.json(metadata)
        else:
            st.info("No clinical summary metadata returned.")

    with tab2:
        if entities:
            st.dataframe(
                [
                    {
                        "ID": e.get("entity_id"),
                        "Type": e.get("entity_type"),
                        "Value": e.get("value"),
                        "Normalized": e.get("normalized_value"),
                        "Confidence": e.get("confidence"),
                        "Page": e.get("page_number"),
                    }
                    for e in entities
                ],
                use_container_width=True,
            )
        else:
            st.info("No entities were returned.")

    with tab3:
        if relations:
            st.dataframe(
                [
                    {
                        "ID": r.get("relation_id"),
                        "Source": r.get("source_entity_id"),
                        "Target": r.get("target_entity_id"),
                        "Type": r.get("relation_type"),
                        "Confidence": r.get("confidence"),
                    }
                    for r in relations
                ],
                use_container_width=True,
            )
        else:
            st.info("No relations were returned.")

    with tab4:
        if layout:
            st.dataframe(
                [
                    {
                        "Node": n.get("node_id"),
                        "Type": n.get("layout_type"),
                        "Page": n.get("page_number"),
                        "Text": n.get("text"),
                    }
                    for n in layout
                ],
                use_container_width=True,
            )
        else:
            st.info("No layout nodes were returned.")

    with tab5:
        st.json(data)


st.title("🏥 Healthcare Document Engine")
st.caption(
    "Document → Structure → Entities → Relations → Clinical Summary → Final Report"
)

with st.sidebar:
    st.header("System")
    st.code(API_URL)

    if st.button("Check API"):
        try:
            health = api_get("/health")
            st.success(health.get("status", "unknown"))
            st.json(health)
        except Exception as exc:
            st.error(str(exc))

    st.divider()
    st.markdown("### Logs")
    if st.button("Refresh Logs"):
        try:
            st.session_state["logs"] = fetch_logs(300)
            st.success("Logs refreshed")
        except Exception as exc:
            st.error(str(exc))

    st.divider()
    st.markdown("### Pipeline")
    for i, stage in enumerate(WORKFLOW, 1):
        st.write(f"{i}. {stage}")

render_workflow()

with st.expander("📋 Application Logs", expanded=True):
    try:
        current_logs = fetch_logs(200)
        if current_logs:
            st.code("\n".join(current_logs), language="text")
        else:
            st.info("No logs yet. Start the API and process a document.")
    except Exception as exc:
        st.warning(f"Unable to read logs: {exc}")

st.divider()

input_tab, upload_tab = st.tabs(["Paste Clinical Text", "Upload Document"])

with input_tab:
    text = st.text_area(
        "Clinical document",
        height=320,
        placeholder=(
            "Paste a clinical report here...\n\n"
            "Example:\n"
            "Diagnosis: Type 2 Diabetes Mellitus\n"
            "Medication: Metformin 500mg twice daily\n"
            "HbA1c: 7.2%"
        ),
    )

    if st.button(
        "🚀 Run Complete Workflow",
        type="primary",
        disabled=not bool(text.strip()),
    ):
        with st.spinner("Running all workflow agents..."):
            try:
                result = api_post_json(
                    "/process/text",
                    {
                        "text": text,
                        "file_name": "streamlit_clinical_document.txt",
                    },
                )
                st.session_state["last_result"] = result
            except requests.HTTPError as exc:
                try:
                    st.error(exc.response.json())
                except Exception:
                    st.error(str(exc))
            except Exception as exc:
                st.error(str(exc))

with upload_tab:
    uploaded = st.file_uploader(
        "Upload clinical document",
        type=["txt", "md", "csv", "pdf", "docx"],
    )

    if st.button(
        "📄 Process Uploaded Document",
        type="primary",
        disabled=uploaded is None,
    ):
        with st.spinner("Extracting document and running all agents..."):
            try:
                result = api_post_file(
                    "/process/file",
                    uploaded,
                )
                st.session_state["last_result"] = result
            except requests.HTTPError as exc:
                try:
                    st.error(exc.response.json())
                except Exception:
                    st.error(str(exc))
            except Exception as exc:
                st.error(str(exc))

if "last_result" in st.session_state:
    st.divider()
    render_result(st.session_state["last_result"])
