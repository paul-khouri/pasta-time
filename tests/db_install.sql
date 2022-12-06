/**
*Database creation script
*/
/* destroy all tables */
drop table if exists food;
drop table if exists combo;
drop table if exists combo_menu;

/* enable foreign key constraint */
pragma foreign_keys = ON;

create table food(
  food_id integer primary key autoincrement not null,
    title text not null unique,
    price real not null,
    description text unique,
    type text not null,
    image text
);

create table combo(
    combo_id integer primary key autoincrement not null,
    name text not null unique,
    description text not null unique,
    feeds integer not null
);

create table combo_menu(
    combo_id integer not null,
    food_id integer not null,
    foreign key (combo_id) references combo(combo_id),
    foreign key (food_id) references food(food_id),
    primary key (combo_id,food_id)
);