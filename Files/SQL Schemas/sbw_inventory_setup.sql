CREATE TABLE sbw_inventory
(item_num INT PRIMARY KEY NOT NULL,
item_sku VARCHAR(255),
item_desc VARCHAR(255),
item_inv INT,
item_upc BIGINT,
item_asin VARCHAR(255)
);
