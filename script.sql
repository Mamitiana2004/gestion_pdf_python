create database manifest;

\c manifest

create table utilisateur(
    id serial primary key,
    identifiant varchar(255),
    password text
);

insert into utilisateur(identifiant,password) values ('admin','admn');

    
create table manifest(
    id serial primary key,
    vessel varchar(50),
    flag varchar(50),
    voyage varchar(50),
    date_arrive date
);


create table shipper(
    id serial primary key,
    name varchar(255),
    adresse varchar(255)
);

create table consigne(
    id serial primary key,
    name varchar(255),
    adresse varchar(2550)
);

CREATE TABLE port (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255)
);

create table cargo(
    id serial primary key,
    bl_no varchar(50),
    manifest_id int references manifest(id) on delete cascade,
    shipper_id int references shipper(id) on delete set null,
    consigne_id int references consigne(id) on delete set null,
    description_good TEXT,
    weight DECIMAL(10,2),
    measurement DECIMAL(10,2)
);



-- gestion pdf 

create table file_pdf(
    id serial primary key,
    nom varchar(255),
    nom_serveur varchar(255)
);

create table pdf_manifest(
    pdf_id int references file_pdf(id),
    manifest_id int references manifest(id)
);  


create table contenu(
    pdf_id int references file_pdf(id) on delete cascade,
    page int,
    contenu text
);

-- recherche dans les contenus 
SELECT * FROM contenu where contenu LIKE '%m%';
