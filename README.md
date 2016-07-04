# dandanspider
spider for dandanbbs of BNU

This project is only used to crawl http://www.oiegg.com/
The "bigspider.py" is used to crawl urls of boards and "myspider.py" crawl list and content of article.
  
We have three tables to store data:
  1.Table boards for all the boards ,including their url and name.
+-------+-------------+------+-----+---------+----------------+
| Field | Type        | Null | Key | Default | Extra          |
+-------+-------------+------+-----+---------+----------------+
| id    | bigint(20)  | NO   | PRI | NULL    | auto_increment |
| name  | varchar(50) | NO   |     | NULL    |                |
| url   | varchar(80) | NO   | UNI | NULL    |                |
+-------+-------------+------+-----+---------+----------------+
  2.Table list for all articles everyboard.
+--------+-------------+------+-----+------------+----------------+
| Field  | Type        | Null | Key | Default    | Extra          |
+--------+-------------+------+-----+------------+----------------+
| id     | bigint(20)  | NO   | PRI | NULL       | auto_increment |
| title  | varchar(80) | NO   |     | NULL       |                |
| url    | varchar(80) | NO   | UNI | NULL       |                |
| author | varchar(30) | NO   |     | NULL       |                |
| time   | date        | NO   |     | 2016-07-04 |                |
| reply  | int(11)     | NO   |     | 0          |                |
+--------+-------------+------+-----+------------+----------------+
  3.Table article for the content of articles.
+-------+-------------+------+-----+---------+----------------+
| Field | Type        | Null | Key | Default | Extra          |
+-------+-------------+------+-----+---------+----------------+
| id    | bigint(20)  | NO   | PRI | NULL    | auto_increment |
| url   | varchar(80) | NO   | UNI | NULL    |                |
| text  | text        | YES  |     | NULL    |                |
+-------+-------------+------+-----+---------+----------------+

And we have two steps to crawl:
  1.scrapy crawl bbs
  2.scrapy crawl bbs2
 
 It is notable that because of limits of authority, some article can't be read. Remember to change the user and password in const.py 
 when you use.
