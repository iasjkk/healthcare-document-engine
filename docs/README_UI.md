# Healthcare Document Engine UI

## 1. Install UI/API dependencies

```powershell
pip install fastapi "uvicorn[standard]" streamlit requests python-multipart pypdf python-docx
```

## 2. Make sure the OpenRouter key exists

```powershell
$env:OPEN_ROUTER_API_KEY="YOUR_KEY"
```

## 3. Start the API

From:

`D:\code\healthcare-document-engine`

run:

```powershell
python -m uvicorn api.main:app --reload --port 8000
```

## 4. Start Streamlit in another terminal

```powershell
streamlit run dashboard\streamlit_app.py
```

Open:

`http://localhost:8501`

## Important

The first UI version intentionally starts from extracted text. For PDF/DOCX it uses `pypdf`/`python-docx` as a lightweight ingestion bridge and then creates the existing `WorkflowState`.

It does not replace your existing parser/extractor architecture. Once the UI is proven end-to-end, the next step is to connect the upload endpoint to your project's ParserRegistry and document-ingestion pipeline.
