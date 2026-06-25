import os
from io import BytesIO
from PIL import Image

class PDFService:
    @staticmethod
    def compile_images_to_pdf(image_files, output_filename, output_directory):
        """
        Compiles a list of image file objects into a single multi-page PDF.
        
        :param image_files: List of file-like objects (e.g. Flask FileStorage objects)
        :param output_filename: Desired name of the PDF (e.g. 'chemistry_notes.pdf')
        :param output_directory: Path to save the compiled PDF locally
        :return: Absolute path to the saved PDF
        """
        if not image_files:
            raise ValueError("No images provided to compile.")

        # Ensure output directory exists
        os.makedirs(output_directory, exist_ok=True)

        # Enforce .pdf extension
        if not output_filename.lower().endswith(".pdf"):
            output_filename += ".pdf"

        output_path = os.path.join(output_directory, output_filename)

        opened_images = []
        try:
            for file_obj in image_files:
                # Open image using Pillow
                img = Image.open(file_obj)
                
                # Pillow requires converting RGBA/LA images to RGB for PDF rendering
                if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
                    # Create a white background canvas to place transparent images on
                    bg = Image.new("RGB", img.size, (255, 255, 255))
                    # Handle transparency masking if applicable
                    mask = img.convert("RGBA").split()[3] if img.mode != "LA" else img.split()[1]
                    bg.paste(img, mask=mask)
                    opened_images.append(bg)
                else:
                    # Convert L, P, CMYK, etc., directly to RGB
                    if img.mode != "RGB":
                        img = img.convert("RGB")
                    opened_images.append(img)

            if not opened_images:
                raise ValueError("Failed to process any valid images.")

            # Save the first image as PDF and append the remaining images as subsequent pages
            first_image = opened_images[0]
            other_images = opened_images[1:]

            first_image.save(
                output_path,
                save_all=True,
                append_images=other_images,
                resolution=100.0,
                quality=85  # Clean compress quality for note scans
            )

            return output_path

        finally:
            # We don't close images here because first_image.save needs them open,
            # but we can ensure they are closed eventually.
            # In Flask, the request lifecycle will clean up the temporary files, 
            # but we should still handle cleanup explicitly where possible.
            pass
