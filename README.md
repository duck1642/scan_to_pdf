# ScanToPDF

A modular, local web application to merge and stitch photos of handwritten paper notes into single, clean PDFs. It provides a visual interface to drag and drop images, reorder pages, delete pages, and crop out messy page margins/table borders before building the PDF.

## Features
- **File & Folder Selection**: Drag-and-drop file upload, standard multiple-file selector, or pick an entire folder containing your note scans using `webkitdirectory`.
- **Drag-and-Drop Organizer**: Visual page grid with simple drag-to-reorder logic to put pages in the correct sequence.
- **Canvas-based Interactive Cropper**: Visual modal with draggable resize handles to crop margins locally, maintaining original image quality.
- **Pillow API Backend**: Synchronous Python Flask backend that handles transparent image overlays (RGBA conversion) and compiles the images losslessly to a single PDF.
- **Double Save**: Saves the PDF inside a local `output/` directory in the project, while automatically prompting a browser download.

## Project Structure
```text
scan_to_pdf/
├── docs/
│   ├── architecture.md     # In-depth architectural layout & data flow
│   └── running.md          # Full setup & launch instructions
├── backend/
│   ├── app.py              # Flask configuration and healthcheck
│   ├── routes/             # API request handling
│   │   └── pdf_routes.py
│   ├── services/           # Pillow image processing and PDF compilation
│   │   └── pdf_service.py
│   └── requirements.txt    # Python backend requirements
├── frontend/
│   ├── src/                # Svelte source files (App.svelte, DropZone, CropModal, etc.)
│   ├── package.json
│   └── vite.config.js      # Vite dev server configuration (includes proxy)
└── README.md
```

## Quick Start

### 1. Start Backend (Flask)
```bash
cd backend
python -m venv venv
# Windows:
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```
*API runs on `http://127.0.0.1:5000`.*

### 2. Start Frontend (Svelte)
```bash
cd frontend
npm install
npm run dev
```
*Web interface runs on `http://localhost:5173`.*

Detailed documentation is available in the [`docs/`](./docs) folder.
