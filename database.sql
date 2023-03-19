-- Create table for builder
create table builder(id int primary key auto_increment, 
                     username varchar(50) not null, 
                     email varchar(100) not null, 
                     hashed_password varchar(100) not null, 
                     hashed_conpassword varchar(100) not null, 
                     companyname varchar(100) not null, 
                     industry varchar(100) not null, 
                     location varchar(100) not null, 
                     phone bigint(10) not null, 
                     reset_otp int, 
                     image blob not null);


--Create table for users
create table users(id int primary key auto_increment, 
                   username varchar(50) not null, 
                   email varchar(100) not null, 
                   hashed_password varchar(100) not null, 
                   hashed_conpassword varchar(100) not null, 
                   location varchar(50) not null, 
                   phone bigint(10) not null, 
                   reset_otp int, 
                   image blob not null);

-- Bitting for user table
create table bit(id int not null primary key auto_increment, 
                 uid int not null, 
                 name varchar(50) not null, 
                 email varchar(50) not null, 
                 location varchar(30) not null, 
                 address varchar(100) not null, 
                 phone bigint(10) not null, 
                 approval_status varchar(30) not null, 
                 timeline varchar(30) not null, 
                 sqft varchar(10) not null, 
                 build_type varchar(50) not null, 
                 budget int not null, 
                 wood varchar(50) not null, 
                 room int not null, 
                 additional varchar(100) not null);