import React, { useEffect, useMemo, useState } from "react";
import { createRoot } from "react-dom/client";
import "./styles.css";

const CHECKS = [
  {
    id: "health",
    title: "Backend health-check",
    path: "/api/health/",
    description: "Django проверяет доступность PostgreSQL по контракту инфраструктуры.",
  },
  {
    id: "home",
    title: "Backend homepage",
    path: "/api/",
    description: "Backend service доступен из отдельного frontend pod.",
  },
];

async function loadCheck(check) {
  const startedAt = performance.now();
  const response = await fetch(check.path, {
    headers: {
      Accept: "application/json,text/html",
    },
  });
  const latencyMs = Math.round(performance.now() - startedAt);
  const contentType = response.headers.get("content-type") || "";
  const payload = contentType.includes("application/json")
    ? await response.json()
    : await response.text();

  return {
    ...check,
    ok: response.ok,
    statusCode: response.status,
    latencyMs,
    payload,
    checkedAt: new Date().toLocaleTimeString("ru-RU"),
  };
}

function formatPayload(payload) {
  if (typeof payload === "string") {
    return payload.replace(/<[^>]*>/g, " ").replace(/\s+/g, " ").trim();
  }

  return JSON.stringify(payload, null, 2);
}

function App() {
  const [checks, setChecks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const healthyCount = useMemo(
    () => checks.filter((check) => check.ok).length,
    [checks],
  );

  async function refresh() {
    setLoading(true);
    setError("");

    try {
      const results = await Promise.all(CHECKS.map(loadCheck));
      setChecks(results);
    } catch (err) {
      setError("Frontend не смог получить ответ от backend API.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    refresh();
    const timerId = window.setInterval(refresh, 10000);
    return () => window.clearInterval(timerId);
  }, []);

  return (
    <main className="shell">
      <section className="summary">
        <div>
          <p className="eyebrow">React frontend service</p>
          <h1>Django + PostgreSQL</h1>
          <p className="lead">
            Отдельный frontend-контейнер в Kubernetes обращается к backend через
            внутренний сервис <code>service-django</code>.
          </p>
        </div>
        <div className="summary-panel" aria-label="Backend status summary">
          <span className="summary-panel__label">Healthy checks</span>
          <strong>
            {healthyCount}/{CHECKS.length}
          </strong>
          <button className="button" type="button" onClick={refresh}>
            Обновить
          </button>
        </div>
      </section>

      {error && <p className="alert">{error}</p>}

      <section className="status-grid" aria-label="Backend checks">
        {CHECKS.map((check) => {
          const result = checks.find((item) => item.id === check.id);
          const isOk = Boolean(result?.ok);

          return (
            <article className="status-card" key={check.id}>
              <div className="status-card__header">
                <span className={isOk ? "status-dot ok" : "status-dot"} />
                <span>{result ? (isOk ? "OK" : "Error") : "Waiting"}</span>
              </div>
              <h2>{check.title}</h2>
              <p>{check.description}</p>
              <dl>
                <div>
                  <dt>Endpoint</dt>
                  <dd>{check.path}</dd>
                </div>
                <div>
                  <dt>Status</dt>
                  <dd>{result ? result.statusCode : "..."}</dd>
                </div>
                <div>
                  <dt>Latency</dt>
                  <dd>{result ? `${result.latencyMs} ms` : "..."}</dd>
                </div>
                <div>
                  <dt>Checked</dt>
                  <dd>{result ? result.checkedAt : "..."}</dd>
                </div>
              </dl>
              {result?.payload && <pre>{formatPayload(result.payload)}</pre>}
            </article>
          );
        })}
      </section>

      {loading && <p className="muted">Проверяю backend...</p>}
    </main>
  );
}

createRoot(document.getElementById("root")).render(<App />);
