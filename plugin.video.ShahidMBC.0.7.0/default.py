#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib
import urllib2
import socket
import sys
import re
import os
import datetime
import xbmcplugin
import xbmcgui
import xbmcaddon
import json

socket.setdefaulttimeout(30)
pluginhandle = int(sys.argv[1])
addon = xbmcaddon.Addon()
addonID = addon.getAddonInfo('id')
thumbsDir = xbmc.translatePath('special://home/addons/'+addonID+'/resources/thumbs')
forceViewMode = addon.getSetting("forceViewMode") == "true"
useThumbAsFanart = addon.getSetting("useThumbAsFanart") == "true"
autoPlay = int(addon.getSetting("autoPlay"))
viewModeNewsShows = str(addon.getSetting("viewModeNewsShows"))
viewModeVideos = str(addon.getSetting("viewModeVideos"))
prefRes = addon.getSetting("prefRes")
prefRes = [1080, 720, 520, 480, 360, 240][int(prefRes)]
itemsPerPage = addon.getSetting("itemsPerPage")
itemsPerPage = ["25", "50", "75", "100"][int(itemsPerPage)]
urlMain = "http://shahid.mbc.net"
iconPathChannels = os.path.join(thumbsDir, "channels.png")
iconPathWhats_new = os.path.join(thumbsDir, "whats_new.png")
iconPathMost_watched = os.path.join(thumbsDir, "most_watchd.png")
iconPathAtoZ = os.path.join(thumbsDir, "AtoZ.png")
urlBase = "http://shahid.mbc.net"
urlChannels = "http://shahid.mbc.net/media/channels"
urlSearch = "http://shahid.mbc.net/Ajax/seriesFilter?year=0&dialect=0&title=0&genre=0&channel=0&prog_type=0&media_type=0&airing=0&sort=alpha&series_id=0&offset=0&sub_type=0&limit=10000"
MBCproviderID = '2fda1d3fd7ab453cad983544e8ed70e4'

def index(): 
    addDir("Channles", "", 'listChannels', iconPathChannels)
    addDir("New Items", "http://shahid.mbc.net/media/episodes?sort=latest", 'listEpisodesSorted', iconPathWhats_new)
    addDir("Most Watched", "http://shahid.mbc.net/media/episodes?sort=popular_all", 'listEpisodesSorted', iconPathMost_watched)
    addDir("A-Z", urlSearch, 'listShowsSorted', iconPathAtoZ)
    if forceViewMode:
        xbmc.executebuiltin('Container.SetViewMode('+viewModeNewsShows+')')
    xbmcplugin.endOfDirectory(pluginhandle)

def listChannels():
    htmlfile = urllib.urlopen(urlChannels)
    htmltext = htmlfile.read()
    regex1 = '''<li><a href="/media/channel/'''+'''[1-9]*'''+'''/(.+?)"'''
    regex2 = '''title=""><b><img src="(.+?)"'''
    regex3 = '''<a href="(.+?)" title='''
    pattern1 = re.compile(regex1)
    pattern2 = re.compile(regex2)
    pattern3 = re.compile(regex3)
    ch_name = re.findall(pattern1,htmltext)
    img_path = re.findall(pattern2,htmltext)
    ch_path = re.findall(pattern3,htmltext)
    i = 0
    while i< len(ch_name):
        addDir(ch_name[i], ch_path[i], 'listShows', img_path[i])
        i+=1
    if forceViewMode:
        xbmc.executebuiltin('Container.SetViewMode('+viewModeNewsShows+')')
    xbmcplugin.endOfDirectory(pluginhandle)

