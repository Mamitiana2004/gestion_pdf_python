create database tdr;

\c tdr

create table utilisateur(
    id serial primary key,
    identifiant varchar(255),
    password 
);

insert into utilisateur(identifiant,password) values ('admin','admn');

    
create table cargo(
    id serial primary key,
    vessel varchar(255)
);