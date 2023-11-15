import xbmcaddon
import xbmcvfs
from . import logger
import os
import urllib.parse as urllib
import random
import bencode
import hashlib
import unicodedata

def printer():
    string = "Viva el Rey Viserys"
    return logger.debug(string)


def getString(stringID):
    string = xbmcaddon.Addon().getLocalizedString(stringID)
    return string


def getSetting(settingName):
    setting=xbmcaddon.Addon().getSetting(settingName)
    return setting


def downloadFile(file_name,subdirectory_name,file_content):
    name = unicodedata.normalize('NFKD', file_name).encode('ASCII', 'ignore').decode('utf-8').replace(',','')
    route = "special://home/temp"
    profile = xbmcvfs.translatePath(route)
    addon = xbmcaddon.Addon().getAddonInfo('name').lower().replace(' ','')
    directory = addon
    archive = subdirectory_name.strip()
    path = xbmcvfs.translatePath(os.path.join(profile, directory, archive))
    try:
        xbmcvfs.mkdirs(path)
        logger.debug("Directory '%s' created" %directory)
    except OSError as error:
        logger.debug(error)
    file_path = xbmcvfs.translatePath("{}\{}\{}\{}".format(profile, directory, archive, name))
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

def getFileData(file):
    with open(file, "rb") as f:
        file = bencode.decode(f.read())
        try:
            info_hash = hashlib.sha1(bencode.encode(file[b'info'])).hexdigest()
            name = file[b'info'][b'name']
            files = file[b'info'][b'files']
            return info_hash, str(name), files
        except Exception as e:
            logger.debug(e)
            pass
    