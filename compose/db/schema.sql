\c tasks

CREATE TABLE projects (
    id SERIAL,
    name VARCHAR (50),

    CONSTRAINT project_pk PRIMARY KEY (id)
);

CREATE TABLE tasks (
    id SERIAL,
    name VARCHAR (50),
    project_pk INT,

    CONSTRAINT task_pk PRIMARY KEY (id),
    CONSTRAINT project_fk FOREIGN KEY (project_pk)
        REFERENCES projects (id) ON DELETE SET NULL
);