import xbmcgui
import xbmcplugin
import xbmcaddon
import json
import os
import sys

addon = xbmcaddon.Addon()
addon_handle = int(sys.argv[1])
path = xbmcaddon.Addon().getAddonInfo('path')

filename = os.path.join(path, "filmy.json")

def load_films():
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def show_menu():
    items = [
        ("Zobraziť filmy (podľa názvu)", "show_by_name", "clapper.png"),
        ("Zobraziť filmy (podľa hodnotenia)", "show_by_rating", "star.png"),
        ("Zobraziť filmy (podľa roku)", "show_by_year", "calendar.png"),
    ]

    media_path = os.path.join(path, "resources", "media")

    for label, action, icon_file in items:
        url = f"{sys.argv[0]}?action={action}"
        li = xbmcgui.ListItem(label)
        li.setArt({
            "icon": os.path.join(media_path, icon_file),
            "thumb": os.path.join(media_path, icon_file)
        })
        xbmcplugin.addDirectoryItem(addon_handle, url, li, True)

    xbmcplugin.endOfDirectory(addon_handle)

def show_sorted(key, reverse=False):
    films = load_films()

    if not films:
        xbmcgui.Dialog().ok("Tomason", "Zatiaľ nemáš pridané žiadne filmy.")
        return

    if key == "nazov":
        films = sorted(films, key=lambda f: f["nazov"].lower())
    else:
        films = sorted(films, key=lambda f: f[key], reverse=reverse)

    default_icon = os.path.join(path, "resources", "media", "filmstrip.png")

    for f in films:
        label = f"{f['nazov']} ({f['rok']}) - {f['hodnotenie']}/10"
        li = xbmcgui.ListItem(label)
        li.setArt({"icon": default_icon, "thumb": default_icon})
        xbmcplugin.addDirectoryItem(addon_handle, "", li, False)

    xbmcplugin.endOfDirectory(addon_handle)

params = dict(arg.split("=") for arg in sys.argv[2].lstrip("?").split("&") if "=" in arg)
action = params.get("action")

if action == "show_by_name":
    show_sorted("nazov")
elif action == "show_by_rating":
    show_sorted("hodnotenie", reverse=True)
elif action == "show_by_year":
    show_sorted("rok")
else:
    show_menu()
