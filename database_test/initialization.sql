DROP DATABASE IF EXISTS pixelStore_test_db;
CREATE DATABASE pixelStore_test_db;

CREATE USER IF NOT EXISTS 'student'@'%' IDENTIFIED BY 'student';
GRANT ALL PRIVILEGES ON pixelStore_test_db.* TO 'student'@'%';
GRANT CREATE ON *.* TO 'student'@'%';

FLUSH PRIVILEGES;


CREATE TABLE notification (
        notification_id         INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        sender_id               INT UNSIGNED NOT NULL,
        receiver_id             INT UNSIGNED NOT NULL,
        sent_date_time          DATETIME NOT NULL,
        text                    VARCHAR(255) NOT NULL,
        is_read                 BOOLEAN NOT NULL
);

CREATE TABLE user (
        user_id                 INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        email                   VARCHAR(64) NOT NULL UNIQUE,
        username                VARCHAR(32) NOT NULL UNIQUE,
        password                VARCHAR(128) NOT NULL,
        is_verified             BOOLEAN NOT NULL,
        bio                     VARCHAR(1024) NOT NULL,
        money                   DECIMAL(10, 2) NOT NULL,
        is_superuser            BOOLEAN NOT NULL DEFAULT FALSE,
        last_login              DATETIME NULL,
        token_version           INT UNSIGNED NOT NULL DEFAULT 0
);

CREATE TABLE contact (
        contact_id              INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        sender_id               INT UNSIGNED NOT NULL,
        receiver_id             INT UNSIGNED NOT NULL
);

CREATE TABLE verification_code (
        verification_id         INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        user_id                 INT UNSIGNED NOT NULL,
        code                    VARCHAR(10) NOT NULL,
        creation_date_time      DATETIME NOT NULL,
        expiration_date_time    DATETIME NOT NULL
);

CREATE TABLE user_preferences (
        user_preferences_id     INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        user_id                 INT UNSIGNED NOT NULL,
        dark_mode               BOOLEAN NOT NULL
);

CREATE TABLE category (
        category_id             INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        name                    VARCHAR(32) NOT NULL UNIQUE,
        description             VARCHAR(1024) NOT NULL
);

CREATE TABLE address (
        address_id              INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        user_id                 INT UNSIGNED NOT NULL,
        address                 VARCHAR(64) NOT NULL,
        postal_code             VARCHAR(5) NOT NULL,
        city                    VARCHAR(32) NOT NULL,
        country                 VARCHAR(32) NOT NULL
);

CREATE TABLE user_statistics (
        user_statistics_id      INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        user_id                 INT UNSIGNED NOT NULL,
        creation_date           DATE NOT NULL,
        products_bought         INT UNSIGNED NOT NULL,
        products_sold           INT UNSIGNED NOT NULL
);

CREATE TABLE category_product (
        category_product_id     INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        category_id             INT UNSIGNED NOT NULL,
        product_id              INT UNSIGNED NOT NULL
);

CREATE TABLE transaction (
        transaction_id          INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        buyer_id                INT UNSIGNED NOT NULL,
        total_price             DECIMAL(8, 2) NOT NULL,
        date_time               DATETIME NOT NULL,
        is_finished             BOOLEAN NOT NULL
);

CREATE TABLE product_review (
        product_review_id       INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        product_id              INT UNSIGNED NOT NULL,
        rating                  DECIMAL(2, 1) NOT NULL,
        description             VARCHAR(1024) NOT NULL,
        reviewer_id             INT UNSIGNED NOT NULL,
        review_date             DATE NOT NULL
);

CREATE TABLE product (
        product_id              INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        owner_id                INT UNSIGNED NOT NULL,
        name                    VARCHAR(64) NOT NULL,
        description             VARCHAR(1024) NOT NULL,
        price                   DECIMAL(8, 2) NOT NULL,
        amount                  INT UNSIGNED NOT NULL,
        color                   VARCHAR(32) NOT NULL,
        weight                  DECIMAL(4, 2) NOT NULL,
        length                  DECIMAL(5, 2) NOT NULL,
        width                   DECIMAL(5, 2) NOT NULL,
        height                  DECIMAL(5, 2) NOT NULL,
        guarantee_period        DECIMAL(2, 1) NOT NULL,
        status                  ENUM('available', 'unavailable', 'archived') NOT NULL DEFAULT 'available'
);

CREATE TABLE order_product (
        order_product_id        INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        transaction_id          INT UNSIGNED NOT NULL,
        product_id              INT UNSIGNED NOT NULL,
        seller_id               INT UNSIGNED NOT NULL,
        shopping_price          DECIMAL(8, 2) NOT NULL
);

CREATE TABLE product_photo (
        product_photo_id        INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        product_id              INT UNSIGNED NOT NULL,
        image_url               VARCHAR(2048) NOT NULL,
        is_main_photo           BOOLEAN NOT NULL
);

