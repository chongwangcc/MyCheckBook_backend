/*==============================================================*/
/* DBMS name:      MySQL 5.0                                    */
/* Created on:     2018/4/17 17:15:47                           */
/*==============================================================*/


drop table if exists AccountInfo;

drop table if exists CheckDetails;

drop table if exists CheckbookAcountMap;

drop table if exists CheckbookInfo;

drop table if exists UserCheckbookMap;

drop table if exists UserInfo;

/*==============================================================*/
/* Table: AccountInfo                                           */
/*==============================================================*/
create table AccountInfo
(
   account_id           varchar(128) not null,
   account_name         varchar(64),
   parent_id            int,
   level                int,
   assets_nums          float,
   liabilities_nums     float,
   primary key (account_id)
);

alter table AccountInfo comment '账户信息表，类似于：花销、投资、储蓄';

/*==============================================================*/
/* Table: CheckDetails                                          */
/*==============================================================*/
create table CheckDetails
(
   id                   varchar(128) not null,
   checkbook_id         varchar(128) not null,
   account_id           varchar(128),
   last_update_user_id  varchar(128),
   date_str             Text,
   year                 varchar(4),
   month                varchar(2),
   day                  varchar(2),
   money                float,
   description          varchar(128),
   balanceType          varchar(64),
   Category             varchar(16),
   isCreditcard         bool,
   updateTime           long,
   createTime           long,
   primary key (id)
);

alter table CheckDetails comment '记账本明细表';

/*==============================================================*/
/* Table: CheckbookAcountMap                                    */
/*==============================================================*/
create table CheckbookAcountMap
(
   checkbook_id         varchar(128),
   account_id           varchar(128)
);

/*==============================================================*/
/* Table: CheckbookInfo                                         */
/*==============================================================*/
create table CheckbookInfo
(
   id                   varchar(128) not null,
   name                 varchar(64),
   description          varchar(1024),
   islocal              bool,
   coverImage           blob,
   primary key (id)
);

/*==============================================================*/
/* Table: UserCheckbookMap                                      */
/*==============================================================*/
create table UserCheckbookMap
(
   user_id              varchar(128) not null,
   account_id           varchar(128),
   permission           int,
   description          varchar(64),
   primary key (user_id)
);

/*==============================================================*/
/* Table: UserInfo                                              */
/*==============================================================*/
create table UserInfo
(
   id                   varchar(128) not null,
   name                 varchar(16),
   password             varchar(64),
   description          Text,
   primary key (id)
);

alter table UserInfo comment '用户信息表';

alter table CheckDetails add constraint FK_Reference_3 foreign key (checkbook_id)
      references CheckbookInfo (id) on delete restrict on update restrict;

alter table CheckDetails add constraint FK_Reference_4 foreign key (account_id)
      references AccountInfo (account_id) on delete restrict on update restrict;

alter table CheckbookAcountMap add constraint FK_Reference_5 foreign key (checkbook_id)
      references CheckbookInfo (id) on delete restrict on update restrict;

alter table CheckbookAcountMap add constraint FK_Reference_6 foreign key (account_id)
      references AccountInfo (account_id) on delete restrict on update restrict;

alter table UserCheckbookMap add constraint FK_Reference_1 foreign key (user_id)
      references UserInfo (id) on delete restrict on update restrict;

alter table UserCheckbookMap add constraint FK_Reference_2 foreign key (account_id)
      references CheckbookInfo (id) on delete restrict on update restrict;

