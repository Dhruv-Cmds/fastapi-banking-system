USE bankaccountsystem;

-- DROP TABLE users;
-- DROP TABLE accounts;
-- DROP TABLE transaction;

ALTER TABLE transactions ADD COLUMN status VARCHAR(20) DEFAULT 'ACTIVE';
-- SELECT * FROM users;
-- SELECT * FROM accounts;
-- SELECT * FROM transactions;