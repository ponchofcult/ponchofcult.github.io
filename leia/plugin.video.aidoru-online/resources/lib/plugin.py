# -*- coding: utf-8 -*-

from __future__ import unicode_literals

# noinspection PyUnresolvedReferences
from codequick import Route, Resolver, Listitem, utils, run
from codequick.utils import urljoin_partial, bold
import requests
import xbmcgui
from bs4 import BeautifulSoup as bs
from . import logger #logger.debug(FUNCION O VARIABLE A DEBUGUEAR)
from . import tools
import xbmc
import xbmcaddon
import xbmcvfs
import sys
import urllib.parse as urllib
from random import uniform
from time import sleep as wait
from PIL import Image
import shutil

STR = tools.getString

addonID = xbmcaddon.Addon().getAddonInfo('id')
repoContainer = xbmcvfs.translatePath('special://home/addons/{}/resources/lib/{}')
path = xbmcvfs.translatePath('special://home/addons/{}')
torrent_addons = ["Elementum","Torrest"]
torrent_addons_selection = ["Elementum: {}".format(STR(30045)), "Torrest: {}".format(STR(30046))]

torrent_player = tools.getSetting("torrent_player")
if not torrent_player.strip():
    selection = xbmcgui.Dialog().select(STR(30047), torrent_addons_selection, useDetails=True)
    xbmcaddon.Addon().setSetting("torrent_player", torrent_addons[selection])

if tools.getSetting("torrent_player") == "Elementum":
    try:
        root = xbmcaddon.Addon('plugin.video.elementum').getSetting('download_path').strip()
        xbmcaddon.Addon("plugin.video.elementum").setSetting("download_file_strategy","2")
        xbmcaddon.Addon("plugin.video.elementum").setSettingBool("silent_stream_start",True)
        xbmcaddon.Addon("plugin.video.elementum").setSettingInt("buffer_timeout",600)
        if root == "" or root == "/":
            xbmcaddon.Addon("plugin.video.elementum").setSetting("download_path","special://home/cache/elementum/")
    except Exception as e:
        sys.exit()

username = tools.getSetting("username")
password = tools.getSetting("password")

url = "https://aidoru-online.me/"
url_constructor = urljoin_partial(url)
url = url_constructor(url)
s = requests.session()
some_time = uniform(1000, 5000)
sleep = xbmc.sleep

cookies = 'flog=6; ufp={}'.format(tools.mixCharacters(32))
user_agent = tools.mixUserAgents()
headers = {
    'authority': 'aidoru-online.me',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'origin': 'https://aidoru-online.me',
    'content-type': 'application/x-www-form-urlencoded',
    'user-agent': user_agent,
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'referer': 'https://aidoru-online.me/login.php',
    'accept-language': 'es-419,es;q=0.9,en;q=0.8',
    'cookie': cookies,
}

params = (
    ('type', 'login'),
)

data = {
  'username': username,
  'password': password,
  'do': 'login',
  'language': 'en'
}

_url = url_constructor("login.php?type=login")
response = s.post(_url, headers=headers, data=data)
sleep(int(some_time))


@Route.register
def root(plugin, content_type="segment"):
    resp = bs(s.get(url).text, 'html.parser')
    sleep(int(some_time))
    if resp.contents == []:
        xbmcgui.Dialog().ok(STR(30005), STR(30006))
        xbmcaddon.Addon().openSettings()
    else:
        logged_Content = resp.find_all(class_="infobar")
        for loginfo in logged_Content: 
            if not "You are logged in as: {}".format(username) in str(loginfo):
                xbmcgui.Dialog().ok(STR(30005), STR(30006))
                xbmcaddon.Addon().openSettings()
            else:
                pass
    
    item = Listitem()
    item.label = "{}: {}".format(STR(30007),tools.getSetting("username").upper())
    yield item

    item = Listitem()
    item.label = STR(30008)
    item.set_callback(search_Content)
    yield item

    categories = [
        (STR(30009),"Show+All"),
        ("48 Group Family","48G"),
        ("Hello! Project","H!P"),
        ("Stardust Promotion","Stardust"),
        (STR(30044),"Other")]

    for pcat in categories:
        item = Listitem()
        item.label = pcat[0]
        linkpart = "get_ttable.php?pcat={}&typ=both".format(pcat[1])
        pcat_url = url_constructor(linkpart)
        item.set_callback(sub_Categories, pcat_url=pcat_url)
        yield item


