create table if not exists genes (
  id integer primary key auto_increment,
  name varchar(20) not null unique,
  old_name varchar(20),
  product varchar(200),
  cog_id integer,
  is_id integer,
  sequence varchar(8000));

create table cog (
  id integer primary key auto_increment,
  name varchar(50) not null unique,
  cog_name varchar(200),
  cog_category_id integer not null,
  cog_pathway_id integer
);

create table cog_categories (
  id integer primary key auto_increment,
  name varchar(200) not null
);

create table cog_pathways (
  id integer primary key auto_increment,
  name varchar(200) not null
);

create table insertion_sequences (
  id integer primary key auto_increment,
  name varchar(30) not null,
  family varchar(50),
  subgroup varchar(30)
);
