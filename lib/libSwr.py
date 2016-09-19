# -*- coding: utf-8 -*-
import sys
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import urllib
import libSwrParser
import libMediathek

translation = xbmcaddon.Addon(id='script.module.libMediathek').getLocalizedString




def libSwrListMain():
	#libSwrParser.getList('http://swrmediathek.de/app-2/index.html')
	#libSwrParser.getList('http://swrmediathek.de/app-2/themen.html')
	libMediathek.addEntry({'name':translation(31030), 'mode':'libSwrListVideos', 'url':'http://swrmediathek.de/app-2/svp.html'})
	libMediathek.addEntry({'name':translation(31031), 'mode':'libSwrListVideos', 'url':'http://swrmediathek.de/app-2/index.html'})
	libMediathek.addEntry({'name':translation(31032), 'mode':'libSwrListDir', 'url':'http://swrmediathek.de/app-2/tv.html'})
	libMediathek.addEntry({'name':translation(31033), 'mode':'libSwrListDate'})
	libMediathek.addEntry({'name':translation(31034), 'mode':'libSwrListDir', 'url':'http://swrmediathek.de/app-2/rubriken.html'})
	libMediathek.addEntry({'name':translation(31035), 'mode':'libSwrListDir', 'url':'http://swrmediathek.de/app-2/themen.html'})
	#libMediathek.addEntry({'name':translation(31032), 'mode':'libSwrListLetters'})
	#libMediathek.addEntry({'name':translation(31033), 'mode':'libSwrListDate'})
	#libMediathek.addEntry({'name':translation(31034), 'mode':'libArdListVideos', 'url':'http://www.ardmediathek.de/appdata/servlet/tv/Rubriken/mehr?documentId=21282550&json'})

def libSwrListDir():
	libMediathek.addEntries(libSwrParser.getList(params['url'],'dir','libSwrListVideos'))
	
def libSwrListDate():
	libMediathek.populateDirDate('libSwrListDateVideos')
		
def libSwrListDateVideos():
	libMediathek.addEntries(libSwrParser.getDate(params['datum'],'date','libSwrPlay'))
	
def libSwrListVideos():
	libMediathek.addEntries(libSwrParser.getList(params['url'],'video','libSwrPlay'))

def libSwrPlay():
	url = libSwrParser.getVideo(params['url'])
	listitem = xbmcgui.ListItem(path=url)
	xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)
	
	
	
	
	
def getDate(date):
	return libSwrJsonParser.parseDate(date)
def getVideoUrl(url):
	return libSwrJsonParser.parseVideo(url)
def play(dict):
	url = getVideoUrl(dict["url"])
	#listitem = xbmcgui.ListItem(label=video["name"],thumbnailImage=video["thumb"],path=url)
	listitem = xbmcgui.ListItem(label=dict["name"],path=url)
	xbmc.Player().play(url, listitem)	
	

	
	
	
def libSwrListLetters():
	libMediathek.populateDirAZ('libSwrListShows',ignore=['#'])
	
def libSwrListShows():
	xbmc.log('listshows')
	libMediathek.addEntries(libSwrParser.parseShows(params['name']))
	
	
	
def list():	
	modes = {
	'libSwrListDir': libSwrListDir,
	'libSwrListDate': libSwrListDate,
	'libSwrListDateVideos': libSwrListDateVideos,
	
	'libSwrListVideos': libSwrListVideos,
	
	'libSwrPlay': libSwrPlay,
	
	
	'libSwrListLetters': libSwrListLetters,
	'libSwrListShows': libSwrListShows,
	#'libSwrListDateChannels': libSwrListDateChannels,
	}
	global params
	params = libMediathek.get_params()
	global pluginhandle
	pluginhandle = int(sys.argv[1])
	xbmc.log('mode')
	xbmc.log(params.get('mode',''))
	if not params.has_key('mode'):
		libSwrListMain()
	else:
		modes.get(params['mode'],libSwrListMain)()
	
	xbmcplugin.endOfDirectory(int(sys.argv[1]))	