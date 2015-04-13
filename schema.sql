drop table if exists stories;
create table stories (
  id integer primary key autoincrement,
  title text not null,
  page integer not null,
  line_num integer not null,
  character text not null,
  script text not null
);