CREATE DATABASE recipedb;

USE recipedb;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE recipes (
	recipe_id INT AUTO_INCREMENT PRIMARY KEY,
    recipe_name VARCHAR(255) NOT NULL,
    recipe_instructions VARCHAR(1000) NOT NULL,
    recipe_ingredients VARCHAR(255) NOT NULL,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES users(id)
		ON DELETE CASCADE
        ON UPDATE CASCADE
);

SELECT * from users;
DROP TABLE recipes;