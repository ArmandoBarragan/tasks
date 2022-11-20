\c tasks

CREATE TABLE tasks(
    id SERIAL,
    name VARCHAR(50),

    CONSTRAINT tasks_pk PRIMARY KEY (id)
);


CREATE TABLE session_records (
    id SERIAL PRIMARY KEY,
    starting_time TIMESTAMP NOT NULL,
    finishing_time TIMESTAMP NULL,
    task_pk INT,

    CONSTRAINT task_fk FOREIGN KEY (task_pk) REFERENCES tasks(id) ON DELETE CASCADE
);
