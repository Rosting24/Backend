import pandas as pd
import io

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

def process_file(file):
    filename = file.filename.lower()

    try:
        if filename.endswith(".csv"):
            df = pd.read_csv(file)
        elif filename.endswith(".xlsx") or filename.endswith(".xls"):
            df = pd.read_excel(file, engine="openpyxl")
        else:
            return {"error": "Unsupported file type. Upload CSV or Excel."}
    except Exception as e:
        return {"error": f"Failed to read file: {str(e)}"}

    clean_cols = [col for col in REQUIRED_COLUMNS if col in df.columns]
    output_df = df[clean_cols]

    output_stream = io.BytesIO()
    output_df.to_excel(output_stream, index=False)
    output_stream.seek(0)

    return output_stream
