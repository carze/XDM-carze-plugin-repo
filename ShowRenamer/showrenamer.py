# Author: Cesar Arze <cesar.arze@gmail.com>
# URL: https://github.com/carze/XDM-carze-plugin-repo/
#
# This file is part of a XDM plugin.
#
# XDM plugin.
# Copyright (C) 2014  panni
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
from xdm.tasks import createGenericEvent

class ModifyName(SearchTermFilter):
    """
    This plugin attempts to rename a show based off a user-provided replacement. 

    Should be used in situations where scraped names do not match scene names. 
    The intent is to keep the search term structure (i.e. <TITLE> <EPISODE NUMBER>)
    but allow replacing of the <TITLE> element.
    """
    version = "0.1"
    identifier = 'de.carze.element.name'
    screenName = 'Replace Name To Look For'
    addMediaTypeOptions = "runFor"
    single = True
    elementConfig = {
        'original_name': ''
        'look_for_instead': '',
    }

    config_meta = {'plugin_desc': "Allows for replacement of a show name in case of the scrapped name not matching scene releases."}

    def compare(self, element, terms):
        self.e.getConfigsFor(element) #this will load all the elements configs

        original_name = self.e.getConfig('original_name', element).value
        replace_name = self.e.getConfig("look_for_instead", element).value

        ## If we can't find our original name in search terms we will want to use the term as-is.
        new_terms = []
        if len(replace_name):
            for term in terms:
                new_terms.append(term.replace(original_name, replace_name))
 
            log.info("Now searching for %s" % ", ".join(new_terms))
            createGenericEvent(element, "filter", message)

        return new_terms

