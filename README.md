# Atlas API

This project is used as a lecture demo for CMPSC 475 at Penn State.

## Run FastAPI Natively

1. Change into the API project directory:
   ```bash
   cd atlas-api
   ```
2. (Optional) Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the API:
   ```bash
   uvicorn api.main:app --host 0.0.0.0 --port 8000
   ```

Open `http://localhost:8000/docs` for the interactive API docs.

## Run with Docker

From the repository root:

1. Build the image:
   ```bash
   docker build -t atlas-api ./atlas-api
   ```
2. Run the container:
   ```bash
   docker run --rm -p 8000:8000 atlas-api
   ```

Open `http://localhost:8000/docs` for the interactive API docs.
