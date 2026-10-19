import React from "react";
import ReactDOM from "react-dom/client";

import "@fontsource/space-grotesk/500.css";
import "@fontsource/space-grotesk/600.css";
import "@fontsource/space-grotesk/700.css";
import "@fontsource/dm-sans/400.css";
import "@fontsource/dm-sans/500.css";
import "@fontsource/dm-sans/600.css";
import "@fontsource/dm-mono/400.css";
import "@fontsource/dm-mono/500.css";
import "./index.css";

import App from "./App";
import ActivityTrayPanel from "./components/activity-tray-panel";
import { ThemeProvider } from "./hooks/use-theme";

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
  <React.StrictMode>
    <ThemeProvider>
      {new URLSearchParams(window.location.search).get("panel")==="activity"?<ActivityTrayPanel/>:<App />}
    </ThemeProvider>
  </React.StrictMode>
);
