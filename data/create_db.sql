/* database creation */

drop table if exists news;
drop table if exists member;
drop table if exists food;
drop table if exists combo;
drop table if exists combo_menu;

/* create tables */
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

create table member(
    member_id integer primary key autoincrement not null,
    name text not null,
    email text not null unique,
    password text not null,
    authorisation integer not null
);

create table news(
    news_id integer primary key autoincrement not null,
    title text not null unique,
    subtitle text not null unique,
    content text not null unique,
    newsdate date not null,
    member_id integer not null,
    foreign key(member_id) references member(member_id)
);



insert into member( name, email, password, authorisation)
values('Mike', 'm@g.com', 'temp', 0 );
insert into member( name, email, password, authorisation)
values('Vanessa', 'vanny@yahoo.com', 'temp', 0 );
insert into member( name, email, password, authorisation)
values('Olivia', 'olly66@marsden.com', 'temp', 1 );
insert into member( name, email, password, authorisation)
values('Suzie', 'zuzy@qmc.com', 'temp', 1 );


insert into news(title, subtitle, content, newsdate, member_id)
values('Pasta Happy Hour!',
       'Every Thursday from 5:00 to 6:30, 15% off any of our Combos',
       'That''s right, it''s real! ' || char(10) ||
       'Drop in early with your work mates and have a great feed at a discount price.',
       '2023-03-04 20:30:00',
       (select member_id from member where name='Mike' )
       );

insert into news(title, subtitle, content, newsdate, member_id)
values('Tasting Night!',
       'Come in and try some new dishes that might end up on our menu.',
       'Jack, our chef, has been working with his team to design some new dishes.' || char(10) ||
       'He has recently returned from Italy and visited many of Italy''s best pasta bars.' || char(10) ||
       'If you would like to be part of our customer tasting panel please put a comment below and we''ll get back to you.'
      ,
       '2023-03-12 17:45:00',
       (select member_id from member where name='Vanessa' )
       );

insert into news(title, subtitle, content, newsdate, member_id)
values('Party night!',
       'Come along after hours next Saturday 5 May.',
       'Meet the staff and enjoy value drinks and entree plates.' ,
       '2023-01-30 10:45:00',
       (select member_id from member where name='Mike' )
       );

insert into news(title, subtitle, content, newsdate, member_id)
values('Date night!!',
       'Bring your date for a couples night out.',
       'Fixed price ($100.00) menu for two..' ,
       '2023-02-23 10:45:00',
       (select member_id from member where name='Vanessa' )
       );


