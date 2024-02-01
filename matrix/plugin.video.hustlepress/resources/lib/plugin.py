# -*- coding: utf-8 -*-

from __future__ import unicode_literals

# noinspection PyUnresolvedReferences
from codequick import Route, Resolver, Listitem, utils, run
from codequick.utils import urljoin_partial, bold
import urlquick
import xbmcvfs
import xbmcaddon
import os
import resolveurl
import xbmc
from . import tools
from . import logger
from time import sleep as wait


STR = tools.getString
GS = tools.getSetting
SS = tools.setSetting

tools.setFont()

video_resolutions = ["240p", "360p", "480p", "720p(HD)", "1080p(FHD)", "1440p(QHD)", "2160p(4K)", "4320p(8K)"]
resolution_selected = GS("video_resolution")
video_resolution = video_resolutions.index(resolution_selected)
youtube_selected = GS("kodion.mpd.quality.selection","plugin.video.youtube")

SS("kodion.video.quality", 4, "plugin.video.youtube")
SS("kodion.video.quality.mpd", True, "plugin.video.youtube")
if youtube_selected == 4:
    SS("kodion.mpd.quality.selection", video_resolution, "plugin.video.youtube")

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
}
URL = "https://hustlepress.co.jp"
url_constructor = urljoin_partial(URL)

#Addon Start    
@Route.register
def root(plugin, content_type="segment"):
    item_data = [
        {"label":STR(30006), "linkpart":"/"},
        {"label":STR(30007), "linkpart":"/category/gravure/"},
        {"label":STR(30008), "linkpart":"/category/interview/"},
        {"label":STR(30009), "linkpart":"/category/feature/"},
        {"label":STR(30010), "linkpart":"/category/coumn/"},
    ]
    
    for data in item_data:
        item = Listitem()
        item.label = data["label"]
        linkpart = data["linkpart"]
        url = url_constructor(linkpart)
        item.set_callback(get_postlist, url=url)  
        yield item


@Route.register
def get_postlist(plugin, url):
    resp = urlquick.get(url, headers=headers, max_age=-1)
    postlistRoot = resp.parse("div",attrs={"class":"blogposts-wrapper clearfix"})
    postList = postlistRoot.iterfind("div/ul/li/div/a")
    
    for post in postList:
        item = Listitem()
        item.label = post.get("title")
        url = post.get("href")
        item.art["thumb"] = post.find("img").get("src")
        item.art["fanart"] = post.find("img").get("src")
        item.set_callback(media_List, url=url)
        yield item
        
    NextPageTree = resp.parse("div",attrs={"id":"blocks-left"})
    for page in NextPageTree.iterfind("div[@class='pagination clearfix']"):
        a_number = page.find("a").text
        span_number = page.find("span[@aria-current='page']").text
        a = int(a_number)
        span = int(span_number)
        if a == span + 1:
            nextPageP = page.find("a")
            yield Listitem.next_page(nextPage=nextPageP.get("href"),callback=get_Nextpostlist)
        elif a == span - 1:
            nextPageP = page.find("a[2]")
            yield Listitem.next_page(nextPage=nextPageP.get("href"),callback=get_Nextpostlist)
        elif a == span - 2:
            nextPageP = page.find("a[3]")
            yield Listitem.next_page(nextPage=nextPageP.get("href"),callback=get_Nextpostlist)    
        else:
            nextPageP = page.find("a[4]")
            yield Listitem.next_page(nextPage=nextPageP.get("href"),callback=get_Nextpostlist)     
              

@Route.register
def get_Nextpostlist(plugin,nextPage):
    resp = urlquick.get(nextPage, headers=headers, max_age=-1)
    postlistRoot = resp.parse("div",attrs={"class":"blogposts-wrapper clearfix"})
    postList = postlistRoot.iterfind("div/ul/li/div/a")
    
    for post in postList:
        item = Listitem()
        item.label = post.get("title")
        url = post.get("href")
        item.art["thumb"] = post.find("img").get("src")
        item.art["fanart"] = post.find("img").get("src")
        item.set_callback(media_List, url=url)
        yield item
        
    NextPageTree = resp.parse("div",attrs={"id":"blocks-left"})
    for page in NextPageTree.iterfind("div[@class='pagination clearfix']"):
        a_number = page.find("a").text
        span_number = page.find("span[@aria-current='page']").text
        a = int(a_number)
        span = int(span_number)
        if a == span + 1:
            nextPageP = page.find("a")
            yield Listitem.next_page(nextPage=nextPageP.get("href"),callback=get_Nextpostlist)
        elif a == span - 1:
            nextPageP = page.find("a[2]")
            yield Listitem.next_page(nextPage=nextPageP.get("href"),callback=get_Nextpostlist)
        elif a == span - 2:
            nextPageP = page.find("a[3]")
            yield Listitem.next_page(nextPage=nextPageP.get("href"),callback=get_Nextpostlist)    
        else:
            nextPageP = page.find("a[4]")
            yield Listitem.next_page(nextPage=nextPageP.get("href"),callback=get_Nextpostlist)
        

@Route.register
def media_List(plugin, url):
    resp = urlquick.get(url, headers=headers, max_age=-1)
    mediaRoot = resp.parse("div", attrs={"class": "post-content"})
    mediaList = mediaRoot.iterfind("div/div[3]")

    def create_item(name, video_url):
        item = Listitem()
        item.label = "{}: {}".format(STR(30011),name)
        id = video_url.replace("https://www.youtube.com/embed/", "")
        img = "https://img.youtube.com/vi/{}/sddefault.jpg".format(id)
        item.art["thumb"] = img
        item.art["fanart"] = img
        item.set_callback(play_Video, url=video_url)
        return item

    for media in mediaList:
        videosList = media.findall("div/iframe")
        videos_nameList = media.findall("h5")
        imagesList = media.findall("p/a/img")

        if not videos_nameList:
            for video in videosList:
                item = create_item(video.get("src").replace('https://www.youtube.com/embed/',''), video.get("src"))
                yield item
        else:
            for name, video in zip(videos_nameList, videosList):
                item = create_item(name.text, video.get("src"))
                yield item


        for img in imagesList:
            img_url = img.get("src")
            if img_url != "https://hustlepress.co.jp/img/webshop_bt.jpg":
                name_original = img_url.split('/')[-1].split('_')
                name_constructor = [name.capitalize() for name in name_original]
                name = ' '.join(name_constructor)
                gallery = resp.url.replace('https://hustlepress.co.jp/','').replace('/','')
                img_response = urlquick.get(img_url)
                img_content = img_response.content
                image = tools.downloadFile(name,gallery,img_content)

                item = Listitem()
                label = name.replace('.jpg','').replace('.gif','').replace('.png','')
                item.label = "{}: {}".format(STR(30012),label)
                album = image.replace(name,'')
                pic = image
                url = img_url
                item.art["thumb"] = image
                item.art["fanart"] = image
                item.set_callback(show_Images, album=album, pic=pic, url=img_url, label=label)
                yield item
                

@Resolver.register
def show_Images(plugin,album,pic,url,label):
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


@Resolver.register
def play_Video(plugin,url):
    url = url        
    resolved = resolveurl.resolve(url)
    return resolved
