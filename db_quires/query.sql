-- Create database
CREATE DATABASE IF NOT EXISTS banking;

-- =====================================================
-- Development Database Setup
-- Replace DB_PASSWORD_FROM_ENV with your own password.
-- Do NOT use production credentials.
-- =====================================================

-- Create application user
-- Set user name and user passowrd that you set in .env DB_PASSWORD nad DB_NAME
CREATE USER IF NOT EXISTS 'banking_user'@'%'
IDENTIFIED BY 'DB_PASSWORD_FROM_ENV';

-- Grant full access to the banking database
GRANT ALL PRIVILEGES ON banking.* TO 'banking_user'@'%';

-- Reload privilege tables
FLUSH PRIVILEGES;

-- Verify granted permissions
SHOW GRANTS FOR 'banking_user'@'%';

-- Verify user exists
SELECT User, Host
FROM mysql.user
WHERE User = 'banking_user';


-- =====================================================
-- Optional Maintenance Commands
-- Uncomment only if you know what you're doing
-- =====================================================

-- DROP DATABASE banking;

USE banking;

-- View data
SELECT * FROM accounts;
SELECT * FROM transactions;
SELECT * FROM users;
