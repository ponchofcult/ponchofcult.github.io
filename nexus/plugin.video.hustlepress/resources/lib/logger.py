import xbmc
import xbmcaddon
from . import tools

def debug(*args):
    addonName = xbmcaddon.Addon().getAddonInfo('name').upper()
    log_enabled = tools.getSetting("debug")
    if log_enabled == "true":
        for message in args:
            xbmc.log("{}: {}".format(addonName,str(message)), xbmc.LOGINFO)
        