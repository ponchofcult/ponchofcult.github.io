import xbmc
import xbmcaddon
import xbmcvfs
from . import logger
import os
import re
from contextlib import contextmanager
import urllib.parse as urllib
import random
import bencode
import hashlib
import unicodedata


def getString(stringID):
    string = xbmcaddon.Addon().getLocalizedString(stringID)
    return string


def getSetting(settingName,addonID=""):
    setting = xbmcaddon.Addon(addonID).getSetting(settingName)
    return setting


def setSetting(setting_name,setting_value,addon_id=""):
    if type(setting_value) == "int":
        xbmcaddon.Addon(addon_id).setSettingInt(setting_name,setting_value)
    elif type(setting_value) == "bool":
        xbmcaddon.Addon(addon_id).setSettingBool(setting_name,setting_value)
    elif type(setting_value) == "float":
        xbmcaddon.Addon(addon_id).setSettingNumber(setting_name,setting_value)
    elif type(setting_value) == "str":
        xbmcaddon.Addon(addon_id).setSetting(setting_name,setting_value)
    else:
        xbmcaddon.Addon(addon_id).setSetting(setting_name,str(setting_value))
    logger.debug(getSetting(setting_name,addon_id))


def downloadFile(file_name,subdirectory_name,file_content):
    file_name = file_name.replace('&', '_and_')
    name = re.sub("[^A-Za-z0-9\-_\s.()]", "", file_name)
    route = xbmcvfs.translatePath("special://home/temp")
    directory = xbmcaddon.Addon().getAddonInfo('name').lower().replace(' ','_')
    archive = subdirectory_name.strip().replace(' ','_')
    path = xbmcvfs.translatePath(os.path.join(route, directory, archive))
    try:
        xbmcvfs.mkdirs(path)
        logger.debug("Directory {} created".format(directory))
    except OSError as error:
        logger.debug(error)
    file_path = xbmcvfs.translatePath(os.path.join(route, directory, archive, name))
    with open(file_path, 'wb') as file:
        file.write(file_content)
        file.close()
        file = file_path
        return file


def mixCharacters(len):
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

    characters = letters + numbers

    string = []

    for i in range(len):
        character_random = random.choice(characters)
        string.append(character_random)
        mix = "".join(string)
    
    string = [str(r) for r in string] #Para quitar las u'
    string = ''.join(string)
    return str(string)


def mixUserAgents():
    ua_list = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.63',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 15_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (Linux; Android 12; Pixel 6 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36',
        'Mozilla/5.0 (iPad; CPU OS 15_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/110.0.0 Mobile/15E148 Safari/604.1'
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/110.'
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0 Safari/537 OPR/95',
    ]

    for ua in ua_list:
        user_agent = ua
    return user_agent


def getFileData(archive):
    with open(archive, "rb") as a:
        file = a.read()
        logger.debug("FILE ES: {}".format(file))
        archive = bencode.decode(file)
        logger.debug("ARCHIVE ES: {}".format(archive))
        try:
            info_hash = hashlib.sha1(bencode.encode(archive[b'info'])).hexdigest()
            logger.debug("INFO_HASH ES: {}".format(info_hash))
        except Exception as e:
            logger.debug("ERROR: {}".format(e))
            info_hash = None
        try:
            name = archive[b'info'][b'name'].decode("utf-8") # name = name_bytes.decode("utf-8")
            logger.debug("NAME ES: {}".format(name))
        except Exception as e:
            logger.debug("ERROR: {}".format(e))
            name = None
        try:
            files_bytes = archive[b'info'][b'files']
            logger.debug("FILES_BYTES ES: {}".format(files_bytes))
            files = ['/'.join([file.decode('utf-8') for file in path[b'path']]) for path in files_bytes]
            logger.debug("FILES ES: {}".format(files))
        except Exception as e:
            logger.debug("ERROR: {}".format(e))
            files = None
        
        return info_hash, name, files, file