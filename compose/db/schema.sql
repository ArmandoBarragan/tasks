\c tasks

CREATE TABLE projects(
    id SERIAL,
    name VARCHAR(50),

    CONSTRAINT projects_pk PRIMARY KEY (id)
);


CREATE TABLE tasks(
    id SERIAL,
    name VARCHAR(50),
    project_pk INT,

    CONSTRAINT tasks_pk PRIMARY KEY (id),
    CONSTRAINT project_fk FOREIGN KEY (project_pk) REFERENCES projects(id)
);


CREATE TABLE session_records (
    id SERIAL PRIMARY KEY,
    starting_time TIMESTAMP NOT NULL,
    finishing_time TIMESTAMP,
    task_pk INT,

    CONSTRAINT task_fk FOREIGN KEY (task_pk) REFERENCES tasks(id) ON DELETE CASCADE
);
