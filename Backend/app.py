from flask import Flask, request, send_file
from flask_cors import CORS
import pandas as pd
import io
import os 

app = Flask(__name__)
CORS(app)

REQUIRED_COLUMNS = [
    "event",
    "subject",
    "from",
    "Email id",
    "reason",
    "outbound_ip_type",
    "mx",
    "url",
    "user_agent",
    "type",
    "is_unique",
    "template_id"
]

@app.route("/extract", methods=["POST"])
def extract_columns():
    if "file" not in request.files:
        return {"error": "No file uploaded"}, 400
    
    file = request.files["file"]
    filename = file.filename.lower()

    # Detect & read file
    try:
        if filename.endswith(".csv"):
            df = pd.read_csv(file)
        elif filename.endswith(".xlsx") or filename.endswith(".xls"):
            df = pd.read_excel(file, engine="openpyxl")
        else:
            return {"error": "Unsupported file type. Upload CSV or Excel."}, 400
    except Exception as e:
        return {"error": f"Failed to read file: {str(e)}"}, 500

    # Keep only the matching columns
    clean_cols = [col for col in REQUIRED_COLUMNS if col in df.columns]
    output_df = df[clean_cols]

    # Convert to Excel in memory
    output_stream = io.BytesIO()
    output_df.to_excel(output_stream, index=False)
    output_stream.seek(0)

    return send_file(
        output_stream,
        as_attachment=True,
        download_name="extracted_columns.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render sets PORT automatically
    app.run(host="0.0.0.0", port=port)