def listShows(ch_path):
    #urlCh = "http://shahid.mbc.net"+ ch_path
    chID = re.findall(re.compile('''/media/channel/(.*?)/'''),ch_path)
    urlCh = "http://shahid.mbc.net/Ajax/series_sort?offset=0&channel_id=" + chID[0] + "&sort=latest&limit=500"
    htmlfile = urllib.urlopen(urlCh)
    htmltext = htmlfile.read()
    regex1 = '''<span class="title major">(.+?)</span>'''
    regex2 = '''title=""><b><img src="(.+?)"'''
    regex3 = '''" href="(.*?)" title="">'''
    pattern1 = re.compile(regex1)
    pattern2 = re.compile(regex2)
    pattern3 = re.compile(regex3)
    show_name = re.findall(pattern1,htmltext)
    img_path = re.findall(pattern2,htmltext)
    ch_path = re.findall(pattern3,htmltext)
    i = 0
    while i< len(show_name):
        addDir(show_name[i], ch_path[i], 'listEpsodes', img_path[i])
        i+=1
    if forceViewMode:
        xbmc.executebuiltin('Container.SetViewMode('+viewModeNewsShows+')')
    xbmcplugin.endOfDirectory(pluginhandle)

def listShowsSorted(urlCh):
    htmlfile = urllib.urlopen(urlCh)
    htmltext = htmlfile.read()
    regex1 = '''<span class="title major">(.+?)</span>'''
    regex2 = '''title=""><b><img src="(.+?)"'''
    regex3 = '''" href="(.*?)" title="">'''
    pattern1 = re.compile(regex1)
    pattern2 = re.compile(regex2)
    pattern3 = re.compile(regex3)
    show_name = re.findall(pattern1,htmltext)
    img_path = re.findall(pattern2,htmltext)
    ch_path = re.findall(pattern3,htmltext)
    i = 0
    while i< len(show_name):
        addDir(show_name[i], ch_path[i], 'listEpsodes', img_path[i])
        i+=1
    if forceViewMode:
        xbmc.executebuiltin('Container.SetViewMode('+viewModeNewsShows+')')
    xbmcplugin.endOfDirectory(pluginhandle)

def listEpsodes(ch_path):
    #urlCh = ch_path
    #http://shahid.mbc.net/Ajax/episode/761?offset=10&media_type=program&limit=10&sort=season&season=null
    chID = re.findall(re.compile('''/media/program/(.*?)/'''),ch_path)
    urlCh = "http://shahid.mbc.net/Ajax/episode/" + chID[0] + "?offset=0&media_type=program&limit=5000&sort=season&season=null"
    htmlfile = urllib.urlopen(urlCh)
    htmltext = htmlfile.read()
    regex1 = '''</span><span class="title">(.*?)</span>'''
    regex2 = '''img src="(.*?)" alt="" border="0" height="" width=""'''
    regex3 = '''</span><a href="(.+?)" title='''
    pattern1 = re.compile(regex1)
    pattern2 = re.compile(regex2)
    pattern3 = re.compile(regex3)
    show_name = re.findall(pattern1,htmltext)
    img_path = re.findall(pattern2,htmltext)
    ch_path = re.findall(pattern3,htmltext)
    i = 0
    while i< len(show_name):
        addDir(show_name[i], ch_path[i], 'playVideo', img_path[i])
        i+=1
    if forceViewMode:
        xbmc.executebuiltin('Container.SetViewMode('+viewModeNewsShows+')')
    xbmcplugin.endOfDirectory(pluginhandle)

def listEpisodesSorted(urlCh):
  #  urlCh = "http://shahid.mbc.net/media/episodes?sort=latest"
    htmlfile = urllib.urlopen(urlCh)
    htmltext = htmlfile.read()
    regex1 = '''</span><span class="title">(.*?)</span>'''
    regex2 = '''img src="(.*?)" alt="" border="0" height="" width=""'''
    regex3 = '''</span><a href="(.+?)" title='''
    pattern1 = re.compile(regex1)
    pattern2 = re.compile(regex2)
    pattern3 = re.compile(regex3)
    show_name = re.findall(pattern1,htmltext)
    img_path = re.findall(pattern2,htmltext)
    ch_path = re.findall(pattern3,htmltext)
    i = 0
    while i< len(show_name):
        addDir(show_name[i], ch_path[i], 'playVideo', img_path[i])
        i+=1
    if forceViewMode:
        xbmc.executebuiltin('Container.SetViewMode('+viewModeNewsShows+')')
    xbmcplugin.endOfDirectory(pluginhandle)


