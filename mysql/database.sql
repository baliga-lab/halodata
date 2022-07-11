drop table if exists cdds;
drop table if exists cog;
drop table if exists cog_categories;
drop table if exists cog_pathways;
drop table if exists gene_cdds;
drop table if exists gene_go_bio;
drop table if exists gene_go_cell;
drop table if exists gene_interpro_refs;
drop table if exists gene_go_mol;
drop table if exists gene_locus_tags;
drop table if exists go_bio;
drop table if exists go_cell;
drop table if exists go_mol;
drop table if exists gene_pathways;
drop table if exists gene_pfam_refs;
drop table if exists gene_prosite_refs;
drop table if exists gene_smart_refs;
drop table if exists gene_uni_pathways;
drop table if exists genes;
drop table if exists interpro_refs;
drop table if exists insertion_sequences;
drop table if exists locus_tags;
drop table if exists pathways;
drop table if exists pfam_refs;
drop table if exists prosite_refs;
drop table if exists smart_refs;
drop table if exists uni_pathways;

drop table if exists cdd_refs;
drop table if exists gene_cdd_refs;
drop table if exists gene_gene_ontologies;
drop table if exists gene_gene_ontologies_bio;
drop table if exists gene_gene_ontologies_cell;
drop table if exists gene_gene_ontologies_mol;
drop table if exists gene_ontologies;
drop table if exists gene_ontologies_bio;
drop table if exists gene_ontologies_cell;
drop table if exists gene_ontologies_mol;


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
  is_extra integer default 0,

  uniprot_id varchar(50),
  string_id varchar(50),
  orthodb_id varchar(50)
);

create table if not exists interpro_refs (
  id integer primary key auto_increment,
  name varchar(200)
);

create table if not exists gene_interpro_refs (
  gene_id integer not null,
  interpro_ref_id integer not null
);

create table if not exists pfam_refs (
  id integer primary key auto_increment,
  name varchar(200)
);

create table if not exists gene_pfam_refs (
  gene_id integer not null,
  pfam_ref_id integer not null
);

create table if not exists prosite_refs (
  id integer primary key auto_increment,
  name varchar(200)
);

create table if not exists gene_prosite_refs (
  gene_id integer not null,
  prosite_ref_id integer not null
);

create table if not exists smart_refs (
  id integer primary key auto_increment,
  name varchar(200)
);

create table if not exists gene_smart_refs (
  gene_id integer not null,
  smart_ref_id integer not null
);

create table if not exists cdd_refs (
  id integer primary key auto_increment,
  name varchar(200)
);

create table if not exists gene_cdd_refs (
  gene_id integer not null,
  cdd_ref_id integer not null
);

create table if not exists pathways (
  id integer primary key auto_increment,
  name varchar(200)
);

create table if not exists gene_pathways (
  gene_id integer not null,
  pathway_id integer not null
);

create table if not exists uni_pathways (
  id integer primary key auto_increment,
  name varchar(200)
);

create table if not exists gene_uni_pathways (
  gene_id integer not null,
  pathway_id integer not null
);

create table if not exists go_bio  (
  id integer primary key auto_increment,
  name varchar(200)
);

create table if not exists gene_go_bio (
  gene_id integer not null,
  ontology_id integer not null
);

create table if not exists go_mol  (
  id integer primary key auto_increment,
  name varchar(200)
);

create table if not exists gene_go_mol (
  gene_id integer not null,
  ontology_id integer not null
);

create table if not exists go_cell  (
  id integer primary key auto_increment,
  name varchar(200)
);

create table if not exists gene_go_cell (
  gene_id integer not null,
  ontology_id integer not null
);

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
