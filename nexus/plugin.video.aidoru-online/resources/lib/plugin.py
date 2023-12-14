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
import random
from random import uniform
from time import sleep as wait
from PIL import Image
import os
import re
import shutil
import platform

STR = tools.getString #Para facilitar el llamado de strings alojados en languages

addonID = xbmcaddon.Addon().getAddonInfo('id')
torrent_addons = ["Elementum: {}".format(STR(30045)), "Torrest: {}".format(STR(30046))]

torrent_player = tools.getSetting("torrent_player")
if not torrent_player.strip():
    selection = xbmcgui.Dialog().select(STR(30047), torrent_addons, useDetails=True)
logger.debug(selection)

xbmcaddon.Addon().setSetting("torrent_player", torrent_addons[selection].split(':')[0])
torrent_player = tools.getSetting("torrent_player")
logger.debug(torrent_player)

player_uri = {"Elementum" : "plugin://plugin.video.elementum",
                    "Torrest" : "plugin://plugin.video.torrest",
                    }

xbmc.executebuiltin('RunPlugin({})'.format(player_uri[torrent_player]))
sistema = sys.platform()
arquitectura = platform.architecture()
logger.debug(f"{sistema} y {arquitectura}")

# player_url = "https://github.com/"
# player_url_constructor = urljoin_partial(player_url)
# download_url = player_url_constructor("{}/{}/{}/{}/{}/{}".format())
# logger.debug(download_url)

# torrent_player = tools.getSetting("torrent_player")
# player_uri = {"Elementum" : f"https://github.com/{elgatito}/plugin.video.{elementum}/releases/download/{v0.1.98}/plugin.video.{elementum}-{0.1.98}.{linux_armv7}.zip",
#                     "Torrest" : f"https://github.com/{i96751414}/plugin.video.{torrest}/releases/download/{v0.0.16}/plugin.video.{torrest}-{0.0.16}.{windows_x64}.zip",
#                     }


    
#     if selection == 0:
#         repo, plugin = "repository.thewarehouse", "plugin.video.elementum"
#     elif selection == 1:
#         repo, plugin = "repository.github", "plugin.video.torrest"
#     else:
#         sys.exit()
    
#     xbmcaddon.Addon().setSetting("torrent_player", torrent_addons[selection])
#     repoPath, repo_origin = path.format(repo), repoContainer.format(addonID, repo)
#     pluginPath, plugin_origin = path.format(plugin), repoContainer.format(addonID, plugin)
#     items = [repo, plugin]
#     for p in items:
#         p_path = path.format(p)
#         p_origin = repoContainer.format(addonID, p)
#         if not xbmcvfs.exists(p_path):
#             try:
#                 shutil.copytree(p_origin, p_path)
#                 xbmc.executebuiltin('UpdateLocalAddons')
#                 xbmc.executebuiltin('EnableAddon({})'.format(p))
#                 xbmcgui.Dialog().ok(STR(30048), "{} {}({}) {}".format(STR(30049),items[1].replace("plugin.video.","").upper(),items[0].replace("thewarehouse","elementum"),STR(30050)))
#                 xbmc.executebuiltin('DialogClose(all,true)')
#                 xbmc.executebuiltin('InstallAddon({})'.format(items[1]))
#             except Exception as e:
#                 logger.debug(e)
#         else:
#             pass

# Modificamos los ajustes necesarios en Elementum para que el usuario no tenga inconvenientes
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

# Definimos la particion donde esta alojado nuestro addon, creamos la particion completa a las carpetas de resources/media y resources/media/fanarts
# Vemos que archivos o carpetas contiene la carpeta de fanarts, creamos una lista vacia, iteramos sobre la lista que nos devuelve fanarts y añadimos cada nombre de archivo a la lista que creamos
# Creamos dos variables para poder utilizarlas posteriormente en todo el script
addon_path = xbmcaddon.Addon().getAddonInfo("path")
media = xbmcvfs.translatePath(os.path.join(addon_path,"resources","media"))
fanarts_path = os.path.join(media,"fanarts")
fanarts = xbmcvfs.listdir(fanarts_path)