def playVideo(ch_path):
 # extracting mediaID
    htmlfile = urllib.urlopen(urlBase + ch_path)
    htmltext = htmlfile.read()
    regex1 = '''mediaId=(.*?)&&default'''
    pattern1 = re.compile(regex1)
    mediaID = re.findall(pattern1,htmltext)    
 # obtaining rtmpURL
    urlContentProvider = 'http://production.ps.delve.cust.lldns.net/PlaylistService'
    headerValues = {'content-type' : 'text/soap+xml'}
    soapParm = '''<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><SOAP-ENV:Body><tns:getPlaylistByMediaId xmlns:tns="http://service.data.media.pluggd.com"><tns:in0>''' + mediaID[0] + '''</tns:in0><tns:in1 xsi:nil="true"/></tns:getPlaylistByMediaId></SOAP-ENV:Body></SOAP-ENV:Envelope>'''
    full_url = urllib2.Request(urlContentProvider, data=soapParm, headers=headerValues)
    response = urllib2.urlopen(full_url)
    urlResponse = response.read()
    regex1 = '''</previewStream><url>(.*?)</url><videoBitRate>'''
    regex2 = '''<videoHeightInPixels>(.*?)</videoHeightInPixels>'''  
    pattern1 = re.compile(regex1)
    pattern2 = re.compile(regex2)
    rtmpURL = re.findall(pattern1,urlResponse)
    resolution = re.findall(pattern2,urlResponse)
 # selecting resolution
    resolution = map(int, resolution)
    if prefRes not in resolution:
        playResPos = resolution.index(max(resolution))
    elif prefRes > max(resolution):
        playResPos = resolution.index(max(resolution)) 
    else: 
        playResPos = resolution.index(prefRes)
        
 #playlist
    playlist = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
    playlist.clear()
    # sample rtmpURL
    # play_string = '''rtmpe://mbc3.csl.delvenetworks.com/a6344/v1/mp4:media/2fda1d3fd7ab453cad983544e8ed70e4/0c0d5121b14c4d5eb46752981de067af/16c00e0bcd074aa6b48fc652fa0945b8/al_arraf_s01_e26.mp4'''
    playlist.add(rtmpURL[playResPos])
    xbmc.executebuiltin('playlist.playoffset(video,0)')     
    #another method to play playlist 
    #xbmc.Player().play( playlist)

def showMessage(msg):
        xbmc.executebuiltin('XBMC.Notification(%s, 5000)'%(msg)) 
        
def parameters_string_to_dict(parameters):
    paramDict = {}
    if parameters:
        paramPairs = parameters[1:].split("&")
        for paramsPair in paramPairs:
            paramSplits = paramsPair.split('=')
            if (len(paramSplits)) == 2:
                paramDict[paramSplits[0]] = paramSplits[1]
    return paramDict

def addDir(name, url, mode, iconimage, type="", desc=""):
    u = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&type="+str(type)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={"Title": name, "Plot": desc})
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
    return ok

params = parameters_string_to_dict(sys.argv[2])
mode = urllib.unquote_plus(params.get('mode', ''))
url = urllib.unquote_plus(params.get('url', ''))
type = urllib.unquote_plus(params.get('type', ''))


if mode == 'playVideo':
    playVideo(url)
elif mode == 'listShowsSorted':
    listShowsSorted(url)    
elif mode == 'listEpisodesSorted':
    listEpisodesSorted(url)    
elif mode == 'listEpsodes':
    listEpsodes(url)
elif mode == 'listShows':
    listShows(url)
elif mode == 'listChannels':
    listChannels()
elif mode == 'showMessage':
    showMessage('Coming Soon')
else:
    index()

