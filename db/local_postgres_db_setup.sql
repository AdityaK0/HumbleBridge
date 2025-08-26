-- Create main user
CREATE USER addy_rw WITH ENCRYPTED PASSWORD 'pwd';

-- Create database
CREATE DATABASE humble_dev;
GRANT ALL PRIVILEGES ON DATABASE humble_dev TO addy_rw;

-- Connect to the new database
\connect humble_dev;

-- Create schema
CREATE SCHEMA IF NOT EXISTS humble AUTHORIZATION addy_rw;

-- Create roles for read-only and read-write access
CREATE ROLE humble_ro;
GRANT CONNECT ON DATABASE humble_dev TO humble_ro;
GRANT USAGE ON SCHEMA humble TO humble_ro;
GRANT SELECT ON ALL TABLES IN SCHEMA humble TO humble_ro;
ALTER DEFAULT PRIVILEGES IN SCHEMA humble GRANT SELECT ON TABLES TO humble_ro;

CREATE ROLE humble_rw;
GRANT CONNECT ON DATABASE humble_dev TO humble_rw;
GRANT USAGE ON SCHEMA humble TO humble_rw;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA humble TO humble_rw;
ALTER DEFAULT PRIVILEGES IN SCHEMA humble GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO humble_rw;

-- Create users for each role
CREATE USER humble_ro_user WITH PASSWORD 'pwd';
GRANT humble_ro TO humble_ro_user;

CREATE USER humble_rw_user WITH PASSWORD 'pwd';
GRANT humble_rw TO humble_rw_user;

-- Give permissions to your main user
GRANT USAGE, CREATE ON SCHEMA humble TO addy_rw;

-- Optional: Set default search path for schema
ALTER ROLE addy_rw SET search_path = humble;
ALTER DATABASE humble_dev SET search_path = humble;
