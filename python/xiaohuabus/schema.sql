-- 创建数据库
CREATE DATABASE xiaohuabus;

USE xiaohuabus;

-- 创建图片项表
CREATE TABLE picture
(
    picture_id BIGINT NOT NULL AUTO_INCREMENT COMMENT '图片id',
    type VARCHAR(120) NOT NULL COMMENT '图片类型',
    title VARCHAR(120) COMMENT '图片标题、描述',
    media_url VARCHAR(512) COMMENT '源媒体（创建者的主页）',
    media_avatar_img VARCHAR(512) COMMENT '源媒体头像',
    media_name VARCHAR(120) COMMENT '原媒体名称',
    comment_count BIGINT COMMENT '评论数量',
    thumbs_up_times BIGINT COMMENT '点赞、喜欢或推荐等次数',
    thumbnail VARCHAR(512) COMMENT '缩略图',
    picture_url VARCHAR(512) COMMENT '图片链接',
    picture_url_md5 VARCHAR(64) UNIQUE COMMENT '图片链接MD5值',
    mark VARCHAR(120) COMMENT '标签(用,隔开)',
    crawl_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '爬取时间',
    crawl_origin VARCHAR(120) COMMENT '爬取源（如头条）',
    crawl_url VARCHAR(512) COMMENT '爬取源url(如https://www.toutiao.com/ch/news_hot/)',
    PRIMARY KEY (picture_id)
)ENGINE=InnoDB AUTO_INCREMENT=1000 DEFAULT CHARSET=utf8 COMMENT='图片项';

-- 创建段子项表
CREATE TABLE joke
(
    joke_id BIGINT NOT NULL AUTO_INCREMENT COMMENT '段子id',
    type VARCHAR(120) NOT NULL COMMENT '段子类型',
    title VARCHAR(120) COMMENT '段子标题、描述',
    media_url VARCHAR(512) COMMENT '源媒体（创建者的主页）',
    media_avatar_img VARCHAR(512) COMMENT '源媒体头像',
    media_name VARCHAR(120) COMMENT '原媒体名称',
    thumbs_up_times BIGINT COMMENT '点赞、喜欢或推荐等次数',
    content LONGTEXT NOT NULL COMMENT '内容',
    mark VARCHAR(120) COMMENT '标签(用,隔开)',
    crawl_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '爬取时间',
    crawl_origin VARCHAR(120) COMMENT '爬取源（如头条）',
    crawl_url VARCHAR(512) COMMENT '爬取url(如https://www.toutiao.com/ch/news_hot/)',
    crawl_url_md5 VARCHAR(64) UNIQUE COMMENT '爬取url MD5值',
    PRIMARY KEY (joke_id)
)ENGINE=InnoDB AUTO_INCREMENT=1000 DEFAULT CHARSET=utf8 COMMENT='段子项';