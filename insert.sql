CREATE TABLE "USER" (
"ID" integer primary key autoincrement not null ,
"USERNAME" varchar(32) ,
"BIRTHDAY" datetime ,
"POINTS" float ,
"PROFILE_IMAGE" blob );