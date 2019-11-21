import scrapy
import os
import cfscrape
import requests
import re
from bs4 import BeautifulSoup
import html.parser

from app.constants import EnvConstants as ec


class WatchList(scrapy.Spider):
    name = 'watchers'

    path = ec.TARGET_SITE + '/' + ec.PATH_WATCHLIST + '/' + ec.TARGET_USER + '/'

    cf_delay = 10
    session = requests.session()
    session.headers  = []

    def get_path(self):
        path = [ec.TARGET_SITE + '/' + ec.PATH_WATCHLIST + '/' + ec.TARGET_USER + '/',
                ec.TARGET_SITE + '/' + ec.PATH_WATCHLIST + '/' + ec.TARGET_USER + '/' + '2' + '/',
                ec.TARGET_SITE + '/' + ec.PATH_WATCHLIST + '/' + ec.TARGET_USER + '/' + '3' + '/',
                ec.TARGET_SITE + '/' + ec.PATH_WATCHLIST + '/' + ec.TARGET_USER + '/' + '4' + '/',
                ec.TARGET_SITE + '/' + ec.PATH_WATCHLIST + '/' + ec.TARGET_USER + '/' + '5' + '/',
                ec.TARGET_SITE + '/' + ec.PATH_WATCHLIST + '/' + ec.TARGET_USER + '/' + '6' + '/',
                ec.TARGET_SITE + '/' + ec.PATH_WATCHLIST + '/' + ec.TARGET_USER + '/' + '7' + '/',
                ec.TARGET_SITE + '/' + ec.PATH_WATCHLIST + '/' + ec.TARGET_USER + '/' + '8' + '/',
                ec.TARGET_SITE + '/' + ec.PATH_WATCHLIST + '/' + ec.TARGET_USER + '/' + '9' + '/',
                ec.TARGET_SITE + '/' + ec.PATH_WATCHLIST + '/' + ec.TARGET_USER + '/' + '10' + '/',
                ec.TARGET_SITE + '/' + ec.PATH_WATCHLIST + '/' + ec.TARGET_USER + '/' + '11' + '/',
        ]
        return path

    def cf_get_tokens(self):
        dblist = 'dblist_sql'
        # pull tokens from DB
        if dblist:
            sql = 'sql'
        else:
            cfscrape.get_cookie_string()
        pass

    def cf_login(self):
        pass

    def cf_scrape(self, path):
        scraper = cfscrape.create_scraper(delay=self.cf_delay)
        req = scraper.get(path)
        return req

    def soup_parser(self):
        raw_watchlist = []
        pathes = self.get_path()
        print('Pathes Complete')
        for path in pathes:
            req = self.cf_scrape(path=path)
            soup = BeautifulSoup(req.content, 'html.parser')
            raw_watchlist.append(list(soup.find_all("a", href=re.compile("/user/"))))
        print('Watchlist Complete')
        return raw_watchlist

    def soup_dict(self, watch_list):
        watch_dict = []
        for chunk in watch_list:
            for entry in chunk:
                user_path = entry.attrs['href']
                user_name = entry.string
                watch_dict.append({'user_name': user_name, 'user_path': user_path})
        print('Dict Complete')
        return watch_dict



