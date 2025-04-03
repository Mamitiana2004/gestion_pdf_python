create database manifest;


\c manifest

create table utilisateur(
    id serial primary key,
    identifiant varchar(255),
    password text,
    date_create date,
    date_login date
);

insert into utilisateur(identifiant,password,date_create,date_login) values('admin','admin','2025-02-05','2025-05-05');

create table vessel(
    id serial primary key,
    name varchar(255) unique,
    flag varchar(255)
);

create table voyage(
    id serial primary key,
    code varchar(255),
    vessel_id int references vessel(id),
    date_arrive date
);

create table cargo(
    id serial primary key,
    voyage_id int references voyage(id) on delete cascade,
    port_depart varchar(255),
    date_depart date,
    shipper varchar(255),
    consignee varchar(255),
    bl_no varchar(255),
    poid numeric(10,2),
    volume numeric(10,2)
);

create table cargo_produit(
    id serial primary key,
    cargo_id int references cargo(id),
    produit varchar(255),
    description_produit text
);

create table file_pdf(
    id serial primary key,
    nom varchar(255),
    nom_serveur varchar(255),
    pdf bytea
);

create table pdf_voyages(
    pdf_id int references file_pdf(id),
    voyage_id int references voyage(id)
);

create table pdf_page(
    pdf_id int references file_pdf(id),
    cargo_id int references cargo(id),
    page int 
);


create table contenu(
    pdf_id int references file_pdf(id) on delete cascade,
    page int,
    contenu text
);


