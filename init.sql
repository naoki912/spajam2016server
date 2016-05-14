CREATE TABLE users (
id INTEGER PRIMARY KEY,
group_id INTEGER,
FOREIGN KEY (group_id) REFERENCES groups(id)
);

CREATE TABLE groups (
id INTEGER PRIMARY KEY,
password INTEGER,
number_of_people INTEGER DEFAULT 0,
flag INTEGER DEFAULT 1
);

CREATE TABLE state_groups (
id INTEGER PRIMARY KEY,
group_id INTEGER,
flag TEXT,
FOREIGN KEY (group_id) REFERENCES groups(group_id)
);

CREATE TABLE question_groups (
id INTEGER PRIMARY KEY,
group_id INTEGER,
FOREIGN KEY (group_id) REFERENCES groups(group_id)
);

CREATE TABLE questions (
id INTEGER PRIMARY KEY,
question_group_id INTEGER,
user_id INTEGER,
text TEXT,
FOREIGN KEY (question_group_id) REFERENCES question_groups(id),
FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE coming_out_groups (
id INTEGER PRIMARY KEY,
group_id INTEGER,
FOREIGN KEY (group_id) REFERENCES groups(group_id)
);

CREATE TABLE coming_outs (
id INTEGER PRIMARY KEY,
coming_out_group_id INTEGER,
user_id INTEGER,
text TEXT,
FOREIGN KEY (coming_out_group_id) REFERENCES coming_out_groups(id),
FOREIGN KEY (user_id) REFERENCES users(id)
);
