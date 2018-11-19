-- 创建数据库
CREATE DATABASE large_data;

USE large_data;

-- 创建新闻项表
CREATE TABLE news(
    news_id BIGINT NOT NULL AUTO_INCREMENT COMMENT '新闻id',
    type VARCHAR(120) NOT NULL COMMENT '新闻类型',
    title VARCHAR(120) NOT NULL COMMENT '新闻标题',
    media_url VARCHAR(512) COMMENT '源媒体（创建者的主页）',
    media_avatar_img VARCHAR(512) COMMENT '源媒体头像',
    media_name VARCHAR(120) COMMENT '原媒体名称',
    comment_count BIGINT COMMENT '评论数量',
    article_img VARCHAR(512) COMMENT '新闻标题图片',
    article_url VARCHAR(512) COMMENT '新闻内容源链接',
    article_url_md5 VARCHAR(64) UNIQUE COMMENT '新闻内容原链接MD5值',
    mark VARCHAR(120) COMMENT '标签(用,隔开)',
    crawl_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '爬取时间',
    crawl_origin VARCHAR(120) COMMENT '爬取源（如头条）',
    crawl_url VARCHAR(512) COMMENT '爬取源url(如https://www.toutiao.com/ch/news_hot/)',
    PRIMARY KEY (news_id)
)ENGINE=InnoDB AUTO_INCREMENT=1000 DEFAULT CHARSET=utf8 COMMENT='新闻项';

-- 创建新闻文章内容表
CREATE TABLE news_content(
    news_content_id BIGINT NOT NULL AUTO_INCREMENT COMMENT '新闻内容id',
    news_id BIGINT NOT NULL COMMENT '新闻id',
    target_url VARCHAR(512) NOT NULL COMMENT '新闻内容目标链接（因为可能有重定向）',
    article_origin INT NOT NULL COMMENT '文章来源，如1表示今日头条',
    content LONGTEXT NOT NULL COMMENT '新闻内容',
    crawl_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '爬取时间',
    PRIMARY KEY (news_content_id),
    FOREIGN KEY(news_id) REFERENCES news(news_id)
)ENGINE=InnoDB AUTO_INCREMENT=1000 DEFAULT CHARSET=utf8 COMMENT='新闻内容表';

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

-- 创建图片分组表
CREATE TABLE picture_group
(
    picture_group_id BIGINT NOT NULL AUTO_INCREMENT COMMENT '图片分组id',
    title VARCHAR(120) COMMENT '图片分组标题、描述',
    mark VARCHAR(120) COMMENT '标签(用,隔开)',
    PRIMARY KEY (picture_group_id)
)ENGINE=InnoDB AUTO_INCREMENT=1000 DEFAULT CHARSET=utf8 COMMENT='图片项';

-- 创建图片分组映射表
CREATE TABLE picture_group_relationships
(
    picture_id BIGINT NOT NULL COMMENT '图片id，外键，对应picture表的picture_id',
    picture_group_id BIGINT NOT NULL COMMENT '图片分组id，外键，对应表picture_group_id',
    FOREIGN KEY(picture_id) REFERENCES picture(picture_id),
    FOREIGN KEY(picture_group_id) REFERENCES picture_group(picture_group_id)
)ENGINE=InnoDB AUTO_INCREMENT=1000 DEFAULT CHARSET=utf8 COMMENT='图片项';

-- 创建图片项表
CREATE TABLE video
(
    video_id BIGINT NOT NULL AUTO_INCREMENT COMMENT '视频id',
    type VARCHAR(120) NOT NULL COMMENT '视频类型',
    title VARCHAR(120) COMMENT '视频标题、描述',
    media_url VARCHAR(512) COMMENT '源媒体（创建者的主页）',
    media_avatar_img VARCHAR(512) COMMENT '源媒体头像',
    media_name VARCHAR(120) COMMENT '原媒体名称',
    comment_count BIGINT COMMENT '评论数量',
    thumbs_up_times BIGINT COMMENT '点赞、喜欢或推荐等次数',
    video_img VARCHAR(512) COMMENT '视频图片',
    video_url VARCHAR(512) COMMENT '视频链接',
    video_url_md5 VARCHAR(64) UNIQUE COMMENT '视频链接MD5值',
    mark VARCHAR(120) COMMENT '标签(用,隔开)',
    crawl_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '爬取时间',
    crawl_origin VARCHAR(120) COMMENT '爬取源（如头条）',
    crawl_url VARCHAR(512) COMMENT '爬取源url(如https://www.toutiao.com/ch/news_hot/)',
    PRIMARY KEY (video_id)
)ENGINE=InnoDB AUTO_INCREMENT=1000 DEFAULT CHARSET=utf8 COMMENT='视频项';