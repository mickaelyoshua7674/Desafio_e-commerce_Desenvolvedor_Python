DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id_user SERIAL PRIMARY KEY,
    login VARCHAR(20) NOT NULL UNIQUE,
    "password" VARCHAR(20) NOT NULL
);

DROP TABLE IF EXISTS users_info;
CREATE TABLE users (
    id_user_info SERIAL PRIMARY KEY,
    
    first_name VARCHAR(20) NOT NULL,
    senha VARCHAR(20) NOT NULL
);