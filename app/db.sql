-- phpMyAdmin SQL Dump
-- version 4.4.15.10
-- https://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: 2019-09-03 10:14:52
-- 服务器版本： 5.5.57-log
-- PHP Version: 7.1.24

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `diymysql`
--

-- --------------------------------------------------------

--
-- 表的结构 `article`
--

CREATE TABLE IF NOT EXISTS `article` (
  `id` int(10) NOT NULL COMMENT '自增ID',
  `cid` int(10) NOT NULL COMMENT '分类ID',
  `subject` varchar(120) NOT NULL COMMENT '标题',
  `keywords` varchar(255) NOT NULL COMMENT '关键词',
  `description` varchar(255) NOT NULL COMMENT '描述',
  `body` text NOT NULL COMMENT '内容',
  `downloader` varchar(255) DEFAULT NULL COMMENT '下载地址',
  `author` varchar(32) NOT NULL DEFAULT '管理员' COMMENT '作者',
  `views` int(10) NOT NULL DEFAULT '0' COMMENT '阅读人数',
  `dateline` int(10) NOT NULL COMMENT '发布时间'
) ENGINE=InnoDB AUTO_INCREMENT=441 DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `caty`
--

CREATE TABLE IF NOT EXISTS `caty` (
  `id` int(10) NOT NULL,
  `name` varchar(32) NOT NULL COMMENT '分类名称',
  `zindex` int(10) NOT NULL DEFAULT '0' COMMENT '分类权重',
  `isdefault` int(1) NOT NULL DEFAULT '0' COMMENT '是否为默认分类',
  `catynames` varchar(255) DEFAULT '' COMMENT '采集中的分类记录',
  `dateline` int(10) NOT NULL COMMENT '添加时间'
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `caty`
--

INSERT INTO `caty` (`id`, `name`, `zindex`, `isdefault`, `catynames`, `dateline`) VALUES
(1, 'QQ教程', 1, 0, '', 1567131829),
(2, 'QQ软件', 2, 0, '', 1567131829),
(3, 'QQ资讯', 3, 0, ' QQ新闻资讯,QQ空间模块,QQ急救室,免费QQ业务,免费QQ秀, 免费点亮QQ图标', 1567131829),
(4, '游戏攻略', 4, 0, '网游攻略 ', 1567131829),
(5, '值得一看', 7, 0, 'QQ空间代码', 1567131829),
(6, '网站源码', 5, 0, '', 1567131829),
(7, '活动线报', 6, 0, '天天剁手价', 1567131829),
(8, '综合资源', 8, 1, '', 1567131829);

-- --------------------------------------------------------

--
-- 表的结构 `target_webs`
--

CREATE TABLE IF NOT EXISTS `target_webs` (
  `id` int(10) NOT NULL,
  `url` varchar(255) NOT NULL COMMENT '网址',
  `charset` char(32) NOT NULL COMMENT '字符编码',
  `identifying` char(32) NOT NULL COMMENT '标识',
  `status` int(1) NOT NULL DEFAULT '0' COMMENT '状态 0=未启用 1=启用',
  `dateline` int(10) NOT NULL COMMENT '添加时间'
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `target_webs`
--

INSERT INTO `target_webs` (`id`, `url`, `charset`, `identifying`, `status`, `dateline`) VALUES
(1, 'http://www.qqyewu.com', 'gb2312', 'qqyewu', 1, 1567131829);
INSERT INTO `target_webs` (`id`, `url`, `charset`, `identifying`, `status`, `dateline`) VALUES
(2, 'http://www.aishoujizy.com', 'gb2312', 'aishoujizy', 1, 1567131829);

-- --------------------------------------------------------

--
-- 表的结构 `web_urls`
--

CREATE TABLE IF NOT EXISTS `web_urls` (
  `id` int(10) NOT NULL,
  `url` varchar(255) NOT NULL COMMENT '采集网址',
  `name` varchar(255) NOT NULL COMMENT '名称',
  `type` varchar(32) NOT NULL COMMENT '所属网站',
  `dateline` int(10) NOT NULL COMMENT '采集时间'
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `article`
--
ALTER TABLE `article`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `caty`
--
ALTER TABLE `caty`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `target_webs`
--
ALTER TABLE `target_webs`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `web_urls`
--
ALTER TABLE `web_urls`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `article`
--
ALTER TABLE `article`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT COMMENT '自增ID',AUTO_INCREMENT=441;
--
-- AUTO_INCREMENT for table `caty`
--
ALTER TABLE `caty`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=18;
--
-- AUTO_INCREMENT for table `target_webs`
--
ALTER TABLE `target_webs`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT for table `web_urls`
--
ALTER TABLE `web_urls`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=2;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
