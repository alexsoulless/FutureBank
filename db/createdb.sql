CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(64) NOT NULL UNIQUE,
    fio VARCHAR(64) NOT NULL,
    balance NUMERIC(10, 2) DEFAULT 0.00,
    is_banned BOOLEAN DEFAULT FALSE,
    role INT DEFAULT 0
);
COMMENT ON TABLE users IS 'Таблица для хранения информации о пользователях';

CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    sender_id INT REFERENCES users(id),
    recipient_id INT REFERENCES users(id),
    transaction_datetime TIMESTAMP NOT NULL,
    amount NUMERIC(10, 2) NOT NULL
);
CREATE INDEX idx_sender_id ON transactions(sender_id);
CREATE INDEX idx_recipient_id ON transactions(recipient_id);
COMMENT ON TABLE transactions IS 'Таблица для хранения транзакций между пользователями';

CREATE TABLE taxes (
    id SERIAL PRIMARY KEY,
    name VARCHAR(32) NOT NULL,
    due_datetime TIMESTAMP NOT NULL,
    amount NUMERIC(10, 2) NOT NULL
);
COMMENT ON TABLE taxes IS 'Таблица для хранения информации о налогах';

CREATE TABLE tax_payments (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(id),
    tax_id INT NOT NULL REFERENCES taxes(id)
);

CREATE INDEX idx_user_id ON tax_payments(user_id);
CREATE INDEX idx_tax_id ON tax_payments(tax_id);
COMMENT ON TABLE tax_payments IS 'Таблица для хранения платежей по налогам';