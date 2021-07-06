"""Support for Actions on Yandex Smart Home."""
import asyncio
import logging
from typing import Dict, Any

import voluptuous as vol

from homeassistant.core import HomeAssistant, Event
from homeassistant.const import CONF_NAME, CONF_USERNAME, CONF_PASSWORD, CONF_TOKEN
from homeassistant.config_entries import SOURCE_IMPORT, ConfigEntry
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers import entityfilter
from homeassistant.helpers.aiohttp_client import async_create_clientsession

from .const import (
    DOMAIN, CONFIG, DATA_CONFIG, CONF_ENTITY_CONFIG, CONF_FILTER, CONF_ROOM, CONF_TYPE,
    CONF_ENTITY_PROPERTIES, CONF_ENTITY_PROPERTY_ENTITY, CONF_ENTITY_PROPERTY_ATTRIBUTE, CONF_ENTITY_PROPERTY_TYPE,
    CONF_CHANNEL_SET_VIA_MEDIA_CONTENT_ID, CONF_RELATIVE_VOLUME_ONLY, CONF_ENTITY_RANGE, CONF_ENTITY_RANGE_MAX, 
    # CONF_ENTITY_RANGE_MIN, CONF_ENTITY_RANGE_PRECISION, CONF_ENTITY_MODE_MAP, PRESSURE_UNIT_MMHG, PRESSURE_UNITS_TO_YANDEX_UNITS,
    # CONF_SKILL, CONF_SKILL_NAME, CONF_SKILL_USER_ID, CONF_PROXY, CONF_SKILL_OAUTH_TOKEN, CONF_SKILL_ID)

# from .http import async_register_http
# from .core import utils
# from .core.yandex_session import YandexSession
# from .skill import YandexSkill
    CONF_ENTITY_RANGE_MIN, CONF_ENTITY_RANGE_PRECISION, CONF_ENTITY_MODE_MAP,
    CONF_SETTINGS, CONF_PRESSURE_UNIT, PRESSURE_UNIT_MMHG, PRESSURE_UNITS_TO_YANDEX_UNITS,
    CONF_NOTIFIER, CONF_SKILL_OAUTH_TOKEN, CONF_SKILL_ID, CONF_NOTIFIER_USER_ID, NOTIFIER_ENABLED)
from .helpers import Config
from .http import async_register_http
from .notifier import setup_notification

_LOGGER = logging.getLogger(__name__)

ENTITY_PROPERTY_SCHEMA = vol.Schema({
    vol.Optional(CONF_ENTITY_PROPERTY_TYPE): cv.string,
    vol.Optional(CONF_ENTITY_PROPERTY_ENTITY): cv.string,
    vol.Optional(CONF_ENTITY_PROPERTY_ATTRIBUTE): cv.string,
}, extra=vol.PREVENT_EXTRA)

ENTITY_RANGE_SCHEMA = vol.Schema({
    vol.Optional(CONF_ENTITY_RANGE_MAX): vol.All(vol.Coerce(float), vol.Range(min=-100.0, max=1000.0)),
    vol.Optional(CONF_ENTITY_RANGE_MIN): vol.All(vol.Coerce(float), vol.Range(min=-100.0, max=1000.0)),
    vol.Optional(CONF_ENTITY_RANGE_PRECISION): vol.All(vol.Coerce(float), vol.Range(min=-100.0, max=1000.0)),
}, extra=vol.PREVENT_EXTRA)

ENTITY_SCHEMA = vol.Schema({
    vol.Optional(CONF_NAME): cv.string,
    vol.Optional(CONF_ROOM): cv.string,
    vol.Optional(CONF_TYPE): cv.string,
    vol.Optional(CONF_ENTITY_PROPERTIES, default=[]): [ENTITY_PROPERTY_SCHEMA],
    vol.Optional(CONF_CHANNEL_SET_VIA_MEDIA_CONTENT_ID): cv.boolean,
    vol.Optional(CONF_RELATIVE_VOLUME_ONLY): cv.boolean,
    vol.Optional(CONF_ENTITY_RANGE, default={}): ENTITY_RANGE_SCHEMA,
    vol.Optional(CONF_ENTITY_MODE_MAP, default={}): {cv.string: {cv.string: [cv.string]}},
})