@Route.register
def sub_Categories(plugin, pcat_url):
    subcategories = [
        (STR(30009), "&scat=&subbed=&fl=&resd=&p=0&searchstr=&deadlive=1"),
        (STR(30010), "&scat=1"),
        (STR(30011), "&scat=2"),
        (STR(30012), "&scat=3"),
        (STR(30013), "&scat=4"),
        (STR(30014), "&scat=5"),
        (STR(30015), "&scat=6"),
        (STR(30016), "&scat=7"),
        (STR(30017), "&scat=8"),
        (STR(30018), "&scat=9"),
        (STR(30019), "&scat=10"),
        (STR(30020), "&scat=11"),
        (STR(30021), "&scat=12"),
        (STR(30022), "&subbed=1"),
        (STR(30023), "&fl=1"),
        (STR(30024), "&resd=1"),    
    ]

    for scat in subcategories:
        item = Listitem()
        item.label = scat[0]
        scat_url = url_constructor("{}{}".format(pcat_url, scat[1]))
        item.set_callback(all_Content, scat_url=scat_url)
        yield item


@Route.register
def all_Content(plugin, scat_url):
    # Construimos la URL, con BeautifulSoup la parseamos y buscamos todos los elementos con class="t-row", cada elemento es un Concierto.
    _url = url_constructor(scat_url)
    resp = bs(s.get(_url).text, 'html.parser')
    root_Content = resp.find_all(class_="t-row")
     
     # Buscamos como punto de referencia en cada elemento de la lista root_Content el elemento con etiqueta td y valign="middle"
     # Saltamos al vecino siquiente con etiqueta td y en "a" encontramos el title y la url
     # IMPORTANTE: Despues, para poder añadir miniaturas volvemos a parsear con BeautifulSoup el link al post del torrent, la "url". Buscamos todos los fanart con class="image-link" y thumbnails con class="torrent-image"

    for elem in root_Content:
        item = Listitem()
        elem_router = elem.find("td", valign="middle")
        item.label = elem_router.find_next_sibling("td").find("a").get("title")
        url = url_constructor(elem_router.find_next_sibling("td").find("a").get("href"))
        img = bs(s.get(url).text, 'html.parser')
        fanarts = img.find_all(class_="image-link")
        thumbnails = img.find_all(class_="torrent-image")
        
        # Obtenemos las URL de las imagenes y sustituimos unos valores para que esten en la mejor calidad posible
        for art in fanarts:
            img_link = art.get("src").replace('640x480q90', '4032x3024q90').replace('/th/','/img/')
            item.art['fanart'] = img_link
        for thumb in thumbnails:
            img_link = thumb.get("data-imgurl").replace('640x480q90', '4032x3024q90')
            item.art['thumb'] = img_link
        item.set_callback(details_Content, url=url, label=item.label, scat_url=scat_url)
        yield item 
        
    # Para ir a la siguiente pagina encontramos todas las etiquetas "p" con align="center" y de esa lista buscamos el ultimo elemento con etiqueta "a" con class="page-link" y adquirimos el numero de data-pagenum
    # Construimos la URL y la pasamos a la siguiente funcion

    NextPageTree = resp.find_all("p", align="center")
    for page in NextPageTree:
        try:
            nextPageP = page.find_all("a", class_="page-link")
            for data_pagenum in nextPageP:
                if 'Next' in data_pagenum.text:
                    nextPage=url_constructor("{}&p={}".format(_url,data_pagenum.get("data-pagenum")))
                    dp = data_pagenum.get("data-pagenum")

                    pag = int(dp) - 1 # Cambia este valor según la página que quieras mostrar
                    art_pag = 30 # Este valor es constante
                    start = pag * art_pag + 1 # El primer artículo de la página actual
                    end = start + art_pag - 1 # El último artículo de la página actual
                    next_start = end + 1 # El primer artículo de la página siguiente
                    next_end = next_start + art_pag - 1 # El último artículo de la página siguiente

                    # Usando el método format() para crear la cadena con los valores calculados
                    item = Listitem()
                    item.label = "{} | {}-{} | {} >> {} | {}-{}".format(str(pag), str(start), str(end), STR(30025), str(pag+1) ,str(next_start), str(next_end))
                    item.set_callback(all_Content, scat_url=nextPage)
                    yield item

                    item = Listitem()
                    item.label = STR(30026)
                    item.set_callback(page_Finder, url=_url)
                    yield item
        
        except IndexError:
            pass
    
       