# raw_watch = [<class 'list'>: [<a href="/user/-fang-/" target="_blank"><span class="artist_name">-Fang-</span></a>, <a href="/user/-mozg-/" target="_blank"><span class="artist_name">-mozg-</span></a>, <a href="/user/-ponca/" target="_blank"><span class="artist_name">-Ponca</span></a>, <a href="/user/-youbelionz-/" target="_blank"><span class="artist_name">-YOUbeLIONZ-</span></a>, <a href="/user/0goldstars/" target="_blank"><span class="artist_name">0Goldstars</span></a>, <a href="/user/12inchfallacy/" target="_blank"><span class="artist_name">12inchFallacy</span></a>, <a href="/user/1442899/" target="_blank"><span class="artist_name">1442899</span></a>, <a href="/user/1991vukxp/" target="_blank"><span class="artist_name">1991vukxp</span></a>, <a href="/user/1pie4me/" target="_blank"><span class="artist_name">1pie4me</span></a>, <a href="/user/20shadowflame17/" target="_blank"><span class="artist_name">20ShadowFlame17</span></a>, <a href="/user/3-apples/" target="_blank"><span class="artist_name">3-Apples</span></a>, <a href="/user/3815/" target="_blank"><span class="artist_name">3815</span></a>, <a href="/user/470/" target="_blank"><span class="artist_name">470</span></a>, <a href="/user/4lopo/" target="_blank"><span class="artist_name">4Lopo</span></a>, <a href="/user/57932/" target="_blank"><span class="artist_name">57932</span></a>, <a href="/user/622536as/" target="_blank"><span class="artist_name">622536as</span></a>, <a href="/user/7xwolfx7/" target="_blank"><span class="artist_name">7xWOLFx7</span></a>, <a href="/user/a-deer-is-fine-too/" target="_blank"><span class="artist_name">a-deer-is-fine-too</span></a>, <a href="/user/a.zippo/" target="_blank"><span class="artist_name">a.zippo</span></a>, <a href="/user/ableophiacodon/" target="_blank"><span class="artist_name">able_ophiacodon</span></a>, <a href="/user/abracon/" target="_blank"><span class="artist_name">Abracon</span></a>, <a href="/user/abyssa/" target="_blank"><span class="artist_name">Abyssa</span></a>, <a href="/user/aceoffate/" target="_blank"><span class="artist_name">ACEofFATE</span></a>, <a href="/user/acro/" target="_blank"><span class="artist_name">Acro</span></a>, <a href="/user/actaeon/" target="_blank"><span class="artist_name">Actaeon</span></a>, <a href="/user/actionhusky/" target="_blank"><span class="artist_name">Actionhusky</span></a>, <a href="/user/addler/" target="_blank"><span class="artist_name">Addler</span></a>, <a href="/user/adelindtiamat/" target="_blank"><span class="artist_name">AdelindTiamat</span></a>, <a href="/user/adelinesquiraffe/" target="_blank"><span class="artist_name">AdelineSquiraffe</span></a>, <a href="/user/adelulf/" target="_blank"><span class="artist_name">Adelulf</span></a>, <a href="/user/adirhaker/" target="_blank"><span class="artist_name">adirhaker</span></a>, <a href="/user/adl/" target="_blank"><span class="artist_name">ADL</span></a>, <a href="/user/adolph113/" target="_blank"><span class="artist_name">adolph113</span></a>, <a href="/user/adtrl/" target="_blank"><span class="artist_name">adtrl</span></a>, <a href="/user/adtuna1192/" target="_blank"><span class="artist_name">adtuna1192</span></a>, <a href="/user/adumbratio/" target="_blank"><span class="artist_name">Adumbratio</span></a>, <a href="/user/aduronf/" target="_blank"><span class="artist_name">AduroNF</span></a>, <a href="/user/aetos/" target="_blank"><span class="artist_name">aetos</span></a>, <a href="/user/af3110/" target="_blank"><span class="artist_name">AF3110</span></a>, <a href="/user/afallenwolf/" target="_blank"><span class="artist_name">aFallenWolf</span></a>, <a href="/user/ag-wolf/" target="_blank"><span class="artist_name">AG-Wolf</span></a>, <a href="/user/agentmoose/" target="_blank"><span class="artist_name">agentmoose</span></a>, <a href="/user/aguy09/" target="_blank"><span class="artist_name">aguy09</span></a>, <a href="/user/ahotewolf/" target="_blank"><span class="artist_name">ahotewolf</span></a>, <a href="/user/ahumeniy/" target="_blank"><span class="artist_name">ahumeniy</span></a>, <a href="/user/aidans/" target="_blank"><span class="artist_name">Aidans</span></a>, <a href="/user/aiden-g-shep/" target="_blank"><span class="artist_name">Aiden-G-shep</span></a>, <a href="/user/airblade/" target="_blank"><span class="artist_name">AirBlade</span></a>, <a href="/user/ak-akita/" target="_blank"><span class="artist_name">AK-Akita</span></a>, <a href="/user/ak4mloz/" target="_blank"><span class="artist_name">AK4mLOZ</span></a>, <a href="/user/akaitsuki1466/" target="_blank"><span class="artist_name">Akai_Tsuki1466</span></a>, <a href="/user/akajesse/" target="_blank"><span class="artist_name">akajesse</span></a>, <a href="/user/akasch/" target="_blank"><span class="artist_name">Akasch</span></a>, <a href="/user/akeluus/" target="_blank"><span class="artist_name">Akeluus</span></a>, <a href="/user/akita/" target="_blank"><span class="artist_name">Akita</span></a>, <a href="/user/akryon/" target="_blank"><span class="artist_name">Akryon</span></a>, <a href="/user/aksel/" target="_blank"><span class="artist_name">Aksel</span></a>, <a href="/user/akumatlt/" target="_blank"><span class="artist_name">Akuma_tlt</span></a>, <a href="/user/alako/" target="_blank"><span class="artist_name">alako</span></a>, <a href="/user/albw/" target="_blank"><span class="artist_name">ALBW</span></a>, <a href="/user/alec/" target="_blank"><span class="artist_name">alec</span></a>, <a href="/user/aleixter/" target="_blank"><span class="artist_name">Aleixter</span></a>, <a href="/user/alekneko/" target="_blank"><span class="artist_name">AlekNeko</span></a>, <a href="/user/alekthebeasty/" target="_blank"><span class="artist_name">AlekTheBeasty</span></a>, <a href="/user/alerkina4the5th/" target="_blank"><span class="artist_name">alerkina4the5th</span></a>, <a href="/user/alexander397/" target="_blank"><span class="artist_name">Alexander397</span></a>, <a href="/user/aliyna/" target="_blank"><span class="artist_name">Aliyna</span></a>, <a href="/user/alkymist/" target="_blank"><span class="artist_name">Alkymist</span></a>, <a href="/user/alpha103/" target="_blank"><span class="artist_name">alpha103</span></a>, <a href="/user/alphafenrir/" target="_blank"><span class="artist_name">alphafenrir</span></a>, <a href="/user/altair2056/" target="_blank"><span class="artist_name">Altair2056</span></a>, <a href="/user/alterhusky/" target="_blank"><span class="artist_name">AlterHusky</span></a>, <a href="/user/alvaro.shin/" target="_blank"><span class="artist_name">alvaro.shin</span></a>, <a href="/user/alvos/" target="_blank"><span class="artist_name">Alvos</span></a>, <a href="/user/amanda/" target="_blank"><span class="artist_name">Amanda</span></a>, <a href="/user/amariecoamenel/" target="_blank"><span class="artist_name">AmarieCoamenel</span></a>, <a href="/user/amaru/" target="_blank"><span class="artist_name">Amaru</span></a>, <a href="/user/amateurowl/" target="_blank"><span class="artist_name">Amateur_Owl</span></a>, <a href="/user/anaroseaperio/" target="_blank"><span class="artist_name">AnaroseAperio</span></a>, <a href="/user/andreawolf01/" target="_blank"><span class="artist_name">Andreawolf01</span></a>, <a href="/user/andrevvv/" target="_blank"><span class="artist_name">Andrevvv</span></a>, <a href="/user/andrewneo/" target="_blank"><span class="artist_name">AndrewNeo</span></a>, <a href="/user/andrewya/" target="_blank"><span class="artist_name">andrew_ya</span></a>, <a href="/user/androgymess/" target="_blank"><span class="artist_name">androgymess</span></a>, <a href="/user/androkei/" target="_blank"><span class="artist_name">AndroKei</span></a>, <a href="/user/andy/" target="_blank"><span class="artist_name">andy</span></a>, <a href="/user/andyvv/" target="_blank"><span class="artist_name">andyvv</span></a>, <a href="/user/ang3l/" target="_blank"><span class="artist_name">ANG3L</span></a>, <a href="/user/angelamylover/" target="_blank"><span class="artist_name">angelamylover</span></a>, <a href="/user/ankubus/" target="_blank"><span class="artist_name">ankubus</span></a>, <a href="/user/annexis/" target="_blank"><span class="artist_name">annexis</span></a>, <a href="/user/anomalocris/" target="_blank"><span class="artist_name">Anomalocris</span></a>, <a href="/user/antewolf/" target="_blank"><span class="artist_name">Antewolf</span></a>, <a href="/user/anthro-loewe/" target="_blank"><span class="artist_name">anthro-loewe</span></a>, <a href="/user/anthrootterperson/" target="_blank"><span class="artist_name">anthrootterperson</span></a>, <a href="/user/antoniusred/" target="_blank"><span class="artist_name">AntoniusRed</span></a>, <a href="/user/anxietydog/" target="_blank"><span class="artist_name">AnxietyDog</span></a>, <a href="/user/any121354324354/" target="_blank"><span class="artist_name">Any121354324354</span></a>, <a href="/user/aoshi2012/" target="_blank"><span class="artist_name">Aoshi2012</span></a>, <a href="/user/aosothnightwalker/" target="_blank"><span class="artist_name">Aosoth_Nightwalker</span></a>...]