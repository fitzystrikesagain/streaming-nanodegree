BEGIN TRANSACTION;

CREATE TABLE IF NOT EXISTS clicks
(
    id        INTEGER not null PRIMARY KEY,
    email     CHARACTER VARYING(100),
    timestamp CHARACTER VARYING(100),
    uri       CHARACTER VARYING(512),
    number    INTEGER
);

INSERT INTO clicks
VALUES (1, 'courtney29@yahoo.com', '2014-10-31 15:10:56', 'http://daniels.org/search/login.html', 26),
       (2, 'longmary@duran.com', '1984-11-30 15:32:50', 'https://huff-pacheco.net/privacy.htm', 21),
       (3, 'mariamason@gmail.com', '1998-09-08 16:46:09', 'https://www.carroll-hill.net/author/', 77),
       (4, 'gwhite@robertson.com', '1974-03-21 04:31:40', 'http://www.swanson.info/tags/category/blog/home).jsp', 59),
       (5, 'david90@hotmail.com', '2009-10-20 01:08:22', 'https://www.marquez-cruz.com/', 85),
       (6, 'jeremy54@hotmail.com', '1992-04-29 04:25:05', 'http://carter-wilson.com/', 74),
       (7, 'lanecorey@yahoo.com', '2009-11-03 17:52:29', 'https://schneider.com/posts/tags/login.htm', 17),
       (8, 'joshuacolon@clark.com', '1982-08-08 12:57:44', 'http://www.daniels.com/privacy/', 18),
       (9, 'qpowers@white.com', '2011-02-07 09:24:29', 'https://www.wells-valdez.com/author/', 64),
       (10, 'rwright@gmail.com', '2017-06-01 23:02:51', 'http://www.taylor.com/post/', 47),
       (11, 'susan25@yahoo.com', '1981-08-24 15:55:03', 'https://collins.com/register.html', 57),
       (12, 'btyler@james.com', '1992-06-04 07:23:47', 'http://mcdonald.org/app/homepage/', 4),
       (13, 'cevans@ellis.com', '1991-09-25 15:44:01', 'https://mendoza.com/search/blog/list/privacy.asp', 11),
       (14, 'uanderson@hotmail.com', '1986-08-09 11:19:01',
        'https://www.stevens-myers.com/blog/category/b)log/privacy/', 85),
       (15, 'matthew54@gmail.com', '1992-08-26 01:30:55', 'http://www.clayton.net/login/', 90),
       (16, 'jenniferfoster@lopez-pham.com', '1983-01-10 14:32:42', 'https://www.salinas.com/app/category/)blog/login/',
        76),
       (17, 'wsmith@hotmail.com', '1989-11-06 14:22:10', 'http://jones.com/main/search.php', 20),
       (18, 'lopezdaniel@hotmail.com', '1978-10-28 06:01:56', 'https://www.schultz-henry.com/category/inde)x.htm', 73),
       (19, 'pbarry@sanders-calderon.biz', '1974-05-12 20:04:01', 'https://ware.com/wp-content/tags/homepa)ge/', 40),
       (20, 'christine14@davis-singleton.com', '2017-11-10 11:11:41', 'http://www.smith.com/category/', 26);

COMMIT;