@Route.register
def details_Content(plugin,url,label,scat_url):
    label = label
    # Construimos la URL y buscamos las imagenes.
    link = s.get(url_constructor(url))
    sleep(int(some_time))
    resp = bs(link.text, 'html.parser')
    covers = resp.find_all(class_="image-link")
    images = resp.find_all(class_="torrent-image")
    #Buscamos como referencia la etiqueta con id ty-button y en el div anterior obtenemos el enlace href al archivo Torrent que se encuentra en 'a'
    url_router = resp.find(id="ty-button")
    url = url_constructor(url_router.find_previous_sibling("div").find("a").get("href"))
    # Obtenemos el contenido, el nombre y el nombre del post para nombrar la locacion
    # Descargamos el archivo Torrent
    tor_content = s.get(url).content
    sleep(int(some_time))
    tor_name = s.get(url).headers.get("Content-Disposition").split('filename=')[1].replace('"','')
    sleep(int(some_time))
    tor_loc = link.url.split('=')[1]
    torrent = tools.downloadFile(tor_name,tor_loc,tor_content)
    img_path = torrent.replace(tor_name,"images\{}".format(""))
    
    item = Listitem()
    if tools.getSetting("torrent_player") == "Elementum":
        if "&scat=7" in scat_url:
            item.label = "{} {}".format(STR(30051),tor_name.replace('.torrent',''))
            item.set_callback(torrent_Images, torrent=torrent, img_path=img_path, url=link.url, label=label, scat_url=scat_url)
        else:
            item.label = tor_name.replace('.torrent','')
            uri = "plugin://plugin.video.elementum/play/?uri={}".format(urllib.quote_plus(torrent, safe=''))
            item.set_path(uri)
    elif tools.getSetting("torrent_player") == "Torrest":
        if "&scat=7" in scat_url:
            item.label = "{} {}".format(STR(30051),tor_name.replace('.torrent',''))
            item.set_callback(torrent_Images, torrent=torrent, img_path=img_path, url=link.url, label=label, scat_url=scat_url)
        else:
            item.label = tor_name.replace('.torrent','')
            uri = "plugin://plugin.video.torrest/play_path?path={}".format(torrent)
            item.set_path(uri)
    item.art['thumb'] = "https://cdn.icon-icons.com/icons2/1508/PNG/512/bittorrent_103937.png"
    yield item
    
    #Despues de buscar, obtener y renombrar la url, obtenemos el nombre de la imagen, el id del post, el contenido de la imagen y la descargamos
    for image in covers + images:
        if image in covers:
            url = image.get("src").replace('640x480q90', '4032x3024q90').replace('/th/','/img/')
        else:
            url = image.get("data-imgurl").replace('640x480q90', '4032x3024q90').replace('/th/','/img/')
 
        img_content = s.get(url).content
        sleep(int(some_time))
        img_name = "{}.jpg".format(url.split("/")[-1].replace('.jpg',''))
        img_gallery = "{}/images/".format(link.url.split('=')[1])
        image_file = tools.downloadFile(img_name, img_gallery, img_content)

    album = image_file.replace(img_name,'')
    all_elems = xbmcvfs.listdir(album)
    all_images = all_elems[1]
    
    for image in all_images:
        item = Listitem()
        pic = "{}{}".format(album,image)
        item.art['thumb'] = pic
        item.art['fanart'] = pic
        if image.endswith(('.jpg','.jpeg', '.jfif', '.png', '.tif', '.tiff', '.gif', '.bmp', '.heif', '.raw')):
            item.label = "{} {}".format(STR(30028),image).replace('.jpg','').replace('.jpeg','').replace('.jfif','').replace('.png','').replace('.tif','').replace('.tiff','').replace('.gif','').replace('.bmp','').replace('.heif','').replace('.raw','')
            item.set_callback(show_Photos, album=album, pic=pic, url=url, label=item.label, uri="")   
        else:
            item.label = image
            if tools.getSetting("torrent_player") == "Elementum":
                uri = "plugin://plugin.video.elementum/play/?uri={}".format(urllib.quote_plus(torrent, safe=''))
                item.set_path(uri)
            elif tools.getSetting("torrent_player") == "Torrest":
                uri = "plugin://plugin.video.torrest/play_path?path={}".format(torrent)
                item.set_path(uri)
        yield item
    
    if "&scat=7" in scat_url:
        item = Listitem()
        # ACA HAY TEXTO!!! 
        item.label = STR(30052)
        item.set_callback(details_Content, url=link.url, label=label, scat_url=scat_url)
        item.art['thumb'] = "https://cdn.icon-icons.com/icons2/1508/PNG/512/bittorrent_103937.png"
        yield item