aviable_fanarts = []

for fanart in fanarts[1]:
    aviable_fanarts.append(os.path.join(fanarts_path,fanart))
    
fanart_random = random.choice(aviable_fanarts)
logo = xbmcvfs.translatePath(os.path.join(media,"{}_logo.png")) # Usamos el método format () una sola vez para insertar el valor del nombre del logo 
### BLOQUE PARA LOGUEAR EN LA PAGINA https://aidoru-online.me/###
# Preguntamos en ajustes cual es el usuario y la contraseña que brindo el usuario
username = tools.getSetting("username")
password = tools.getSetting("password")

# Asignamos una url principal, la pasamos a urljoin_partial, creamos una variable url con el constructor creado
# Asignamos variables para utilizar requests, uniform y sleep en todo el script
main_url = "https://aidoru-online.me/"
url_constructor = urljoin_partial(main_url)
url = url_constructor(main_url)
s = requests.session()
some_time = uniform(1000, 5000)
sleep = xbmc.sleep

# Llamamos la cookie ufp y el user-agent que nos manda el script tools.py y rellenamos el header, los parametros y la data
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

# Asignamos a una variable _url y le colocamos la url construida para loguear en la pagina
# Enviamos los datos a esa url con requests y hacemos una pausa para no saturar el sistema  
_url = url_constructor("login.php?type=login")
response = s.post(_url, headers=headers, data=data)
sleep(int(some_time))


@Route.register
def root(plugin, content_type="segment"):
    # Entramos al sitio, comprobamos si estamos logueados, si no estamos logueados aparece un popup pidiendonoslo.
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
    # El primer item es un mensaje de Bienvenida al usuario.
    item = Listitem()
    item.label = "{}: {}".format(STR(30007),tools.getSetting("username").upper())
    item.art["fanart"] = fanart_random
    yield item

    # Mensaje a los lindos usuarios que no me dejaran morir de hambre.
    item = Listitem()
    item.label = STR(30059)
    item.info["plot"] = STR(30060).format("JPonCho","https://www.buymeacoffee.com/ponchofcult")
    item.art["thumb"] = logo.format("qr")
    item.art["fanart"] = fanart_random
    yield item
    # Nos envia a la opcion para buscar el contenido deseado
    item = Listitem()
    item.label = STR(30008)
    item.art["thumb"] = logo.format("search")
    item.art["fanart"] = fanart_random
    item.set_callback(search_Content)
    yield item

    # Hacemos una lista de tuplas, con dos elementos relacionados en cada una, nombre completo de la compañia y nombre abreviado que se pone en la URL. Accedemos a el segun los necesitemos.
    categories = [
        (STR(30009),"Show+All","all-content"),
        ("48 Group Family","48G","48g"),
        ("Hello! Project","H!P","h!p"),
        ("Stardust Planet","Stardust","stapla"),
        (STR(30044),"Other","others")]

    for pcat in categories:
        item = Listitem()
        item.label = pcat[0]
        linkpart = "get_ttable.php?pcat={}&typ=both".format(pcat[1])
        pcat_url = url_constructor(linkpart)
        item.art["thumb"] = logo.format(pcat[2])
        item.art["fanart"] = fanart_random
        item.set_callback(sub_Categories, pcat_url=pcat_url)
        yield item


