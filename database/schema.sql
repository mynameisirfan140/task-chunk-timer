CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    total_duration INTERVAL NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE subtasks (
    id SERIAL PRIMARY KEY,
    task_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    duration INTERVAL NOT NULL,
    completed_at TIMESTAMPTZ,
    FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE
);