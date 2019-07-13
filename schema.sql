CREATE TABLE IF NOT EXISTS "USER" (
"ID" integer primary key autoincrement not null ,
"USERNAME" varchar(32) ,
CREATE INDEX "USER_IDX1" on "USER"("ID");
CREATE TABLE IF NOT EXISTS "PRODUCT" (
"ID" integer primary key autoincrement not null ,
"PRODUCT_NAME" varchar(32) ,
CREATE INDEX "USER_IDX1" on "PRODUCT"("ID");