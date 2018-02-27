# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging
import re
import MySQLdb
import urllib2
import platform
import time

class BtshoufaPipeline(object):

    def __init__(self):
        logging.critical("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!db connected!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        try:
            self.db = MySQLdb.connect(host="192.168.1.16",port=3306,user="root", passwd="root",
                         db="movies",charset="utf8")
        except Exception,ex:
            logging.critical(ex,exc_info=1)

    def checkIndb(self,title):
        cursor = self.db.cursor()
        sql="select title from btshoufa where title = '%s'" % (title)
        logging.critical(sql)
        try:
            res = cursor.execute(sql)
            return res
        except Exception,ex:
            logging.critical(("exception: %s")%ex,exc_info=1)
            return 0


    def insertIndb(self,seed, title):
        logging.critical("************************************insert db start************************************")
        cursor = self.db.cursor()
        t=time.asctime(time.localtime(time.time()))
        sql = "INSERT INTO btshoufa(url,title,insertTime) VALUES ('%s','%s','%s')" % (seed, title,t)
        try:
            cursor.execute(sql)
            self.db.commit()
        except Exception, ex:
            logging.critical(ex, exc_info=1)
            self.db.rollback()
        logging.critical("************************************insert db end************************************")

    def savetorrent(self,seed,title):
        if re.search(".torrent", title):
            logging.critical("title :%s,seed :%s"%(title,seed))
            res=self.checkIndb(title=title)
            if res == 0:
                self.insertIndb(seed, title)
            else:
                logging.critical("res is %s!!!!!!!!!!!this is in DB!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"%(res))
            try:
                f = urllib2.urlopen(seed,timeout=15)
                ts = "/home/siwei/torrent/"
                if platform.system() == "Darwin":
                    ts = "/Users/siwei/torrent/"
                tt = ts + title.strip()
                logging.critical("+++++++++++++++++read from net start++++++++++++++")
                torrent=f.read()
                logging.critical("+++++++++++++++++read ended++++++++++++++++++++++++")
                logging.critical("*****************write file start*******************")
                with open(tt, "wb") as code:
                    code.write(torrent)
                logging.critical("*****************write file end*******************")
            except Exception,e:
                logging.critical(e)


            #logging.critical("*****************savetorrent end*****

    def close_spider(self):
        logging.critical("close db!!!!!!!!!!")
        self.db.close()

    def process_btshoufaspider(self,item):
        if 'title' in item and 'seed' in item:
            title=item['title'][0]
            seed=item['seed'][0]
            if re.match("http://www.btshoufa.net/forum.php\?mod=attachment",seed):
                #seed="http://www.btshoufa.net/"+seed
                logging.critical("%s----------BtshoufaPipeline------------->%s"%(title,seed))
                self.savetorrent(seed,title)
        elif 'seed' in item:
            seed=item['seed'][0]
            title="unknown"
            self.savetorrent(seed,title)


    def process_item(self, item, spider):
        if spider.name == "btshoufaspider":
            self.process_btshoufaspider(item)
        return item
