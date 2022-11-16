"""Sensor for mealviewer account status."""
from datetime import timedelta
import logging
import requests
import arrow
import xmltodict, json
from xml.etree import ElementTree

from time import mktime

import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.core import callback
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.event import track_time_interval
from homeassistant.util.dt import utc_from_timestamp

_LOGGER = logging.getLogger(__name__)

CONF_ACCOUNTS = "accounts"

ICON = "mdi:robot-outline"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_ACCOUNTS, default=[]): vol.All(cv.ensure_list, [cv.string]),
    }
)


BASE_INTERVAL = timedelta(hours=6)


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the mealviewer platform."""
    
    entities = [mealviewerSensor(account) for account in config.get(CONF_ACCOUNTS)]
    if not entities:
        return
    add_entities(entities, True)

    # Only one sensor update once every 60 seconds to avoid
    entity_next = 0



class mealviewerSensor(Entity):
    """A class for the mealviewer account."""

    def __init__(self, account):
        """Initialize the sensor."""
        
        self._account = account
        self._lunch0 = None
        self._lunch1 = None
        self._lunch2 = None
        self._lunch3 = None
        self._lunch4 = None
        self._state = None
        self._name = self._account

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def entity_id(self):
        """Return the entity ID."""
        #return f"sensor.mealviewer_{self._name}"
        return 'sensor.mealviewer_' + (self._account).lower()
        
    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state
    
    @property
    def should_poll(self):
        """Turn off polling, will do ourselves."""
        return True
        
    def update(self):
        """Update device state."""
        
        self._state = 'Not Updated'
        try:
            host = 'https://api.mealviewer.com/api/v4/school'
            school = self._account
            self._name = school

            for day in range(5):
                tomorrow = arrow.utcnow().to('US/Eastern').shift(days=day)
            
                meal = ''
  

                if tomorrow.weekday() not in (5, 6):
                    formatted_tomorrow = tomorrow.format('MM-DD-YYYY')

                    url = f'{host}/{school}/{formatted_tomorrow}/{formatted_tomorrow}'
   
                    r = requests.get(url)
                    menus = r.json().get('menuSchedules')[0].get('menuBlocks')
        
                    
                    if not menus:
                        meal = ''
                    else:
                        lunch_menu = menus[0]
                    
                        meal = tomorrow.format('dddd')
                        counter = 0
                        for datas in lunch_menu.get('cafeteriaLineList').get('data')[0]['foodItemList']['data']:
                            counter = counter + 1
                            entree = datas['item_Name']
                            if counter == 1:
                                meal = meal + ': ' + entree
                            else:
                                meal = meal + ', ' + entree
                
                if day == 0:
                    self._lunch0 = meal
                if day == 1:
                    self._lunch1 = meal
                if day == 2:
                    self._lunch2 = meal
                if day == 3:
                    self._lunch3 = meal
                if day == 4:
                    self._lunch4 = meal
                    
                self._state = 'Updated'    
        except:        
            self._lunch0 = None
            self._lunch1 = None
            self._lunch2 = None
            self._lunch3 = None
            self._lunch4 = None
    
    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        attr = {}
        
        attr["lunch0"] = self._lunch0
        attr["lunch1"] = self._lunch1    
        attr["lunch2"] = self._lunch2
        attr["lunch3"] = self._lunch3
        attr["lunch4"] = self._lunch4
        
 
        return attr

    
    @property
    def icon(self):
        """Return the icon to use in the frontend."""
        return ICON
