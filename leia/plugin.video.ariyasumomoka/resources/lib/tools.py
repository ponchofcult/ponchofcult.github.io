import xbmcaddon
import xbmc
import xbmcvfs
import xbmcgui
from . import logger
import shutil
import os
import urlquick

def getString(stringID):
    string = xbmcaddon.Addon().getLocalizedString(stringID)
    return string


def getSetting(settingName):
    setting=xbmcaddon.Addon().getSetting(settingName)
    return setting


def downloadFile(file_name,subdirectory_name,file_url):
    name = file_name
    url = urlquick.get(file_url)
    route = "special://home/temp"
    profile = xbmcvfs.translatePath(route)
    addon = xbmcaddon.Addon().getAddonInfo('name').lower().replace(' ','')
    directory = addon
    archive = subdirectory_name
    path = xbmcvfs.translatePath(os.path.join(profile, directory, archive))
    try:
        xbmcvfs.mkdirs(path)
        logger.debug("Directory '%s' created" %directory)
    except OSError as error:
        logger.debug(error)
    file_path = xbmcvfs.translatePath("{}/{}/{}/{}".format(profile, directory, archive, name))
    file = open(file_path, 'wb')
    file.write(url.content)
    file.close()
    file = file_path
    return file


def setFont():
    addonID = xbmcaddon.Addon().getAddonInfo('id')
    skin = xbmc.getSkinDir()
    xmls_route = [
        {"xmls": "xml"},
        {"xmls": "16x9"},
        {"xmls": "720p"},
        {"xmls": "1080i"},
    ]
    # Conocer que Skin estamos usando y obtener las rutas
    for xmls_folder in xmls_route:
        xmls = xbmcvfs.translatePath('special://home/addons/{}/{}/'.format(skin,xmls_folder["xmls"]))
        skin_original = xbmcvfs.translatePath('special://xbmc/addons/{}'.format(skin))
        skin_new = xbmcvfs.translatePath('special://home/addons/{}'.format(skin))
        act_font = xmls + 'Font.xml'
        xml_font = xbmcvfs.translatePath('special://home/addons/{}/resources/lib/Font.xml'.format(addonID))
        
        if xbmcvfs.exists(xmls):   

            # Leer el archivo Font.xml
            with open(act_font, "r") as f:
                data = f.readlines()
                line_org = data[2]
                line_need = '<fontset id="Default" idloc="31053">'
                    
                # Verificar si la linea 3 es la correcta
                if line_org.strip() != line_need.strip():
                    # Si la linea no es correcta, eliminar y reemplazar el archivo Font.xml
                    xbmcvfs.delete(act_font)
                    shutil.copy(xml_font, act_font.replace('Font.xml',''))
                    xbmcgui.Dialog().ok(getString(30002), getString(30003))
                else:
                    # Si la linea es correcta, no hacer nada
                    pass

        elif not xbmcvfs.exists(xmls):
            # Si no existe la carpeta, verificar si estamos usando Estuary o Estouchy
            if skin == "skin.estuary" or skin == "skin.estouchy":
                try:
                    # Copiar la carpeta original y reemplazar el archivo Font.xml
                    shutil.copytree(skin_original, skin_new)
                    xbmcvfs.delete(xbmcvfs.translatePath('{}{}'.format(skin_new,'/xml/Font.xml')))
                    shutil.copy(xml_font, '{}/xml/'.format(skin_new))
                    xbmcgui.Dialog().ok(getString(30002), getString(30003))
                except OSError as error:
                    logger.debug(error)
        else:
            xbmcgui.Dialog().ok(getString(30004) , getString(30005))
