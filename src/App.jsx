import { useMemo, useState } from 'react';

const initialTasks = [
  { id: 1, title: 'Refine onboarding', priority: 'High', owner: 'Maya', done: false },
  { id: 2, title: 'Audit color contrast', priority: 'Medium', owner: 'Jules', done: true },
  { id: 3, title: 'Consolidate cards', priority: 'Low', owner: 'Theo', done: false }
];

function Badge({ level }) {
  return <span className={`badge badge-${level.toLowerCase()}`}>{level}</span>;
}

function TaskRow({ task, onToggle }) {
  return (
    <li className="task-row">
      <label className="task-title">
        <input
          type="checkbox"
          checked={task.done}
          onChange={() => onToggle(task.id)}
          aria-label={`Mark ${task.title} as ${task.done ? 'incomplete' : 'complete'}`}
        />
        <span>{task.title}</span>
      </label>
      <div className="task-meta">
        <Badge level={task.priority} />
        <span className="owner">{task.owner}</span>
      </div>
    </li>
  );
}

export default function App() {
  const [tasks, setTasks] = useState(initialTasks);
  const [search, setSearch] = useState('');

  const filteredTasks = useMemo(() => {
    const query = search.trim().toLowerCase();
    if (!query) return tasks;
    return tasks.filter((task) => task.title.toLowerCase().includes(query) || task.owner.toLowerCase().includes(query));
  }, [search, tasks]);

  const completedCount = useMemo(() => tasks.filter((task) => task.done).length, [tasks]);

  function handleToggle(id) {
    setTasks((previous) =>
      previous.map((task) => (task.id === id ? { ...task, done: !task.done } : task))
    );
  }

  return (
    <main className="app-shell">
      <section className="panel">
        <header className="header">
          <div>
            <h1>Product UI Review Board</h1>
            <p>Improved React structure with memoized filtering, reusable task rows, and accessible controls.</p>
          </div>
          <div className="stats" aria-label="Completion stats">
            <strong>{completedCount}</strong>
            <span>completed</span>
          </div>
        </header>

        <label className="search-wrap" htmlFor="task-search">
          <span>Search by task or owner</span>
          <input
            id="task-search"
            type="search"
            value={search}
            onChange={(event) => setSearch(event.target.value)}
            placeholder="Try 'Maya' or 'contrast'"
          />
        </label>

        <ul className="task-list" aria-live="polite">
          {filteredTasks.length > 0 ? (
            filteredTasks.map((task) => <TaskRow key={task.id} task={task} onToggle={handleToggle} />)
          ) : (
            <li className="empty-state">No tasks match your search.</li>
          )}
        </ul>
      </section>
    </main>
  );
}
