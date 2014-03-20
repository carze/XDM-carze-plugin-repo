# Author: Dennis Lutter <lad1337@gmail.com>
# Modified By: Cesar Arze (cesar.arze@gmail.com)
# URL: https://github.com/lad1337/XDM-main-plugin-repo/
# URL: https://github.com/carze/XDM-carze-plugin-repo/
# This file is part of a XDM plugin.
#
# XDM plugin.
# Copyright (C) 2013  Dennis Lutter
#
# This plugin is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This plugin is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses/.

from xdm.plugins import *
import datetime
from dateutil import parser

import trakt.tv

class TraktAnime(Provider):
    version = "0.2"
    identifier = "de.carze.traktanime"
    _tag = 'traktanime'
    single = True
    types = ['de.uranime.anime']
    _config = {'api_key': '',
               'release_delta': 0,
              }
    config_meta = {'plugin_desc': 'TV show info from http://trakt.tv. Get your api key from http://trakt.tv/settings/api',
                   'release_delta': {'human': 'Timedelta for the air time in hours', 'desc': 'e.g. -8 or 12'}
                  }

    _resize_url = "http://urani.me/api/imageresize/"

    def __init__(self, instance='Default'):
        Provider.__init__(self, instance=instance)
        trakt.tv.setup(apikey=self.c.api_key)

    def searchForElement(self, term=''):
        self.progress.reset()

        mediaType = MediaType.get(MediaType.identifier == 'de.uranime.anime')
        mtm = common.PM.getMediaTypeManager('de.uranime.anime')[0]
        fakeRoot = mtm.getFakeRoot(term)

        log('trakt.tv [anime] searching for %s' % term)

        _results = trakt.tv.search.shows(term)
        self.progress.total = len(_results)
        for _show in _results:
            _show = trakt.tv.show.summary(_show['tvdb_id'], True)
            self.progress.addItem()
            #self._build_show(_show, fakeRoot, mediaType)
            if 'Animation' in _show['genres']:
                self._createAnime(_show, fakeRoot, mediaType)
                

        return fakeRoot

    def _createAnime(self, _show, fakeRoot, mediaType):
        showElement = Element()
        showElement.mediaType = mediaType
        showElement.parent = fakeRoot
        showElement.type = 'Show'
        showElement.setField('title', _show['title'].encode('utf-8'), self.tag)
        showElement.setField('id', _show['tvdb_id'], self._tag)
        showElement.setField('poster_image', _show['images']['poster'], self.tag)
        showElement.setField('fanart_image', _show['images']['fanart'], self.tag)
        showElement.setField('description', _show['overview'], self.tag)
        showElement.setField('runtime', _show['runtime'], self.tag)
        showElement.setField('classification', 'null', self.tag)

        # if 'synonyms' in item:
        #     showElement.setField(
        #         'synonyms',
        #         dumps([s["title"] for s in item['synonyms'] if s["title"].strip()]),
        #         self.tag
        #     )

        # if "connections" in item:
        #     for connection in item["connections"]:
        #         if connection["site_id"] in connection_names:
        #             showElement.setField('id', connection["source_id"], connection_names[connection["site_id"]])

        showElement.saveTemp()

        for _simple_season in _show['seasons']:
            if _simple_season['season'] == 0:
                continue

            for _episode in _simple_season['episodes']:
                episode = Element()
                episode.mediaType = mediaType
                episode.parent = showElement
                episode.type = 'Episode'
                episode.setField('title', _episode['title'], self.tag)
                episode.setField('number', _episode['episode'], self.tag)
                episode.setField('overview', _episode['overview'], self.tag)
                episode.setField('id', _episode['tvdb_id'], self.tag)
                if _episode['first_aired_iso']:
                    airdate = parser.parse(_episode['first_aired_iso']) - datetime.timedelta(hours=self.c.release_delta)
                    episode.setField('airdate', airdate, self.tag)
                else:
                    episode.setField('airdate', common.FAKEDATE, self.tag)
                episode.setField('screencap_image', _episode['images']['screen'], self.tag)
                episode.saveTemp()

    # def _build_show(self, _show, fakeRoot, mediaType):
    #     show = Element()
    #     show.mediaType = mediaType
    #     show.parent = fakeRoot
    #     show.type = 'Show'
    #     show.setField('title', _show['title'], self.tag)
    #     show.setField('overview', _show['overview'], self.tag)
    #     show.setField('year', _show['year'], self.tag)
    #     show.setField('show_status', _show['status'], self.tag)
    #     show.setField('country', _show['country'], self.tag)
    #     show.setField('genres', ', '.join(_show['genres']), self.tag)
    #     show.setField('runtime', _show['runtime'], self.tag)
    #     show.setField('poster_image', _show['images']['poster'], self.tag)
    #     show.setField('banner_image', _show['images']['banner'], self.tag)
    #     show.setField('fanart_image', _show['images']['fanart'], self.tag)
    #     show.setField('id', _show['tvdb_id'], "tvdb")
    #     show.saveTemp()
    #     for _simple_season in _show['seasons']:
    #         season = Element()
    #         season.mediaType = mediaType
    #         season.parent = show
    #         season.type = 'Season'
    #         season.setField('number', _simple_season['season'], self.tag)
    #         season.setField('poster_image', _simple_season['images']['poster'], self.tag)
    #         season.saveTemp()
    #         for _episode in _simple_season['episodes']:
    #             episode = Element()
    #             episode.mediaType = mediaType
    #             episode.parent = season
    #             episode.type = 'Episode'
    #             episode.setField('title', _episode['title'], self.tag)
    #             episode.setField('season', _episode['season'], self.tag)
    #             episode.setField('number', _episode['episode'], self.tag)
    #             episode.setField('overview', _episode['overview'], self.tag)
    #             episode.setField('id', _episode['tvdb_id'], "tvdb")
    #             if _episode['first_aired_iso']:
    #                 airdate = parser.parse(_episode['first_aired_iso']) - datetime.timedelta(hours=self.c.release_delta)
    #                 episode.setField('airdate', airdate, self.tag)
    #             else:
    #                 episode.setField('airdate', common.FAKEDATE, self.tag)
    #             episode.setField('screencap_image', _episode['images']['screen'], self.tag)
    #             episode.saveTemp()


    def getElement(self, id, element=None):
        tvdb_id = None
        if element is not None:
            tvdb_id = element.getField('id', self._tag)
        if id:
            tvdb_id = id
        if tvdb_id is None:
            return False

        mediaType = MediaType.get(MediaType.identifier == 'de.uranime.anime')
        mtm = common.PM.getMediaTypeManager('de.uranime.anime')[0]
        fakeRoot = mtm.getFakeRoot(tvdb_id)

        _show = trakt.tv.show.summary(tvdb_id, True)
        self._build_show(_show, fakeRoot, mediaType)

        for ele in fakeRoot.decendants:
            if int(ele.getField('id', self._tag)) == int(tvdb_id):
                return ele
        return False
