# -*- coding: utf-8 -*-

from __future__ import unicode_literals

# noinspection PyUnresolvedReferences
from codequick import Route, Resolver, Listitem, utils, run
from codequick.utils import urljoin_partial, bold
import urlquick
import xbmcgui
from . import logger #logger.debug(FUNCION O VARIABLE A DEBUGUEAR)
from . import tools
import resolveurl
import xbmc
import xbmcvfs
import os
import json
from time import sleep as wait


STR = tools.getString
GS = tools.getSetting
SS = tools.setSetting

tools.setFont()

video_resolutions = ["240p", "360p", "480p", "720p(HD)", "1080p(FHD)", "1440p(QHD)", "2160p(4K)", "4320p(8K)", "Auto"]
resolution_selected = GS("video_resolution")
video_resolution = video_resolutions.index(resolution_selected)
youtube_selected = GS("kodion.mpd.quality.selection","plugin.video.youtube")
inputstream_selected = GS("adaptivestream.res.max","inputstream.adaptive")

SS("kodion.video.quality", 4, "plugin.video.youtube")
SS("kodion.video.quality.mpd", True, "plugin.video.youtube")
if youtube_selected == 4:
    SS("kodion.mpd.quality.selection", video_resolution, "plugin.video.youtube")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Referer": "https://www.ariyasumomoka.jp/",
}

URL = "https://www.ariyasumomoka.jp"
url_constructor = urljoin_partial(URL)
s = urlquick.Session()

@Route.register
def root(plugin, content_type="segment"):
    menu_items = [
        {"label": STR(30006), "callback": get_photos, "linkpart": "/photography/"},
        {"label": STR(30007), "callback": get_videos, "linkpart": "/movie/"},
        {"label": STR(30008), "callback": get_albums, "linkpart": "/discography/"},
    ]
    
    for item_data in menu_items:
        item = Listitem()
        item.label = item_data["label"]
        url = url_constructor(item_data["linkpart"])
        item.set_callback(item_data["callback"], url=url)
        yield item

   
@Route.register
def get_videos(plugin, url):
    resp = s.get(url, headers=headers)
    videosRoot = resp.parse("ul", attrs={"class": "movie-index"})
    videoslist = videosRoot.iterfind("li/a")

    for elem in videoslist:
        item = Listitem()
        item.label = elem.find("div").text
        linkpart = elem.get("href")
        url = url_constructor("/movie/" + linkpart)
        img = elem.find("figure/img").get("src")
        item.art["thumb"] = url_constructor(img)
        item.art["fanart"] = url_constructor(img)
        item.set_callback(data_Video, url=url, img=img)
        yield item

    NextPageTree = resp.parse("div",attrs={"class":"parts-pager-index"})
    for page in NextPageTree.iterfind("a[5]"):
        next_url = url_constructor("/movie/{}".format(page.get("href")))
        yield Listitem.next_page(nextPage=next_url,callback=get_Nextvideos)


@Route.register
def get_Nextvideos(plugin, nextPage):
    resp = s.get(nextPage, headers=headers, max_age=-1)
    videosRoot = resp.parse("ul", attrs={"class": "movie-index"})
    videoslist = videosRoot.iterfind("li/a")

    for elem in videoslist:
        item = Listitem()
        item.label = elem.find("div").text
        linkpart = elem.get("href")
        url = url_constructor("/movie/" + linkpart)
        img = elem.find("figure/img").get("src")
        item.art["thumb"] = url_constructor(img)
        item.art["fanart"] = url_constructor(img)
        item.set_callback(data_Video, url=url, img=img)
        yield item

    NextPageTree = resp.parse("div",attrs={"class":"parts-pager-index"})
    for page in NextPageTree.iterfind("a[5]"):
        next_url = url_constructor("/movie/{}".format(page.get("href")))
        yield Listitem.next_page(nextPage=next_url,callback=get_Nextvideos)

             
@Route.register
def get_photos(plugin, url):
    resp = s.get(url, headers=headers, max_age=-1)
    photosRoot = resp.parse("ul", attrs={"class": "bio__content-list"})
    photoslist = photosRoot.iterfind("li/img")
    
    for photo in photoslist:
        url = url_constructor(photo.get("src"))
        gallery = resp.url.replace('https://www.ariyasumomoka.jp/','').replace('/','')
        img = url.replace('https://www.ariyasumomoka.jp/images/bio/','')
        image_response = urlquick.get(url)
        image_content = image_response.content
        image = tools.downloadFile(img,gallery,image_content)
        
        item = Listitem()
        item.label = img.replace('.jpg','')
        album = image.replace(img,'')
        pic = image
        item.art["thumb"] = image
        item.art["fanart"] = image
        item.set_callback(show_Photos, album=album, pic=pic, url=url, label=item.label)
        yield item


@Route.register
def data_Video(plugin, url, img):
    img = url_constructor(img)
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"}
    resp = s.get(url, headers=headers)
    page_root = resp.parse("div", attrs={"class":"wrap"})
    page_elems = page_root.iterfind("div")

    for elem in page_elems:
        item = Listitem()
        item.label = elem.find("h3").text
        url = elem.find("div/div/iframe").get("src")
        item.art["thumb"] = img
        item.art["fanart"] = img
        item.set_callback(play_Video, url=url)
        yield item


@Resolver.register
def show_Photos(plugin,album,pic,url,label):
    album = album
    url = url
    xbmc.executebuiltin("ShowPicture({})".format(pic))
    wait(5)
    xbmc.executebuiltin("SlideShow({})".format(album))
    plugin = plugin.extract_source(url)
    return Listitem().from_dict(**{
        "label" : label,
        "callback" : plugin,
    })


