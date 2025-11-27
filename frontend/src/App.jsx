import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";

// Import your landing page component
import Landing_Page from "./components/Landing_page.jsx";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Landing Page Route */}
        <Route path="/" element={<Landing_Page />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
