create database Flask_shop;

show databases;

use Flask_shop;

create table user(
 no int(3) AUTO_INCREMENT,
 id varchar(20) NOT NULL,
 name varchar(20) NOT NULL,
 age varchar(3) NOT NULL,
 birthday date NOT NULL,
 gender varchar(2) NOT NULL,
 mail varchar(100) NOT NULL,
 zip varchar(8) NOT NULL,
 zyusyo varchar(50) NOT NULL,
 pw varchar(64) NOT NULL,
 salt varchar(64) NOT NULL,
 point int(8) DEFAULT 0,
 PRIMARY KEY(no)
);



create table product(
 no int(3) AUTO_INCREMENT,
 product_name varchar(50) NOT NULL,
 product_price int(5) NOT NULL,
 data varchar(200),
 class varchar(10) NOT NULL,
 pasu varchar(100) NOT NULL,
 PRIMARY KEY(no)
);

insert into product(product_name,product_price,data,class,pasu) values('ラプラスぬいぐるみ', 75600, 
'ポケモンセンターオンライン
抽選限定販売 超ビッグサイズぬいぐるみ',
 'おもちゃ', 'ラプラス_ぬいぐるみ.jpg');
 
insert into product(product_name,product_price,data,class,pasu) values('ニンフィアぬいぐるみ', 6980, 
'本体サイズ: 25.0x13.0x14.5(H×W×D㎝)
主な製造国:フィリピン
対象年齢 :3才以上',
'おもちゃ', 'ニンフィア_ぬいぐるみ.jpg');

insert into product(product_name,product_price,data,class,pasu) values('鬼滅の刃23巻',481,
'鬼の始祖・鬼舞辻無惨と炭治郎たちの
戦いは最終局面へ…!',
  '本', '鬼滅の刃23巻.jpg');

insert into product(product_name,product_price,data,class,pasu) values('鬼滅の刃1巻',481,
'時は大正時代。
炭を売る心優しき少年・炭治郎の
日常は、家族を鬼に皆殺しに
されたことで一変する。',
  '本', '鬼滅の刃1巻.jpg');

insert into product(product_name,product_price,data,class,pasu) values('マリオカート8デラックス',5500,
'パッケージ版',
'ゲーム', 'マリオカート8デラックス.jpg');

insert into product(product_name,product_price,data,class,pasu) values('スマッシュブラザーズ',6591,
'パッケージ版',
  'ゲーム', '大乱闘スマッシュブラザーズSPECIAL.jpg');

insert into product(product_name,product_price,data,class,pasu) values('AppleAirPodsPro',30580,
'ブランド:Apple(アップル)
色:White
接続:無線
型式:インイヤー',
  '家電', 'イヤホンAppleAirPodsPro.jpg');

insert into product(product_name,product_price,data,class,pasu) values('ゼンハイザー(Sennheiser)',36300,
'ブランド:ゼンハイザー(Sennheiser)
色:ブラック
接続方式:無線
型式:インイヤー',
  '家電', 'ゼンハイザー(Sennheiser).jpg');


create table history(
 id varchar(20) NOT NULL,
 no int(3) NOT NULL,
 kazu int(3) NOT NULL,
 entry datetime NOT NULL,
 FOREIGN KEY(no) REFERENCES product(no)
);



create table reset(
 id varchar(20) NOT NULL,
 kodo varchar(20) NOT NULL
);


