-- 创建数据库
CREATE DATABASE large_data;

USE large_data;

CREATE TABLE news(
news_id BIGINT NOT NULL AUTO_INCREMENT COMMENT '新闻id',
type VARCHAR(120) NOT NULL COMMENT '新闻类型',
title VARCHAR(120) NOT NULL COMMENT '新闻标题',
media_url VARCHAR(512) COMMENT '源媒体',
media_avatar_img VARCHAR(512) COMMENT '源媒体头像',
media_name VARCHAR(120) COMMENT '原媒体名称',
comment_count BIGINT COMMENT '评论数量',
article_img VARCHAR(512) COMMENT '新闻标题图片',
article_url VARCHAR(512) COMMENT '新闻源链接',
mark VARCHAR(120) COMMENT '标签(用空格隔开)',
crawl_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '爬取时间',
crawl_origin VARCHAR(120) COMMENT '爬取源（如头条）',
crawl_url VARCHAR(512) COMMENT '爬取源url(如https://www.toutiao.com/ch/news_hot/)',
crawl_url_md5 VARCHAR(16) UNIQUE COMMENT 'crawl_url的MD5值',
PRIMARY KEY (news_id)
)ENGINE=InnoDB AUTO_INCREMENT=1000 DEFAULT CHARSET=utf8 COMMENT='新闻爬取项表';

CREATE TABLE news_content(
news_content_id BIGINT NOT NULL AUTO_INCREMENT COMMENT '新闻内容id',
news_url VARCHAR(512) NOT NULL COMMENT '新闻源链接',
news_url_md5 VARCHAR(16) UNIQUE COMMENT 'news_url的MD5值',
content MEDIUMBLOB NOT NULL COMMENT '新闻内容',
PRIMARY KEY (news_content_id)
)ENGINE=InnoDB AUTO_INCREMENT=1000 DEFAULT CHARSET=utf8 COMMENT='新闻内容表';