CREATE TABLE order_return (
        order_return_id         INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        order_product_id        INT UNSIGNED NOT NULL,
        description             VARCHAR(1024) NOT NULL,
        return_date_time        DATETIME NOT NULL,
        is_accepted             BOOLEAN NOT NULL
);


ALTER TABLE notification ADD CONSTRAINT notification_sender_id_fk FOREIGN KEY(sender_id) REFERENCES user(user_id);
ALTER TABLE notification ADD CONSTRAINT notification_receiver_id_fk FOREIGN KEY(receiver_id) REFERENCES user(user_id);

ALTER TABLE contact ADD CONSTRAINT contact_sender_id_fk FOREIGN KEY(sender_id) REFERENCES user(user_id);
ALTER TABLE contact ADD CONSTRAINT contact_receiver_id_fk FOREIGN KEY(receiver_id) REFERENCES user(user_id);

ALTER TABLE verification_code ADD CONSTRAINT verification_code_user_id_fk FOREIGN KEY(user_id) REFERENCES user(user_id);

ALTER TABLE user_preferences ADD CONSTRAINT user_preferences_user_id_fk FOREIGN KEY(user_id) REFERENCES user(user_id);

ALTER TABLE address ADD CONSTRAINT address_user_id_fk FOREIGN KEY(user_id) REFERENCES user(user_id);

ALTER TABLE user_statistics ADD CONSTRAINT user_statistics_user_id_fk FOREIGN KEY(user_id) REFERENCES user(user_id);

ALTER TABLE category_product ADD CONSTRAINT category_product_category_id_fk FOREIGN KEY(category_id) REFERENCES
    category(category_id);
ALTER TABLE category_product ADD CONSTRAINT category_product_product_id_fk FOREIGN KEY(product_id) REFERENCES
    product(product_id);

ALTER TABLE transaction ADD CONSTRAINT transaction_buyer_id_fk FOREIGN KEY(buyer_id) REFERENCES user(user_id);

ALTER TABLE product_review ADD CONSTRAINT product_review_product_id_fk FOREIGN KEY(product_id) REFERENCES product(product_id);
ALTER TABLE product_review ADD CONSTRAINT product_review_reviewer_id_fk FOREIGN KEY(reviewer_id) REFERENCES user(user_id);

ALTER TABLE product ADD CONSTRAINT product_owner_id_fk FOREIGN KEY(owner_id) REFERENCES user(user_id);

ALTER TABLE order_product ADD CONSTRAINT order_item_transaction_id_fk FOREIGN KEY(transaction_id) REFERENCES
    transaction(transaction_id);
ALTER TABLE order_product ADD CONSTRAINT order_product_product_id_fk FOREIGN KEY(product_id) REFERENCES product(product_id);
ALTER TABLE order_product ADD CONSTRAINT order_product_seller_id_fk FOREIGN KEY(seller_id) REFERENCES user(user_id);

ALTER TABLE product_photo ADD CONSTRAINT product_photo_product_id_fk FOREIGN KEY(product_id) REFERENCES product(product_id);

ALTER TABLE order_return ADD CONSTRAINT order_return_order_product_id_fk FOREIGN KEY(order_product_id) REFERENCES
    product(product_id);


CREATE INDEX notification_sender_id_idx ON notification(sender_id);
CREATE INDEX notification_receiver_id_idx ON notification(receiver_id);
CREATE INDEX notification_sent_date_time_idx ON notification(sent_date_time);

CREATE INDEX contact_sender_id_idx ON contact(sender_id);
CREATE INDEX contact_receiver_id_idx ON contact(receiver_id);

CREATE INDEX verification_code_user_id_idx ON verification_code(user_id);

CREATE INDEX user_preferences_user_id_idx ON user_preferences(user_id);

CREATE INDEX category_name_idx ON category(name);

CREATE INDEX address_user_id_idx ON address(user_id);

CREATE INDEX user_statistics_user_id_idx ON user_statistics(user_id);

CREATE INDEX category_product_category_id_idx ON category_product(category_id);
CREATE INDEX category_product_product_id_idx ON category_product(product_id);

CREATE INDEX transaction_buyer_id_idx ON transaction(buyer_id);
CREATE INDEX transaction_date_time_idx ON transaction(date_time);

CREATE INDEX product_review_product_id_idx ON product_review(product_id);
CREATE INDEX product_review_reviewer_id_idx ON product_review(reviewer_id);

CREATE INDEX product_owner_id_idx ON product(owner_id);
CREATE INDEX product_name_idx ON product(name);

CREATE INDEX order_product_transaction_id_idx ON order_product(transaction_id);
CREATE INDEX order_product_product_id_idx ON order_product(product_id);
CREATE INDEX order_seller_id_idx ON order_product(seller_id);

CREATE INDEX product_photo_product_id_idx ON product_photo(product_id);

CREATE INDEX order_return_order_product_id_idx ON order_return(order_product_id);
CREATE INDEX order_return_return_date_time_idx ON order_return(return_date_time);
