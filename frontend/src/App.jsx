import React, { useState } from "react";

function App() {
  const [file, setFile] = useState(null);
  const [downloading, setDownloading] = useState(false);

  const handleUpload = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async () => {
    if (!file) {
      alert("Please upload a file first.");
      return;
    }

    setDownloading(true);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("http://127.0.0.1:5000/extract", {
        method: "POST",
        body: formData,
      });

      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);

      const a = document.createElement("a");
      a.href = url;
      a.download = "extracted_columns.xlsx";
      a.click();
      window.URL.revokeObjectURL(url);

    } catch (err) {
      alert("Error: " + err);
    }

    setDownloading(false);
  };

  return (
    <div style={{ padding: "40px", fontFamily: "Arial" }}>
      <h2>Extract Required Excel Columns</h2>
      <input type="file" onChange={handleUpload} accept=".xlsx,.xls" />
      <br /><br />
      <button onClick={handleSubmit} disabled={downloading}>
        {downloading ? "Processing..." : "Extract Columns"}
      </button>
    </div>
  );
}

export default App;
