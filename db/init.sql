CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER,
    height NUMERIC
);

INSERT INTO users (name, age, height) VALUES
('田中', 25, 170.5),
('佐藤', 30, 165.2),
('鈴木', 22, 158.8);