@Route.register
def get_albums(plugin,url):
    resp = s.get(url, headers=headers, max_age=-1)
    albumsRoot = resp.parse("div", attrs={"class": "wrap"})
    albumslist = albumsRoot.iterfind("ul")
    
    for elem in albumslist:
        album_info = [
            {"label": elem.find("li/span").text, "linkpart": "/discography/"},
            {"label": elem.find("li/a").text, "linkpart": elem.find("li/a").get("href")},
            {"label": elem.find("li[3]/a").text, "linkpart": elem.find("li[3]/a").get("href")},
            {"label": elem.find("li[4]/a").text, "linkpart": elem.find("li[4]/a").get("href")},
            {"label": elem.find("li[5]/a").text, "linkpart": elem.find("li[5]/a").get("href")},
            {"label": elem.find("li[6]/a").text, "linkpart": elem.find("li[6]/a").get("href")},
            ]
            
        for album in album_info:
            item = Listitem()
            item.label = album["label"]
            linkpart = album["linkpart"]
            url = url_constructor(linkpart)
            item.set_callback(albums_List, url=url)
            yield item
        

@Route.register
def albums_List(plugin, url):
    resp = s.get(url, headers=headers, max_age=-1)
    try:
        albumsRoot = resp.parse("div", attrs={"class": "disco-index__list"})
        albumslist = albumsRoot.iterfind("ul/li/a")
        
        for album in albumslist:
            item = Listitem()
            item.label = album.find("div[2]").text
            linkpart = album.get("href").replace('.','/discography/')
            url = url_constructor(linkpart)
            img = album.find("figure/img").get("src")
            item.art["thumb"] = url_constructor(img)
            item.art["fanart"] = url_constructor(img)
            item.set_callback(album_Page, url=url)
            yield item
    except RuntimeError as error:
        xbmcgui.Dialog().ok(STR(30011), STR(30012))
        xbmc.executebuiltin('Dialog.Close(all,true)')
        
        
@Route.register
def album_Page(plugin, url):
    resp = s.get(url, headers=headers, max_age=-1)
    albumRoot = resp.parse("div", attrs={"class": "wrap"})
    albumElems = albumRoot.iterfind("div/div")
    
    for elem in albumElems:
        item = Listitem()
        item.label = elem.find("div[2]/h3").text
        img = elem.find("div/div/div/img").get("src")
        item.art["thumb"] = url_constructor(img)
        item.art["fanart"] = url_constructor(img)
        emptyAlbums = ["『有安杏果 サクライブ 2019 ～Another story～』Live Blu-ray&DVD", "有安杏果写真集『ヒカリの声』", "ライフスタイル本『Happy Holidays』", "有安杏果 サクライブ 2019 ～Another story～"]

        if item.label == "『有安杏果 Pop Step Zepp Tour 2019』Live Blu-ray&DVD":
            url = elem.find("div[2]/div[3]/a").get("href")
            item.set_callback(enter_AlbumPopSZT2019, url=url)
            yield item
        elif item.label == "有安杏果 Pop Step Zepp Tour 2019":
            url = elem.find("div[2]/div[3]/a[2]").get("href")
            item.set_callback(enter_AlbumPopSZT2019, url=url)
            yield item
        else:
            try:
                url = elem.find("div[2]/div[3]/a[2]").get("href")
                item.set_callback(enter_AlbumVideo, url=url)
                yield item
            except AttributeError as error:
                logger.debug(error)
                xbmcgui.Dialog().ok(STR(30014), STR(30015))
                xbmc.executebuiltin('Dialog.Close(all,true)')


@Route.register
def enter_AlbumVideo(plugin, url):
    resp = s.get(url, headers=headers, max_age=-1)
    videosRoot = resp.parse("section", attrs={"class": "section section--v1"})
    videosElems = videosRoot.iterfind("div/div/div/div/div/iframe")
    
    counter = 1
    for elem in videosElems:
        item = Listitem()
        item.label = "{} {}".format(STR(30013),str(counter))
        url = elem.get("src")
        id = url.replace('https://www.youtube.com/embed/','')
        img = "https://img.youtube.com/vi/{}/sddefault.jpg".format(id)
        item.art["thumb"] = img
        item.art["fanart"] = img
        item.set_callback(play_Video, url=url)
        counter += 1
        yield item   
        
            
@Route.register
def enter_AlbumPopSZT2019(plugin, url):
    resp = s.get(url, headers=headers, max_age=-1)
    videosRoot = resp.parse("div", attrs={"class": "movie"})
    videosElems = videosRoot.iterfind("div/div/div/iframe")
    
    counter = 1
    for elem in videosElems:
        item = Listitem()
        item.label = "{} {}".format(STR(30013),str(counter))
        url = elem.get("src")
        id = url.replace('https://www.youtube.com/embed/','')
        img = "https://img.youtube.com/vi/{}/sddefault.jpg".format(id)
        item.art["thumb"] = img
        item.art["fanart"] = img
        item.set_callback(play_Video, url=url)
        counter += 1
        yield item
        

@Resolver.register
def play_Video(plugin, url):    
    if not "https://player.vimeo.com/video/" in url:
        url = url
        resolved = resolveurl.resolve(url)
        logger.debug(resolved)
        return resolved
    else:
        id = url.split('video/')[1].split('?')[0]
        url = "{}$${}".format(url.split('?')[0],headers["Referer"])
        resolved = resolveurl.resolve(url)
        
        properties = {"inputstream" : "inputstream.adaptive","inputstream.adaptive.manifest_type" : "hls"}
        item = {"callback": resolved, "label": f"Vimeo ID: {id}", "properties": properties}
        listitem = Listitem.from_dict(**item)
        return listitem



    
    
   
