# -*- Mode: python; coding: utf-8; tab-width: 4; indent-tabs-mode: nil; -*-
#
# Copyright 2011, Adrian Sampson.
# Copyright (C) 2012 - Carrasco Agustin
#
# This module is based on beet's lastfmgenre plugin (http://beets.radbox.org/).
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

import pylast
import rb

from LastFMExtensionUtils import asynchronous_call as async

#constants
GENRES_FILE = 'genres.txt'

'''
Genre guesser based on beets' lastgenre plugin. It uses Last.fm tags on a track
to guess the track genre, given a whitelist of genres.
'''
class LastFMGenreGuesser(object):
    '''
    Initialises the guesser, needs the plugin to find the whitelist file.
    '''
    def __init__(self, plugin):
        #load genres whitelist asynchronously
        genres_file = rb.find_plugin_file(plugin, GENRES_FILE)
        self.whitelist = set()
        async(self._load_whitelist)(genres_file)

    '''
    Loads the whitelist file.
    '''
    def _load_whitelist(self, path):
        with open(path) as f:
            for line in f:
                line = line.decode('utf8').strip().lower()
                if line:
                    self.whitelist.add(line)

    '''
    Main interface of the guesser. Given a track, guesses it's genre, using
    Last.fm tags.
    '''
    def guess(self, track):
        tags = self._get_tags(track)
        genre = self._genre_from_tags(tags)

        return genre

    '''
    Retrieves the track tags or return None in case it doesn't find it or fails
    to retrieve them.
    '''
    def _get_tags(self, track):
        try:
            res = track.get_top_tags()
        except:
            return []

        tags = []
        for el in res:
            if isinstance(el, pylast.TopItem):
                el = el.item
            tags.append(el.get_name())
        return tags

    '''
    Crossreferences a list of tags with the whitelisted genres and returns the
    first match.
    '''
    def _genre_from_tags(self, tags):
        for tag in tags:
            if tag.lower() in self.whitelist:
                return tag.title()
        return None