@Route.register
def sub_Categories(plugin, pcat_url):
    # Lista de Tuplas con dos elementos relacionados, el nombre de la subcategoria y la parte que le corresponde de la URL.
    subcategories = [
        (STR(30009), "&scat=&subbed=&fl=&resd=&p=0&searchstr=&deadlive=1", "all-content"),
        (STR(30010), "&scat=1", "dvd-bd"),
        (STR(30011), "&scat=2", "dvd-bd2"),
        (STR(30012), "&scat=3", "tv"),
        (STR(30013), "&scat=4", "perf"),
        (STR(30014), "&scat=5", "pv"),
        (STR(30015), "&scat=6", "stream"),
        (STR(30016), "&scat=7", "image"),
        (STR(30017), "&scat=8", "audio"),
        (STR(30018), "&scat=9", "album"),
        (STR(30019), "&scat=10", "single"),
        (STR(30020), "&scat=11", "radio"),
        (STR(30021), "&scat=12", "misc"),
        (STR(30022), "&subbed=1", "subs"),
        (STR(30023), "&fl=1", "freeleech"),
        (STR(30024), "&resd=1", "resurrected"),    
    ]

    for scat in subcategories:
        item = Listitem()
        item.label = scat[0]
        scat_url = url_constructor("{}{}".format(pcat_url, scat[1]))
        item.art["thumb"] = logo.format(scat[2])
        item.art["fanart"] = fanart_random
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
        data = bs(s.get(url).text, 'html.parser')
        
        ### SOLO PONER .TEXT AL FINAL CUANDO COLOQUEMOS LO QUEREMOS MOSTRAR A LOS ITEM DE LISTITEM()###
        covers = data.find_all(class_="image-link")
        screenshots = data.find_all(class_="torrent-image")
        
        description = data.find("b", text="Description:").find_parent("tr").text
        category = data.find("b", text="Category:").find_parent("tr").text
        total_size = data.find("b", text="Total Size:").find_parent("tr").text
        added_by = data.find("b", text="Added By:").find_parent("tr").text
        date_added = data.find("b", text="Date Added:").find_parent("tr").text
        seeds = data.find("b", text="Seeds:").find_parent("tr").text
        leechers = data.find("b", text="Leechers:").find_parent("tr").text
        completed = data.find("b", text="Completed:").find_parent("tr").text
        views = data.find("b", text="Views:").find_parent("tr").text
        hits = data.find("b", text="Hits:").find_parent("tr").text
        try:
            last_activity = data.find("b", text="Last Activity").find_parent("tr").text
        except AttributeError as e:
            logger.debug(e)
            last_activity = ""
        
        item.info["plot"] = "| {} | {} | {} | {} | {} | {} | {} | {} | {} | {} | {} |".format(seeds,leechers,added_by,description,total_size,category,date_added,last_activity,completed,views,hits)

        # Inicializar art_link y thumb_link con un valor por defecto y verificar si fanarts tiene algún elemento.
        # Asignamos el valor de la imagen al ultimo elemento de fanarts, si fanarts esta vacio se le asigna el primer elemento de thumbnails.
        # Luego verificamos si thumbnails tiene algun elemento, asignamos el valor de la imagen al ultimo elemento de thumbnails, si thumbnails esta vacio se le asigna el primer elemento de fanarts.
        # Obtenemos las URL de las imagenes y sustituimos unos valores para que esten en la mejor calidad posible.
        # Llamamos a la función details_Content con set_callback con los valores que necesitemos.
        
        art_link = fanart_random
        thumb_link = ""
        
        if covers:
            thumb_link = covers[0].get("src").replace('640x480q90', '4032x3024q90').replace('/th/','/img/')
            item.art['thumb'] = thumb_link 
        elif screenshots:
            thumb_link = screenshots[0].get("data-imgurl").replace('640x480q90', '4032x3024q90')
            item.art['thumb'] = thumb_link

        if screenshots:    
            art_link = screenshots[-1].get("data-imgurl").replace('640x480q90', '4032x3024q90')
            item.art['fanart'] = art_link
        elif covers:
            art_link = covers[0].get("src").replace('640x480q90', '4032x3024q90').replace('/th/','/img/')
            item.art['fanart'] = art_link
            
        item.set_callback(details_Content, url=url, label=item.label, art=art_link, thumb=thumb_link, scat_url=scat_url)
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
                    item.art["thumb"] = logo.format("next")
                    item.art["fanart"] = fanart_random
                    item.set_callback(all_Content, scat_url=nextPage)
                    yield item

                    item = Listitem()
                    item.label = STR(30026)
                    item.art["thumb"] = logo.format("find")
                    item.art["fanart"] = fanart_random
                    item.set_callback(page_Finder, url=_url)
                    yield item
        
        except IndexError:
            pass
    
       