@Route.register
def torrent_Images(plugin,torrent,img_path,url,label,scat_url):
    progress = xbmcgui.DialogProgressBG()
    progress.create(STR(30053),label)
    progress.update(25, STR(30054))
    info_hash = tools.getFileData(torrent)[0]
    dir_name = tools.getFileData(torrent)[1].replace("b'","").replace("'","")
    files = tools.getFileData(torrent)[2]
    images = [str(file[b'path']).replace("[b'","").replace("',","").replace(" b'","/").replace("']","") for file in files]
    
   
    if tools.getSetting("torrent_player") == "Elementum":
        root = xbmcaddon.Addon('plugin.video.elementum').getSetting('download_path')
        uri = "plugin://plugin.video.elementum/download/?uri={}".format(urllib.quote_plus(torrent, safe=''))
        resume = "plugin://plugin.video.elementum/download/?oindex={}&resume={}"
        xbmc.executebuiltin('Dialog.Close(all, true)')
        xbmc.executebuiltin('PlayMedia({})'.format(uri))
        wait(5)
        xbmc.executebuiltin('Action(Close)')
        wait(2)
        
        
    elif tools.getSetting("torrent_player") == "Torrest":
        root = xbmcaddon.Addon('plugin.video.torrest').getSetting('s:download_path')
        uri = "plugin://plugin.video.torrest/play_path?path={}&download=true&buffer=false".format(torrent)
        download = "plugin://plugin.video.torrest/torrents/{}/download".format(info_hash)

        xbmc.executebuiltin('RunPlugin("{}")'.format(uri))
        wait(2)
        xbmc.executebuiltin('RunPlugin("{}")'.format(download))
        wait(2)

    wait(3)
    paths = []
    images_toCopy = []
    for image in images:
        route = "/".join([root, dir_name, image])
        path = xbmcvfs.translatePath(route)
        paths.append(path)
    
    while len(images) > len(images_toCopy):
        progress.update(50, STR(30054))
        if paths[0].endswith(('.jpg','.jpeg', '.jfif', '.png', '.tif', '.tiff', '.gif', '.bmp', '.heif', '.raw')): 
            try:
                img = Image.open(paths[0])
                img = img.verify()
                images_toCopy.append(paths[0])
                paths.remove(paths[0])
            except Exception as e:
                root_dir = xbmcvfs.translatePath("/".join([root,dir_name,""]))
                img_loc = paths[0].replace(root_dir,"")
                logger.debug("{}: {}".format(img_loc,e))
                if tools.getSetting("torrent_player") == "Elementum":
                    if img_loc in images:
                        oindex = images.index(img_loc)
                        logger.debug("Oindex is: {}, and the file is: {}".format(oindex,img_loc))
                        xbmc.executebuiltin('Dialog.Close(all, true)')
                        xbmc.executebuiltin('PlayMedia({})'.format(resume.format(oindex,info_hash)))    
                        wait(5)
                paths.append(paths[0])
                paths.remove(paths[0])
        else:
            images_toCopy.append(paths[0])
            paths.remove(paths[0])
        if len(xbmcvfs.listdir(img_path)) >= len(images):
            break

    if tools.getSetting("torrent_player") == "Elementum":
        xbmc.executebuiltin('Action(Close)')
    wait(2)
    progress.update(75, STR(30054))
    wait(2)
    
    copy_progress = xbmcgui.DialogProgress()
    copy_progress.create(STR(30055), label)
    copied_images = []
    for img in images_toCopy:
        shutil.copy(img,img_path)
        copied_images.append(img)
        copy_progress.update((len(copied_images) * 100) // len(images), "{}: {}, {} {}".format(STR(30056),img,len(images) - len(copied_images),STR(30057)))
        wait(1)
    copy_progress.close()
    # ACA HAY TEXTO!!! 
    progress.update(100, STR(30058))
    wait(5)
    progress.close()
    return details_Content(plugin=plugin,url=url,label=label,scat_url=scat_url)
    

@Resolver.register
def show_Photos(plugin,album,pic,url,label,uri):
    # Obtenemos el album, la imagen, la url de la imagen para evitar errores y el nombre de la imagen para visualizarla
    uri = uri
    xbmc.executebuiltin('RunPlugin({})'.format(uri))
    url = url
    plugin = plugin.extract_source(url)
    xbmc.executebuiltin("ShowPicture({})".format(pic))
    wait(5)
    xbmc.executebuiltin("SlideShow({},random)".format(album))
    return Listitem().from_dict(**{
        "label" : label,
        "callback" : plugin,
    })
     

@Route.register
def search_Content(plugin):
    # Creamos una lista con el nombre de todas las categorias y subcategorias.
    principal_categories = [STR(30029),"48G","H!P","Stardust",STR(30044)]
    secondary_categories = [STR(30010),STR(30011),STR(30012),STR(30013),STR(30014),STR(30015),STR(30016),STR(30017),STR(30018),STR(30019),STR(30020),STR(30021)]
    extra_categories = [STR(30022),STR(30023),STR(30024), STR(30030)]
    type_categories = [STR(30031), STR(30032), STR(30033)]
    deadlive_categories = [STR(30034), STR(30035), STR(30036), STR(30037)]

    # Usamos la seleccion o multiseleccion de xbmcgui para obtener el resultado integro o string que necesitamos incluyendo evacion de errores
    sel_pcat = xbmcgui.Dialog().select(STR(30038),principal_categories,useDetails=True)
    if sel_pcat == -1:
        sel_pcat = 0
    pcat = principal_categories[sel_pcat].replace(STR(30029),'Show+All').replace(STR(30044),'Other')
    sel_scat = xbmcgui.Dialog().multiselect(STR(30039),secondary_categories,useDetails=True)
    if sel_scat is not None:
        scat = '%2C'.join([str(opt+1) for opt in sel_scat])
    else:
        scat = ''
    sel_excat = xbmcgui.Dialog().select(STR(30040),extra_categories,useDetails=True)
    excat = extra_categories[sel_excat].replace(STR(30022),'&subbed=1').replace(STR(30023),'&fl=1').replace(STR(30024),'&resd=1').replace(STR(30030),'')
    sel_type = xbmcgui.Dialog().select(STR(30041),type_categories,useDetails=True)
    typ = type_categories[sel_type].replace(STR(30033),'both').replace(STR(30031),'name').replace(STR(30032),'descr')
    sel_deadlive = xbmcgui.Dialog().select(STR(30042),deadlive_categories,useDetails=True)
    if sel_deadlive == -1:
        sel_deadlive = 1
    deadlive = sel_deadlive
    # Enviamos las variables donde estan los resultados que conseguimos a la funcion que realiza la busqueda
    yield Listitem.search(search_All, pcat=pcat, scat=scat, excat=excat, typ=typ, deadlive=deadlive)
    

@Route.register
def search_All(plugin, search_query, pcat, scat, excat, typ, deadlive):
    # Realizamos la busqueda con las variables recibidas
    url = url_constructor("get_ttable.php?pcat={}&typ={}&scat={}{}&p=0&searchstr={}&deadlive={}".format(pcat,typ,scat,excat,search_query,deadlive))
    return all_Content(plugin, url)

@Route.register
def page_Finder(plugin, url):
    page = xbmcgui.Dialog().input(STR(30043),type=xbmcgui.INPUT_NUMERIC)
    p = "&p={}".format(page)
    url = url_constructor("{}{}".format(url,p))
    return all_Content(plugin, scat_url=url)

