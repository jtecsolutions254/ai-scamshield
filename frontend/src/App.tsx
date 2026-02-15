import React from "react";
import { Routes, Route } from "react-router-dom";
import Shell from "./components/Shell";
import AnalyzePage from "./pages/Analyze";
import HistoryPage from "./pages/History";
import TrendsPage from "./pages/Trends";

export default function App() {
  return (
    <Shell>
      <Routes>
        <Route path="/" element={<AnalyzePage />} />
        <Route path="/history" element={<HistoryPage />} />
        <Route path="/trends" element={<TrendsPage />} />
      </Routes>
    </Shell>
  );
}
