import xbmc
import xbmcaddon
from . import tools

def debug(message):
    addonName = xbmcaddon.Addon().getAddonInfo('name').upper()
    log_enabled = tools.getSetting("debug")
    if log_enabled == "true":
        xbmc.log("{}: {}".format(addonName,str(message)), xbmc.LOGINFO)
        