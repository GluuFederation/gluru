# Client
## Running on local
```
cd client
npm install
npm run dev
```

# Server
## Prequites
 - Postgresql
 - Python Dev Environment

 ## Configure Database
```
sudo su postgres
psql
CREATE DATABASE database_name;
CREATE USER my_username WITH PASSWORD 'my_password';
GRANT ALL PRIVILEGES ON DATABASE "database_name" to my_username;
```