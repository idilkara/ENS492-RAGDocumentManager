# highlight_pdf_handle.py
import tempfile
import time
import threading
import os
from datetime import datetime, timedelta
import uuid
import fitz
import traceback
from documents import get_document_by_id


class TempFileManager:
    def __init__(self, cleanup_interval=3600, file_lifetime=1800):  # 1 hour cleanup, 30 min lifetime
        self.temp_dir = tempfile.mkdtemp(prefix="highlighted_pdfs_")
        self.cleanup_interval = cleanup_interval
        self.file_lifetime = file_lifetime
        self.file_timestamps = {}
        self._start_cleanup_thread()

    def _start_cleanup_thread(self):
        thread = threading.Thread(target=self._cleanup_loop, daemon=True)
        thread.start()

    def _cleanup_loop(self):
        while True:
            self.cleanup_old_files()
            time.sleep(self.cleanup_interval)

    def cleanup_old_files(self):
        current_time = datetime.now()
        files_to_remove = []
        
        for filepath, timestamp in self.file_timestamps.items():
            if current_time - timestamp > timedelta(seconds=self.file_lifetime):
                try:
                    if os.path.exists(filepath):
                        os.remove(filepath)
                    files_to_remove.append(filepath)
                except Exception as e:
                    print(f"Error removing file {filepath}: {e}")

        for filepath in files_to_remove:
            self.file_timestamps.pop(filepath, None)

    def add_file(self, filepath):
        self.file_timestamps[filepath] = datetime.now()

    def get_temp_filepath(self, prefix="highlighted_", suffix=".pdf"):
        return os.path.join(self.temp_dir, f"{prefix}{uuid.uuid4()}{suffix}")


class PDFHighlighter:
    def __init__(self, temp_file_manager):
        self.temp_file_manager = temp_file_manager

    def highlight_text_in_pdf(self, pdf_path, relevant_chunks, output_path):
        """
        Highlight text in PDF with improved error handling and temporary file management.
        """
        try:
            if not os.path.exists(pdf_path):
                raise FileNotFoundError(f"File not found: {pdf_path}")

            # Try opening the PDF with additional checks
            doc = None
            try:
                doc = fitz.open(pdf_path)
            except Exception as e:
                print(f"MuPDF Error: {e}. Attempting repair...")
                repaired_path = f"{pdf_path}_repaired.pdf"
                os.system(f"qpdf --linearize {pdf_path} {repaired_path}")
                doc = fitz.open(repaired_path)

            if not doc:
                raise ValueError("Could not open the PDF after repair attempts.")

            
            highlighting_successful = False
            for page in doc:

                for chunk in relevant_chunks:
                    # Clean and prepare the text for searching
                    search_text = chunk.page_content.strip()
                    print(search_text[:200])
                    if not search_text:
                        continue
                    
                    # Break down the chunk into smaller, manageable pieces
                    sentences = [s.strip() for s in search_text.split('.') if s.strip()]
                    
                    for sentence in sentences:
                        try:
                            # Use more flexible text search
                            text_instances = page.search_for(sentence, quads=True)
                            
                            for inst in text_instances:
                                try:
                                    # Add highlight with error handling
                                    annot = page.add_highlight_annot(inst)
                                    if annot:
                                        annot.set_colors(stroke=(1, 1, 0))  # Yellow highlight
                                        annot.update()
                                        highlighting_successful = True
                                except Exception as e:
                                    print(f"Warning: Could not highlight specific instance: {str(e)}")
                                    continue
                                    
                        except Exception as e:
                            print(f"Warning: Search failed for text: {str(e)}")
                            continue

            # Save with optimization and compression
            doc.save(
                output_path,
                garbage=4,  # Garbage collection
                deflate=True,  # Compress stream
                clean=True,  # Clean content
                pretty=False  # Don't prettify output
            )
            doc.close()
            
            # Register the file with temp file manager
            if highlighting_successful:
                self.temp_file_manager.add_file(output_path)
                return output_path
            else:
                print("No highlights were added to the document")
                return None

        except Exception as e:
            print(f"Error in highlight_text_in_pdf: {str(e)}")
            traceback.print_exc()
            if 'doc' in locals():
                doc.close()
            return None

    def create_highlighted_pdf(self, mongo_id, relevant_chunks):
        """
        Creates a highlighted version of a PDF file from MongoDB document.
        """
        temp_original_path = None
        try:
            # Get document from MongoDB
            document = get_document_by_id(mongo_id)
            if not document:
                print(f"Document not found in MongoDB with ID: {mongo_id}")
                return None

            # Create temporary file for the original PDF
            temp_original_path = self.temp_file_manager.get_temp_filepath(prefix="original_")
            with open(temp_original_path, 'wb') as temp_file:
                temp_file.write(document['file_data'])

            # Generate path for highlighted PDF
            highlighted_pdf_path = self.temp_file_manager.get_temp_filepath(prefix="highlighted_")

            # Attempt to highlight the PDF
            result = self.highlight_text_in_pdf(temp_original_path, relevant_chunks, highlighted_pdf_path)
            
            if result is None:
                print("Highlighting failed, returning original PDF")
                # Copy original PDF to expected location
                import shutil
                shutil.copy2(temp_original_path, highlighted_pdf_path)
                self.temp_file_manager.add_file(highlighted_pdf_path)

            return highlighted_pdf_path

        except Exception as e:
            print(f"Error highlighting PDF: {e}")
            traceback.print_exc()
            return None
        finally:
            # Clean up temporary original file
            if temp_original_path and os.path.exists(temp_original_path):
                try:
                    os.unlink(temp_original_path)
                except Exception as e:
                    print(f"Error removing temporary file: {e}")