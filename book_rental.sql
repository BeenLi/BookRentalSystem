/*
 Navicat MySQL Data Transfer

 Source Server         : mysql5.0
 Source Server Type    : MySQL
 Source Server Version : 50022
 Source Host           : localhost:3306
 Source Schema         : book_rental

 Target Server Type    : MySQL
 Target Server Version : 50022
 File Encoding         : 65001

 Date: 17/02/2021 21:54:16
*/

SET FOREIGN_KEY_CHECKS = 0;

CREATE DATABASE IF NOT EXISTS book_rental DEFAULT CHARSET utf8 COLLATE utf8_general_ci;

DROP TABLE IF EXISTS `book_item`;
CREATE TABLE `book_item`  (
  `ISBN` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT 'ISBN',
  `bname` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '书名',
  `price` float(10, 2) NULL DEFAULT NULL COMMENT '单价',
  `inventory` int(3) NULL DEFAULT NULL COMMENT '库存',
  PRIMARY KEY USING BTREE (`ISBN`)
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

DROP TABLE IF EXISTS `customer_info`;
CREATE TABLE `customer_info`  (
  `uid` int(10) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '顾客编号',
  `uname` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '顾客姓名',
  `card_class` enum('月卡','季卡','年卡') CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '办卡类型',
  `rental_time` date NOT NULL COMMENT '办卡日期',
  `expire_date` int(5) NULL COMMENT '剩余天数',
  PRIMARY KEY USING BTREE (`uid`)
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

DROP TABLE IF EXISTS `order_info`;
CREATE TABLE `order_info`  (
  `uid` int(10) UNSIGNED NOT NULL COMMENT '顾客编号',
  `uname` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '顾客姓名',
  `ISBN` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT 'ISBN',
  `bname` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '租书书名',
  `start_time` date NOT NULL COMMENT '借书日期',
  `end_time` date NULL COMMENT '还书日期',
  INDEX `ISBN` USING BTREE(`ISBN`)
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

SET FOREIGN_KEY_CHECKS = 1;
