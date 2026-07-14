import { useEffect, useState } from "react";
import { healthCheck, ApiError } from "@/lib/api";

/**
 * Step 1 placeholder shell.
 *
 * This intentionally does ONE thing: prove the frontend can reach the
 * FastAPI backend through the dev proxy. The dashboard, sidebar, chat
 * UI, and agent selector are built in later steps on top of this
 * confirmed-working connection.
 */
function App() {
  const [status, setStatus] = useState<"loading" | "online" | "offline">(
    "loading"
  );
  const [detail, setDetail] = useState<string>("");

  useEffect(() => {
    healthCheck()
      .then((res) => {
        setStatus("online");
        setDetail(`${res.app} · ${res.environment}`);
      })
      .catch((err: unknown) => {
        setStatus("offline");
        setDetail(err instanceof ApiError ? err.message : "Unknown error");
      });
  }, []);

  return (
    <div className="min-h-screen flex items-center justify-center bg-nexus-bg">
      <div className="bg-nexus-surface border border-nexus-border rounded-xl px-8 py-10 w-full max-w-md text-center shadow-xl">
        <h1 className="text-2xl font-semibold text-nexus-text mb-2">
          Nexus AI
        </h1>
        <p className="text-nexus-text-muted mb-6">Multi-Agent AI Platform</p>

        <div className="flex items-center justify-center gap-2 text-sm">
          <span
            className={`h-2.5 w-2.5 rounded-full ${
              status === "online"
                ? "bg-emerald-500"
                : status === "offline"
                ? "bg-red-500"
                : "bg-amber-400 animate-pulse"
            }`}
          />
          <span className="text-nexus-text">
            {status === "loading" && "Connecting to backend..."}
            {status === "online" && `Backend online — ${detail}`}
            {status === "offline" && `Backend offline — ${detail}`}
          </span>
        </div>
      </div>
    </div>
  );
}

export default App;
