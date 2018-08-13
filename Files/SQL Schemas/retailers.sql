CREATE TABLE walmart
(vendor_sku VARCHAR(255) PRIMARY KEY NOT NULL,
merchant_sku VARCHAR(255),
upc VARCHAR(255),
description VARCHAR(255),
quantity INT,
status VARCAR(255),
manufacturer_id VARCHAR(255)
);

CREATE TABLE bestbuy
(vendor_sku VARCHAR(255) PRIMARY KEY NOT NULL,
merchant_sku VARCHAR(255),
upc VARCHAR(255),
description VARCHAR(255),
quantity INT,
status VARCAR(255),
manufacturer_id VARCHAR(255)
);

CREATE TABLE source
(vendor_sku VARCHAR(255) PRIMARY KEY NOT NULL,
merchant_sku VARCHAR(255),
upc VARCHAR(255),
description VARCHAR(255),
quantity INT,
status VARCAR(255),
manufacturer_id VARCHAR(255)
);

CREATE TABLE staples
(vendor_sku VARCHAR(255) PRIMARY KEY NOT NULL,
staples_sku VARCHAR(255),
description VARCHAR(255),
quantity INT,
status VARCAR(255)
);

