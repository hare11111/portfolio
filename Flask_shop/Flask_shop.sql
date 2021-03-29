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

insert into product(product_name,product_price,data,class,pasu) values('���v���X�ʂ������', 75600, 
'�|�P�����Z���^�[�I�����C��
���I����̔� ���r�b�O�T�C�Y�ʂ������',
 '��������', '���v���X_�ʂ������.jpg');
 
insert into product(product_name,product_price,data,class,pasu) values('�j���t�B�A�ʂ������', 6980, 
'�{�̃T�C�Y: 25.0x13.0x14.5(H�~W�~D�p)
��Ȑ�����:�t�B���s��
�Ώ۔N�� :3�ˈȏ�',
'��������', '�j���t�B�A_�ʂ������.jpg');

insert into product(product_name,product_price,data,class,pasu) values('�S�ł̐n23��',481,
'�S�̎n�c�E�S���Җ��S�ƒY���Y������
�킢�͍ŏI�ǖʂցc!',
  '�{', '�S�ł̐n23��.jpg');

insert into product(product_name,product_price,data,class,pasu) values('�S�ł̐n1��',481,
'���͑吳����B
�Y�𔄂�S�D�������N�E�Y���Y��
����́A�Ƒ����S�ɊF�E����
���ꂽ���Ƃň�ς���B',
  '�{', '�S�ł̐n1��.jpg');

insert into product(product_name,product_price,data,class,pasu) values('�}���I�J�[�g8�f���b�N�X',5500,
'�p�b�P�[�W��',
'�Q�[��', '�}���I�J�[�g8�f���b�N�X.jpg');

insert into product(product_name,product_price,data,class,pasu) values('�X�}�b�V���u���U�[�Y',6591,
'�p�b�P�[�W��',
  '�Q�[��', '�嗐���X�}�b�V���u���U�[�YSPECIAL.jpg');

insert into product(product_name,product_price,data,class,pasu) values('AppleAirPodsPro',30580,
'�u�����h:Apple(�A�b�v��)
�F:White
�ڑ�:����
�^��:�C���C���[',
  '�Ɠd', '�C���z��AppleAirPodsPro.jpg');

insert into product(product_name,product_price,data,class,pasu) values('�[���n�C�U�[(Sennheiser)',36300,
'�u�����h:�[���n�C�U�[(Sennheiser)
�F:�u���b�N
�ڑ�����:����
�^��:�C���C���[',
  '�Ɠd', '�[���n�C�U�[(Sennheiser).jpg');


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


