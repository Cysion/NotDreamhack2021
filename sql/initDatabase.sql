drop table if exists Item;
$$
drop table if exists QuestLog;
$$
drop table if exists Quest;
$$
drop table if exists Hero;
$$
create table Hero(
	HeroId int primary key,
    HeroName varchar(64),
    Gold int
    );
$$
create table Quest(
	Questid int primary key auto_increment,
	HeroId int,
	QuestName varchar(64),
    QuestDescription varchar(512),
    Reward int,
    Prio int,
    RepeatableQuest varchar (16),
    startTime datetime,
    Duration int,
    foreign key (HeroId) references Hero(HeroId)
);
$$
create table Item(
	ItemId int primary key auto_increment,
    HeroId int,
    ItemName varchar(64),
    ItemDescription varchar(512),
    Duration int,
    Cost int,
    foreign key (HeroId) references Hero(HeroId)
);
$$
create table QuestLog(
	LogId int primary key auto_increment,
    HeroId int,
    QuestId int,
    ActiveQuest bool,
    foreign key (HeroId) references Hero(HeroId),
    foreign key (QuestId) references Quest(QuestId)
);
$$