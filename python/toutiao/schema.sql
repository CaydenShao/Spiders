-- 创建数据库
CREATE DATABASE large_data;

USE large_data;

CREATE TABLE news(
news_id BIGINT NOT NULL AUTO_INCREMENT COMMENT '新闻id',
type VARCHAR NOT NULL COMMENT '新闻类型',
title VARCHAR NOT NULL COMMENT '新闻标题',
media_url VARCHAR COMMENT '源媒体',
media_avatar_img VARCHAR COMMENT '源媒体头像',
media_name COMMENT '原媒体名称',
comment_count BIGINT COMMENT '评论数量',
article_img VARCHAR COMMENT '新闻标题图片',
article_url VARCHAR COMMENT '新闻源链接',
mark VARCHAR COMMENT '标签(用空格隔开)',
crawl_time TIMESTAMP NOT NULL COMMENT '爬取时间',
crawl_origin VARCHAR COMMENT '爬取源（如头条）',
crawl_url VARCHAR COMMENT '爬取源url(如https://www.toutiao.com/ch/news_hot/)',
PRIMARY KEY (news_id),
INDEX idx_crawl_time(crawl_time(length)),
INDEX idx_artical_url(artical_url)
);

CREATE TABLE news_content(
news_content_id BIGINT NOT NULL AUTO_INCREMENT COMMENT '新闻内容id',
news_url VARCHAR NOT NULL COMMENT '新闻源链接',
content MEDIUMBLOB NOT NULL COMMENT '新闻内容',
PRIMARY KEY (artical_content_id),
KEY idx_artical_url(artical_url)
);