@Route.register
def details_Content(plugin,url,label,art,thumb,scat_url):
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
    added_by = resp.find("b", text="Added By:").find_parent("tr").text.split(':')[1]

    if url_router.text == "Thanks":
        item = Listitem()
        item.label = STR(30061)
        item.info["plot"] = STR(30062).format(added_by)
        item.art["thumb"] = logo.format("thanksbutton")
        item.art["fanart"] = fanart_random
        item.set_callback(thanks_button, url=link.url, label=label, art=art, thumb=thumb, scat_url=scat_url)
        yield item
    else:
        item = Listitem()
        item.label = STR(30063).format(url_router.text.replace(' Thanks',''),added_by)
        item.art["thumb"] = logo.format("thankssupport")
        item.art["fanart"] = fanart_random
        item.set_callback(details_Content, url=link.url, label=label, art=art, thumb=thumb, scat_url=scat_url)
        yield item
    # Obtenemos el contenido, el nombre y el nombre del post para nombrar la locacion
    # Descargamos el archivo Torrent
    tor_content = s.get(url).content
    sleep(int(some_time))
    get_name = s.get(url).headers.get("Content-Disposition").split('filename=')[1].replace('"','').replace('&', '_and_')
    tor_name = re.sub("[^A-Za-z0-9\-_\s.()]", "", get_name)
    sleep(int(some_time))
    tor_loc = link.url.split('=')[1]
    torrent = tools.downloadFile(tor_name,tor_loc,tor_content)
    img_path = xbmcvfs.translatePath(os.path.join(torrent.replace(tor_name,''),"images", ""))
    # Preguntamos que reproductor de Torrent esta seleccionado y dependiendo de la eleccion
    # Si el torrent es de la categoria imagenes lo mandamos a una funcion, si es video lo reproducimos

    torrent_player = tools.getSetting("torrent_player")
    player_uri = {"Elementum" : "plugin://plugin.video.elementum/play/?uri={}".format(urllib.quote_plus(torrent, safe='')),
                    "Torrest" : "plugin://plugin.video.torrest/play_path?path={}".format(torrent),
                    }
    
    item = Listitem()
    if "&scat=7" in scat_url:
        item.label = "{} {}".format(STR(30051),label)
        item.set_callback(download_Images, torrent=torrent, img_path=img_path, url=link.url, label=label, art=art, thumb=thumb, scat_url=scat_url)
    else:
        item.label = label
        uri = player_uri[torrent_player]
        logger.debug("URI: {}".format(uri))
        item.set_path(uri)
    item.art['thumb'] = "https://cdn.icon-icons.com/icons2/1508/PNG/512/bittorrent_103937.png"
    yield item
    
    # Colocamos un valor vacio a image_file para evitar errores
    image_file = ""
    # Despues de buscar, obtener y renombrar la url, obtenemos el nombre de la imagen, el id del post, el contenido de la imagen y la descargamos
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

    if not image_file == "":
        album = image_file.replace(img_name,'')
        all_elems = xbmcvfs.listdir(album)
        all_images = all_elems[1]
        all_images = [i for i in all_images if not i.endswith('.txt')]

        for image in all_images:
            item = Listitem()
            pic = xbmcvfs.translatePath(os.path.join(album,image))
            if image.endswith(('.jpg','.jpeg', '.jfif', '.png', '.tif', '.tiff', '.gif', '.bmp', '.heif', '.raw')):
                item.label = "{} {}".format(STR(30028),image).replace('.jpg','').replace('.jpeg','').replace('.jfif','').replace('.png','').replace('.tif','').replace('.tiff','').replace('.gif','').replace('.bmp','').replace('.heif','').replace('.raw','')
                item.set_callback(show_Photos, album=album, pic=pic, url=url, label=item.label, uri="")   
                item.art['thumb'] = pic
                item.art['fanart'] = pic
            else:
                item.label = image
                item.art['thumb'] = xbmcvfs.translatePath(os.path.join(album,all_images[3]))
                uri_vid = pic
                item.set_path(uri_vid)
            yield item

