# BookRentalSystem
一个简单的租书系统

## 1. 需求文档

基本需求如下：

1. 记录书店所有的书
2. 记录办卡的顾客信息
3. 记录借书的订单信息

## 2. 项目构架

![mark](https://image.beenli.cn/img/20210221/PE78M0ejwJH4.png?imageslim)

| UI                  | wxPython==4.1.1            |
| ------------------- | -------------------------- |
| Python 数据库驱动库 | PyMySQL==1.0.2             |
| 数据库              | MySQL==5.0.22-community-nt |

## 3. 项目demo

### 一、书单信息(表1)

![mark](https://image.beenli.cn/img/20210221/sMOMb8OXeDry.png?imageslim)

### 二、顾客信息(表2)

![mark](https://image.beenli.cn/img/20210221/IAAuSXWpJNsA.png?imageslim)

### 三、租书信息(表3)

![mark](https://image.beenli.cn/img/20210221/8GspxpGVDNyP.png?imageslim)

## 4. 项目特色

- 每隔`1分钟`自动提交数据到数据库

- 程序打开时自动去数据库提取数据(也仅访问一次)，然后保存到一个变量中；此后所有操作只对该变量操作，不会立即反应到数据库中。只有当用户点击`提交`或者`保存`才会提交到数据库。

- 程序在每次数据修改之前，设有一次`备份`；所以允许用户进行一次`返回`操作(如果进行两次修改，那么第二次修改会覆盖第一次备份，也即只能返回一步)

- 考虑到有可能提交数据库失败，数据库访问速度等问题，本程序放弃使用`外键`，取而代之由程序内部逻辑保证数据一致性。

  