-- Create roles table
CREATE TABLE roles (
    id int PRIMARY KEY AUTO_INCREMENT,
    name varchar(255) NOT NULL UNIQUE
);


-- Create users table
CREATE TABLE users (
    id int PRIMARY KEY AUTO_INCREMENT,
    email varchar(255) NOT NULL UNIQUE,
    hashed_password varchar(255) NOT NULL,
    is_active boolean NOT NULL DEFAULT TRUE,
    address varchar(255),
    full_name varchar(255),
    phone_number varchar(15)
);


-- Create user-role table
CREATE TABLE users_roles (
    user_id int,
    role_id int,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (role_id) REFERENCES roles(id),
    PRIMARY KEY (user_id, role_id)
);


-- Init roles table
INSERT INTO
    roles (name)
VALUES
    ('admin'),
    ('user');