@Route.register
def download_Images(plugin,torrent,img_path,url,art,thumb,label,scat_url):
    progress = xbmcgui.DialogProgress()
    progress.create(STR(30053),label)
    progress.update(25, STR(30054))

    info_hash = tools.getFileData(torrent)[0]
    dir_name = tools.getFileData(torrent)[1]
    images = tools.getFileData(torrent)[2]
    
    path_file = xbmcvfs.translatePath(os.path.join(img_path,images[-1].split('/')[-1]))
    
    if not xbmcvfs.exists(path_file):
        if tools.getSetting("torrent_player") == "Elementum":
            root = xbmcaddon.Addon('plugin.video.elementum').getSetting('download_path')
            uri = "plugin://plugin.video.elementum/download/?uri={}".format(urllib.quote_plus(torrent, safe=''))
            resume = "plugin://plugin.video.elementum/download/?oindex={}&resume={}"
            xbmc.executebuiltin('Dialog.Close(all, true)')
            xbmc.executebuiltin('PlayMedia({})'.format(uri))
            wait(5)
            # xbmc.executebuiltin('Action(Close)')
            # wait(2)
            
            
        elif tools.getSetting("torrent_player") == "Torrest":
            root = xbmcaddon.Addon('plugin.video.torrest').getSetting('s:download_path')
            uri = "plugin://plugin.video.torrest/play_path?path={}&download=true&buffer=false".format(torrent)
            download = "plugin://plugin.video.torrest/torrents/{}/download".format(info_hash)

            xbmc.executebuiltin('RunPlugin("{}")'.format(uri))
            wait(2)
            xbmc.executebuiltin('RunPlugin("{}")'.format(download))
            wait(2)
    else:
        pass

    paths = []
    images_toCopy = []
    for image in images:
        route = xbmcvfs.translatePath(os.path.join(root,dir_name,image))
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
                root_dir = xbmcvfs.translatePath(os.path.join(root,dir_name,""))
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

    # if tools.getSetting("torrent_player") == "Elementum":
    #     xbmc.executebuiltin('Action(Close)')
    wait(2)
    progress.update(75, STR(30054))
    wait(2)
    
    if not xbmcvfs.exists(path_file):
        copy_progress = xbmcgui.DialogProgress()
        copy_progress.create(STR(30055), label)
        copied_images = []
        for img in images_toCopy:
            shutil.copy(img,img_path)
            copied_images.append(img)
            logger.debug(copied_images)
            copy_progress.update((len(copied_images) * 100) // len(images), "{}: {}, {} {}".format(STR(30056),img,len(images) - len(copied_images),STR(30057)))
            wait(1)
        copy_progress.close()
    progress.update(100, STR(30058))
    progress.close()
    return details_Content(plugin=plugin, url=url, label=label, art=art, thumb=thumb, scat_url=scat_url)
    
@Route.register
def thanks_button(plugin,url,label,art,thumb,scat_url):
    id = url.split('?')[1]
    logger.debug(f"URL: {url}")
    logger.debug(f"ID: {id}")
    thanks_url = url_constructor("torrents-thanks.php?{}".format(id))
    logger.debug(f"URL DE THANKS BUTTON: {thanks_url}")
    do_thanks = s.get(thanks_url)
    logger.debug(do_thanks.status_code)
    return details_Content(plugin=plugin, url=url, label=label, art=art, thumb=thumb, scat_url=scat_url)

@Resolver.register
def show_Photos(plugin,album,pic,url,label,uri):
    # Obtenemos el album, la imagen, la url de la imagen para evitar errores y el nombre de la imagen para visualizarla
    uri = uri
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

