drop table if exists cog;
drop table if exists cog_categories;
drop table if exists cog_pathways;
drop table if exists gene_locus_tags;
drop table if exists genes;
drop table if exists insertion_sequences;
drop table if exists locus_tags;
/*
drop table if exists extra_genes;
*/

create table if not exists genes (
  id integer primary key auto_increment,
  name varchar(20) not null unique,
  gene_symbol varchar(20),
  product varchar(200),
  cog_id integer,
  is_id integer,
  sequence varchar(8000),

  /* new fields */
  chrom varchar(20),
  start_pos integer,
  end_pos integer,
  strand varchar(1),
  is_extra integer
);

/*
create table if not exists extra_genes (
  id integer primary key auto_increment,
  name varchar(20) not null unique,
  gene_symbol varchar(20),
  product varchar(200),
  chrom varchar(20)
  start_pos integer,
  end_pos integer,
  strand varchar(1)
);
*/

create table if not exists locus_tags (
  id integer primary key auto_increment,
  name varchar(20) not null unique
);

create table if not exists gene_locus_tags (
  gene_id integer not null,
  locus_tag_id integer not null
);

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
