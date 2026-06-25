import os
from flask import Blueprint, request, jsonify, send_file
from services.pdf_service import PDFService

pdf_bp = Blueprint("pdf", __name__)

# Base output directory: F:\ARCHIVE\main\software\python\snippets\scan_to_pdf\output
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(os.path.dirname(BASE_DIR), "output")

@pdf_bp.route("/merge", methods=["POST"])
def merge_images():
    """
    Accepts an ordered list of images and merges them into a single PDF.
    Expects:
      - Form field 'images': array of files (appended sequentially on frontend)
      - Form field 'output_name': string (the desired name of the PDF)
    """
    try:
        # 1. Extract and validate output name
        output_name = request.form.get("output_name", "compiled_notes").strip()
        if not output_name:
            output_name = "compiled_notes"

        # 2. Extract and validate uploaded files
        uploaded_files = request.files.getlist("images")
        if not uploaded_files or len(uploaded_files) == 0:
            return jsonify({"error": "No images were received. Please select or drag images."}), 400

        # 3. Compile images to PDF using service layer
        pdf_path = PDFService.compile_images_to_pdf(
            image_files=uploaded_files,
            output_filename=output_name,
            output_directory=OUTPUT_DIR
        )

        # 4. Return the compiled PDF as a download
        return send_file(
            pdf_path,
            mimetype="application/pdf",
            as_attachment=True,
            download_name=os.path.basename(pdf_path)
        )

    except Exception as e:
        # Handle exceptions gracefully
        return jsonify({"error": f"An error occurred while compiling the PDF: {str(e)}"}), 500
