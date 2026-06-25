# Running scan_to_pdf

Follow these instructions to run the application locally.

## Prerequisites
- **Python 3.8+**
- **Node.js 18+ & npm**

---

## 1. Backend Setup (Flask)

1. Open a terminal and navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows (PowerShell/CMD):
   venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the Flask server:
   ```bash
   python app.py
   ```
   The backend API will run on `http://127.0.0.1:5000`.

---

## 2. Frontend Setup (Svelte + Vite)

1. Open a new terminal and navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install npm packages:
   ```bash
   npm install
   ```
3. Start the Svelte development server:
   ```bash
   npm run dev
   ```
4. Open the application:
   Navigate to the URL displayed in the terminal (usually `http://localhost:5173`).

---

## How to Use the App

1. **Upload Images**: Drag-and-drop your image files (JPG, PNG, WEBP, etc.) into the main dashboard, or use the **Select Files** / **Select Folder** buttons.
2. **Reorder Pages**: Drag any image card and drop it in the desired position to re-order the pages of your PDF.
3. **Crop/Edit**: Hover over any card and click the **Crop** icon. Drag the boundary selection box to crop out unnecessary margins, then click **Save**.
4. **Remove Pages**: Click the **Delete (X)** icon to remove an image from the PDF queue.
5. **Name your PDF**: Type the desired filename in the bottom input field.
6. **Generate PDF**: Click the **Generate PDF** button. The file will be saved in `backend/output/` and downloaded automatically in your browser.
