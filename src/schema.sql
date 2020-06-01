CREATE TABLE Catalog (
  id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR (128),
  parent INT NOT NULL,
  PRIMARY KEY (id)
);

INSERT INTO Catalog VALUES
(1, "Storages", 0),
(2, "SSD", 1),
(3, "AIC PCI-E", 2),
(4, "SATA", 2),
(5, "M.2", 2),
(6, "HDD", 1),
(7, "SAS", 6),
(8, "SATA", 6);


CREATE TABLE Field (
  id INT NOT NULL,
  name VARCHAR (128),
  typeOf INT,
  searchable INT,
  catalog_id INT,
  table_view INT,
  sort INT,
  PRIMARY KEY (id)
);

INSERT INTO Field VALUES
(1, "Capacity, GB",      0, 1, 1, 1, 100),
(2, "Product Brif",      1, 1, 1, 0, 900),
(3, "Weight, kg",        0, 0, 1, 0, 800),
(4, "Endurance, TBW",    0, 1, 2, 1, 200),
(5, "Rotate speed, RPM", 0, 1, 6, 1, 250),
(6, "Version",           0, 1, 6, 1, 300);


CREATE TABLE Good (
  id INT  NOT NULL AUTO_INCREMENT,
  name VARCHAR (128),
  price FLOAT NOT NULL,
  item_count INT NOT NULL,
  reserved_count INT NOT NULL,
  catalog_id INT NOT NULL,
  PRIMARY KEY (id)
);


CREATE TABLE TextValues ​​(
  good_id INT  NOT NULL,
  field_id INT NOT NULL,
  fValue TEXT,
  UNIQUE KEY (good_id, field_id)
);


CREATE TABLE NumberValues ​​(
  good_id INT NOT NULL,
  field_id INT NOT NULL,
  fValue INT NOT NULL,
  UNIQUE KEY (good_id, field_id)
);
