
import os

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from werkzeug.utils import secure_filename

# ==========================================
# IMPORT DOCUMENT PROCESSING MODULES
# ==========================================

from utils.document_reader import extract_text
from utils.text_processor import clean_text

# ==========================================
# IMPORT AI / NLP MODELS
# ==========================================

from models.entity_extractor import extract_entities
from models.clause_extractor import extract_clauses
from models.obligation_extractor import extract_obligations
from models.summarizer import generate_summary
from models.risk_detector import detect_risks
from models.deadline_extractor import extract_deadlines


# ==========================================
# FLASK CONFIGURATION
# ==========================================

app = Flask(__name__)

app.secret_key = "legal_document_analyzer_secret_key"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ==========================================
# CHECK ALLOWED FILE EXTENSIONS
# ==========================================

def allowed_file(filename):

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


# ==========================================
# HOME PAGE
# ==========================================

@app.route("/")
def home():

    return render_template("index.html")


# ==========================================
# DOCUMENT ANALYSIS
# ==========================================

@app.route("/analyze", methods=["POST"])
def analyze():

    # Get uploaded file
    if "file" in request.files:
        uploaded_file = request.files["file"]

    elif "document" in request.files:
        uploaded_file = request.files["document"]

    else:
        flash("Please select a document.")
        return redirect(url_for("home"))

    # Check filename
    if not uploaded_file or uploaded_file.filename == "":
        flash("No file selected.")
        return redirect(url_for("home"))

    # Check file format
    if not allowed_file(uploaded_file.filename):
        flash("Only PDF, DOCX and TXT files are supported.")
        return redirect(url_for("home"))

    original_name = secure_filename(uploaded_file.filename)

    if not original_name:
        flash("Invalid filename.")
        return redirect(url_for("home"))

    file_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        original_name
    )

    # Save uploaded document
    uploaded_file.save(file_path)

    try:

        # STEP 1: EXTRACT DOCUMENT TEXT
        raw_text = extract_text(file_path)

        # STEP 2: CLEAN DOCUMENT TEXT
        document_text = clean_text(raw_text)

        if not document_text or not document_text.strip():
            raise ValueError(
                "The uploaded document contains no readable text."
            )

        # STEP 3: ENTITY EXTRACTION
        entities = extract_entities(document_text)

        # STEP 4: CLAUSE EXTRACTION
        clauses = extract_clauses(document_text)

        # STEP 5: OBLIGATION EXTRACTION
        obligations = extract_obligations(document_text)

        # STEP 6: DOCUMENT SUMMARIZATION
        summary_error = None

        try:

            summary = generate_summary(document_text)

        except Exception as error:

            print("Summarization Error:", error)

            summary = (
                "AI summarization is temporarily unavailable. "
                "Please review the extracted document information."
            )

            summary_error = str(error)

        # STEP 7: LEGAL RISK DETECTION
        risks = detect_risks(
            document_text,
            clauses
        )

        # STEP 8: DATE AND DEADLINE EXTRACTION
        deadlines = extract_deadlines(document_text)

        # STEP 9: CUAD SEMANTIC CLAUSE DETECTION
        semantic_clauses = []
        semantic_error = None

        try:

            # Lazy import: load the semantic model when needed
            from models.semantic_cuad_matcher import (
                detect_semantic_clauses
            )

            semantic_clauses = detect_semantic_clauses(
                document_text
            )

        except Exception as error:

            print("CUAD Semantic Matching Error:", error)

            semantic_clauses = []
            semantic_error = (
                "CUAD semantic matching is temporarily unavailable."
            )

        # STEP 10: WORD COUNT
        word_count = len(document_text.split())

        # STEP 11: DISPLAY RESULTS
        return render_template(
            "result.html",
            filename=original_name,
            summary=summary,
            entities=entities,
            clauses=clauses,
            obligations=obligations,
            risks=risks,
            deadlines=deadlines,
            semantic_clauses=semantic_clauses,
            semantic_error=semantic_error,
            word_count=word_count,
            summary_error=summary_error
        )

    except Exception as error:

        print("Document Analysis Error:", error)

        flash(
            f"Document analysis failed: {error}"
        )

        return redirect(url_for("home"))

    finally:

        # Remove temporary uploaded document
        if os.path.exists(file_path):
            os.remove(file_path)


# ==========================================
# HANDLE FILE TOO LARGE
# ==========================================

@app.errorhandler(413)
def file_too_large(error):

    flash(
        "File is too large. Maximum allowed size is 16 MB."
    )

    return redirect(url_for("home"))


# ==========================================
# RUN FLASK APPLICATION
# ==========================================

if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )
