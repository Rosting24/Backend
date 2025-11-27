from flask import Flask, request, send_file
from flask_cors import CORS
import io
import os 
from logic import extract_column  # <-- import business logic

app = Flask(__name__)
CORS(app)

@app.route("/extract", methods=["POST"])
def extract_columns():
    if "file" not in request.files:
        return {"error": "No file uploaded"}, 400

    file = request.files["file"]

    # run business logic
    result = extract_column(file)
    if isinstance(result, dict):  
        return result, 400

    output_stream = result  # a BytesIO stream

    return send_file(
        output_stream,
        as_attachment=True,
        download_name="extracted_columns.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)