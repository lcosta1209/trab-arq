import { useState, useEffect } from "react";

const API = "http://localhost:8000";

const STATUS_LABEL = {
  pending: "Pendente",
  in_progress: "Em andamento",
  done: "Concluído",
};

const STATUS_NEXT = {
  pending: "in_progress",
  in_progress: "done",
  done: null,
};

const STATUS_COLOR = {
  pending: "#e2a04a",
  in_progress: "#4a90d9",
  done: "#4caf7d",
};

export default function App() {
  const [tasks, setTasks] = useState([]);
  const [newTitle, setNewTitle] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  async function fetchTasks() {
    try {
      const res = await fetch(`${API}/tasks/`);
      const data = await res.json();
      setTasks(data);
    } catch {
      setError("Não foi possível conectar com a API.");
    } finally {
      setLoading(false);
    }
  }

  async function createTask(e) {
    e.preventDefault();
    if (!newTitle.trim()) return;
    const res = await fetch(`${API}/tasks/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title: newTitle.trim() }),
    });
    const task = await res.json();
    setTasks((prev) => [...prev, task]);
    setNewTitle("");
  }

  async function advanceStatus(task) {
    const next = STATUS_NEXT[task.status];
    if (!next) return;
    const res = await fetch(`${API}/tasks/${task.id}/status`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ status: next }),
    });
    const updated = await res.json();
    setTasks((prev) => prev.map((t) => (t.id === updated.id ? updated : t)));
  }

  useEffect(() => { fetchTasks(); }, []);

  return (
    <div style={styles.page}>
      <header style={styles.header}>
        <h1 style={styles.title}>TaskFlow</h1>
        <span style={styles.subtitle}>Gerenciador de tarefas</span>
      </header>

      <form onSubmit={createTask} style={styles.form}>
        <input
          style={styles.input}
          type="text"
          placeholder="Nova tarefa..."
          value={newTitle}
          onChange={(e) => setNewTitle(e.target.value)}
        />
        <button style={styles.button} type="submit">Adicionar</button>
      </form>

      {loading && <p style={styles.info}>Carregando...</p>}
      {error && <p style={{ ...styles.info, color: "#e05c5c" }}>{error}</p>}

      {!loading && !error && (
        <table style={styles.table}>
          <thead>
            <tr>
              <th style={styles.th}>Tarefa</th>
              <th style={styles.th}>Status</th>
              <th style={styles.th}>Ação</th>
            </tr>
          </thead>
          <tbody>
            {tasks.length === 0 && (
              <tr>
                <td colSpan={3} style={{ ...styles.td, textAlign: "center", color: "#999" }}>
                  Nenhuma tarefa ainda.
                </td>
              </tr>
            )}
            {tasks.map((task) => (
              <tr key={task.id} style={styles.tr}>
                <td style={styles.td}>{task.title}</td>
                <td style={styles.td}>
                  <span style={{ ...styles.badge, background: STATUS_COLOR[task.status] }}>
                    {STATUS_LABEL[task.status]}
                  </span>
                </td>
                <td style={styles.td}>
                  {STATUS_NEXT[task.status] ? (
                    <button style={styles.advanceBtn} onClick={() => advanceStatus(task)}>
                      Avançar →
                    </button>
                  ) : (
                    <span style={{ color: "#999", fontSize: "0.85rem" }}>Concluída</span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

const styles = {
  page: {
    maxWidth: 700,
    margin: "0 auto",
    padding: "2rem 1rem",
    fontFamily: "'Segoe UI', sans-serif",
    color: "#1a1a1a",
  },
  header: {
    marginBottom: "2rem",
  },
  title: {
    fontSize: "2rem",
    fontWeight: 700,
    margin: 0,
    letterSpacing: "-0.5px",
  },
  subtitle: {
    fontSize: "0.9rem",
    color: "#888",
  },
  form: {
    display: "flex",
    gap: "0.5rem",
    marginBottom: "2rem",
  },
  input: {
    flex: 1,
    padding: "0.6rem 0.9rem",
    fontSize: "1rem",
    border: "1px solid #ddd",
    borderRadius: 6,
    outline: "none",
  },
  button: {
    padding: "0.6rem 1.2rem",
    fontSize: "1rem",
    background: "#1a1a1a",
    color: "#fff",
    border: "none",
    borderRadius: 6,
    cursor: "pointer",
  },
  table: {
    width: "100%",
    borderCollapse: "collapse",
  },
  th: {
    textAlign: "left",
    padding: "0.6rem 0.8rem",
    fontSize: "0.8rem",
    textTransform: "uppercase",
    letterSpacing: "0.05em",
    color: "#888",
    borderBottom: "2px solid #eee",
  },
  tr: {
    borderBottom: "1px solid #f0f0f0",
  },
  td: {
    padding: "0.75rem 0.8rem",
    fontSize: "0.95rem",
  },
  badge: {
    display: "inline-block",
    padding: "0.2rem 0.6rem",
    borderRadius: 20,
    color: "#fff",
    fontSize: "0.8rem",
    fontWeight: 500,
  },
  advanceBtn: {
    padding: "0.3rem 0.8rem",
    fontSize: "0.85rem",
    background: "transparent",
    border: "1px solid #ddd",
    borderRadius: 5,
    cursor: "pointer",
    color: "#444",
  },
  info: {
    color: "#888",
    textAlign: "center",
    marginTop: "2rem",
  },
};