NOTIFIER_SCHEMA = vol.Schema({
    vol.Optional(CONF_SKILL_OAUTH_TOKEN): cv.string,
    vol.Optional(CONF_SKILL_ID): cv.string,
    vol.Optional(CONF_NOTIFIER_USER_ID): cv.string,
}, extra=vol.PREVENT_EXTRA)

def pressure_unit_validate(unit):
    if not unit in PRESSURE_UNITS_TO_YANDEX_UNITS:
        raise vol.Invalid(f'Pressure unit "{unit}" is not supported')

    return unit
    
SKILL_SCHEMA = vol.Schema({
    vol.Optional(CONF_USERNAME): cv.string,
    vol.Optional(CONF_PASSWORD): cv.string,
    vol.Optional(CONF_TOKEN): cv.string,
    vol.Optional(CONF_PROXY): cv.string,
    vol.Optional(CONF_SKILL_NAME): cv.string,
    vol.Optional(CONF_SKILL_USER_ID): cv.string,
    # light
    vol.Optional(CONF_SKILL_OAUTH_TOKEN): cv.string,
    vol.Optional(CONF_SKILL_ID): cv.string,
}, extra=vol.PREVENT_EXTRA)

SETTINGS_SCHEMA = vol.Schema({
    vol.Optional(CONF_PRESSURE_UNIT, default=PRESSURE_UNIT_MMHG): vol.Schema(
        vol.All(str, pressure_unit_validate)
    ),
})

SETTINGS_SCHEMA = vol.Schema({
    vol.Optional(CONF_PRESSURE_UNIT, default=PRESSURE_UNIT_MMHG): vol.Schema(
        vol.All(str, pressure_unit_validate)
    ),
})

YANDEX_SMART_HOME_SCHEMA = vol.All(
    vol.Schema({
        vol.Optional(CONF_SKILL, default={}): SKILL_SCHEMA,
        vol.Optional(CONF_NOTIFIER, default={}): NOTIFIER_SCHEMA,
        vol.Optional(CONF_SETTINGS, default={}): SETTINGS_SCHEMA,
        vol.Optional(CONF_FILTER, default={}): entityfilter.FILTER_SCHEMA,
        vol.Optional(CONF_ENTITY_CONFIG, default={}): {cv.entity_id: ENTITY_SCHEMA},
    }, extra=vol.PREVENT_EXTRA))

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: YANDEX_SMART_HOME_SCHEMA
}, extra=vol.ALLOW_EXTRA)


async def async_setup(hass: HomeAssistant, yaml_config: Dict[str, Any]):
    """Activate Yandex Smart Home component."""
    # hass.data[DOMAIN] = yaml_config.get(DOMAIN, {})
    # async_register_http(hass, hass.data[DOMAIN])
    
    # await _setup_entry_from_config(hass)
    
    # return True

