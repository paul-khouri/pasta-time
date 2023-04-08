/* database creation */

/* destroy all tables */
drop table if exists news;
drop table if exists member_news;
drop table if exists member;


/* create tables */

create table member(
    member_id integer primary key autoincrement not null,
    name text not null unique,
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
    member_id date not null,
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
       (select member_id from member where name="Mike" )
       );

insert into news(title, subtitle, content, newsdate, member_id)
values('Tasting Night!',
       'Come in and try some new dishes that might end up on our menu.',
       'Jack, our chef, has been working with his team to design some new dishes.' || char(10) ||
       'He has recently returned from Italy and visited many of Italy''s best pasta bars.' || char(10) ||
       'If you would like to be part of our customer tasting panel please put a comment below and we''ll get back to you.'
      ,
       '2023-03-12 17:45:00',
       (select member_id from member where name="Vanessa" )
       )



