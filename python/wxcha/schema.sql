-- 创建数据库
CREATE DATABASE wxcha;

USE wxcha;

-- 创建图片分组项表
CREATE TABLE picture_group
(
    picture_group_id BIGINT NOT NULL AUTO_INCREMENT COMMENT '图片id',
    type VARCHAR(120) NOT NULL COMMENT '图片类型',
    title VARCHAR(120) COMMENT '图片标题、描述',
    thumbs_up_times BIGINT COMMENT '点赞、喜欢或推荐等次数',
    mark VARCHAR(120) COMMENT '标签(用,隔开)',
    group_url VARCHAR(512) COMMENT '分组url',
    group_url_md5 VARCHAR(64) UNIQUE COMMENT '图片分组链接MD5值',
    crawl_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '爬取时间',
    crawl_origin VARCHAR(120) COMMENT '爬取源（如头条）',
    crawl_url VARCHAR(512) COMMENT '爬取源url(如https://www.toutiao.com/ch/news_hot/)',
    PRIMARY KEY (picture_group_id)
)ENGINE=InnoDB AUTO_INCREMENT=1000 DEFAULT CHARSET=utf8 COMMENT='图片分组项表';

-- 创建图片项表
CREATE TABLE picture
(
    picture_id BIGINT NOT NULL AUTO_INCREMENT COMMENT '图片id',
    picture_group_id BIGINT NOT NULL COMMENT '图片分组id，对应picture_group表的picture_group_id',
    picture_url VARCHAR(512) COMMENT '图片链接',
    picture_url_md5 VARCHAR(64) UNIQUE COMMENT '图片链接MD5值',
    PRIMARY KEY (picture_id)
)ENGINE=InnoDB AUTO_INCREMENT=1000 DEFAULT CHARSET=utf8 COMMENT='图片项表';

-- 创建图片分组爬取失败项表
CREATE TABLE picture_crawl_failed
(
    picture_crawl_failed_id BIGINT NOT NULL AUTO_INCREMENT COMMENT '图片id',
    group_url VARCHAR(512) COMMENT '分组url',
    group_url_md5 VARCHAR(64) UNIQUE COMMENT '图片分组链接MD5值',
    type VARCHAR(120) NOT NULL COMMENT '图片类型',
    PRIMARY KEY (picture_crawl_failed_id)
)ENGINE=InnoDB AUTO_INCREMENT=1000 DEFAULT CHARSET=utf8 COMMENT='图片分组爬取失败项表';