# async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    # async def update_cookie_and_token(**kwargs):
        # kwargs[CONF_SKILL_NAME] = entry.data[CONF_SKILL_NAME]
        # kwargs[CONF_SKILL_USER_ID] = entry.data[CONF_SKILL_USER_ID]
        # hass.config_entries.async_update_entry(entry, data=kwargs)
    
    # session = async_create_clientsession(hass)
    # yandex = YandexSession(session, entry.data['x_token'], entry.data['music_token'], entry.data['cookie'])
    # if CONF_SKILL in hass.data[DOMAIN]:
        # config = hass.data[DOMAIN][CONF_SKILL]
        # yandex.proxy = config.get(CONF_PROXY)
    # yandex.add_update_listener(update_cookie_and_token)

    # if not await yandex.refresh_cookies():
        # hass.components.persistent_notification.async_create(
            # "Необходимо заново авторизоваться в Яндексе. Для этого [добавьте "
            # "новую интеграцию](/config/integrations) с тем же логином.",
            # title="Yandex Smart Home")
        # return False
    
    # if CONF_SKILL_NAME in entry.data and CONF_SKILL_NAME not in hass.data[DOMAIN][CONF_SKILL]:
        # hass.data[DOMAIN][CONF_SKILL][CONF_SKILL_NAME] = entry.data[CONF_SKILL_NAME]
    # if CONF_SKILL_USER_ID in entry.data and CONF_SKILL_USER_ID not in hass.data[DOMAIN][CONF_SKILL]:
        # hass.data[DOMAIN][CONF_SKILL][CONF_SKILL_USER_ID] = entry.data[CONF_SKILL_USER_ID]
    # # light
    # # if CONF_SKILL_OAUTH_TOKEN in entry.data and CONF_SKILL_OAUTH_TOKEN not in hass.data[DOMAIN][CONF_SKILL]:
        # # hass.data[DOMAIN][CONF_SKILL][CONF_SKILL_OAUTH_TOKEN] = entry.data[CONF_SKILL_OAUTH_TOKEN]
    # # if CONF_SKILL_ID in entry.data and CONF_SKILL_ID not in hass.data[DOMAIN][CONF_SKILL]:
        # # hass.data[DOMAIN][CONF_SKILL][CONF_SKILL_ID] = entry.data[CONF_SKILL_ID]
    
    # await _setup_skill(hass, yandex)
    
    hass.data[DOMAIN] = {}
    hass.data[DOMAIN][CONFIG] = yaml_config.get(DOMAIN, {})
    hass.data[DOMAIN][DATA_CONFIG] = Config(
        settings=hass.data[DOMAIN][CONFIG].get(CONF_SETTINGS),
        should_expose=hass.data[DOMAIN][CONFIG].get(CONF_FILTER),
        entity_config=hass.data[DOMAIN][CONFIG].get(CONF_ENTITY_CONFIG)
    )
    hass.data[DOMAIN][NOTIFIER_ENABLED] = False
    async_register_http(hass)
    setup_notification(hass)

    return True
    
async def _setup_entry_from_config(hass: HomeAssistant):
    """Support legacy config from YAML."""
    _LOGGER.info("Trying to import config into entry...")
    if CONF_SKILL not in hass.data[DOMAIN]:
        hass.data[DOMAIN][CONF_SKILL] = {}
        _LOGGER.debug("No skill config - nothing to import")
        return
        
    config = hass.data[DOMAIN][CONF_SKILL]
    if CONF_USERNAME not in config:
        _LOGGER.debug("No username inside config - nothing to import")
        return
    
    # check if already configured
    for entry in hass.config_entries.async_entries(DOMAIN):
        if entry.unique_id == config[CONF_USERNAME]:
            _LOGGER.info("Config entry already configured")
            return
    
    if CONF_TOKEN not in config:
        # load config/.yandex_station.json
        x_token = utils.load_token_from_json(hass)
        if x_token:
            _LOGGER.info("x_token is inside json")
            config['x_token'] = x_token
    else:
        config['x_token'] = config[CONF_TOKEN]
        _LOGGER.info("Got x_token from config")
        
    # need username and token or password
    if 'x_token' not in config and CONF_PASSWORD not in config:
        _LOGGER.error("No password or x_token inside config")
        return
    _LOGGER.info("Credentials configured inside config - BEGIN IMPORT")
    
    hass.async_create_task(hass.config_entries.flow.async_init(
        DOMAIN, context={'source': SOURCE_IMPORT}, data=config
    ))
    
async def _setup_skill(hass: HomeAssistant, session: YandexSession):
    """Set up connection to Yandex Dialogs."""
    _LOGGER.info("Skill Setup") 
    try:
        skill = YandexSkill(hass, session)
        if not await skill.async_init():
            _LOGGER.error("Skill Setup Failed") 
            return False
            
        async def listener(event: Event):
            await skill.async_event_handler(event)
        
        hass.bus.async_listen('state_changed', listener)
        
    except Exception:
        _LOGGER.exception("Skill Setup error")
        return False
