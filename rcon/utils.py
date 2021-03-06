import json
import redis
import logging
from rcon.cache_utils import get_redis_pool

logger = logging.getLogger('rcon')

def get_current_map(rcon):
    map_ = rcon.get_map()

    if map_.endswith('_RESTART'):
        map_ = map_.replace('_RESTART', '')

    return map_

def get_current_selection():
    red = redis.StrictRedis(connection_pool=get_redis_pool())
    selection = red.get("votemap_selection")
    if selection:
        selection = json.loads(selection)
    return selection

def numbered_maps(maps):
    return  {
        str(idx): map_
        for idx, map_ in enumerate(maps)
    }
   
def categorize_maps(maps):
    warfare_offsensive = {
        'warfare': [],
        'offensive': [],
    }
    for m in maps:
        if 'offensive' in m:
            warfare_offsensive['offensive'].append(m)
        if 'warfare' in m:
            warfare_offsensive['warfare'].append(m)

    return warfare_offsensive

def map_name(map_):
    name, *rest = map_.split('_')
    return name

LONG_HUMAN_MAP_NAMES = {
    "foy_warfare": "Foy",
    "stmariedumont_warfare": "St Marie du Mont",
    "hurtgenforest_warfare": "Hurtgen forest", 
    "utahbeach_warfare": "Utah beach", 
    "omahabeach_offensive_us": "Offensive Omaha beach", 
    "stmereeglise_warfare": "St Mere Eglise",
    "stmereeglise_offensive_ger": "Offensive St Mere eglise (Ger)", 
    "foy_offensive_ger": "Offensive Foy", 
    "purpleheartlane_warfare": "Purple Heart Lane",
    "purpleheartlane_offensive_us": "Offensive Purple Heart Lane",
    "hill400_warfare": "Hill 400",
    "hill400_offensive_US": "Offensive Hill 400",
    "stmereeglise_offensive_us": "Offensive St Mere Eglise (US)",
    "carentan_warfare": "Carentan",
    "carentan_offensive_us": "Offensive Carentan"
}

SHORT_HUMAN_MAP_NAMES = {
    "foy_warfare": "Foy",
    "stmariedumont_warfare": "St.Marie",
    "hurtgenforest_warfare": "Hurtgen", 
    "utahbeach_warfare": "Utah", 
    "omahabeach_offensive_us": "Off. Omaha", 
    "stmereeglise_warfare": "SME",
    "stmereeglise_offensive_ger": "Off. SME(Ger)", 
    "foy_offensive_ger": "Off. Foy", 
    "purpleheartlane_warfare": "PHL",
    "purpleheartlane_offensive_us": "Off. PHL",
    "hill400_warfare": "Hill400",
    "hill400_offensive_US": "Off. Hill400",
    "stmereeglise_offensive_us": "Off. SME (US)",
    "carentan_warfare": "Carentan",
    "carentan_offensive_us": "Off. Carentan"
}


NO_MOD_LONG_HUMAN_MAP_NAMES = {
    "foy_warfare": "Foy",
    "stmariedumont_warfare": "St Marie du Mont",
    "hurtgenforest_warfare": "Hurtgen orest", 
    "utahbeach_warfare": "Utah beach", 
    "omahabeach_offensive_us": "Omaha beach", 
    "stmereeglise_warfare": "St Mere Eglise",
    "stmereeglise_offensive_ger": "St Mere eglise (Ger)", 
    "foy_offensive_ger": "Foy", 
    "purpleheartlane_warfare": "Purple Heart Lane",
    "purpleheartlane_offensive_us": "Purple Heart Lane",
    "hill400_warfare": "Hill 400",
    "hill400_offensive_US": "Hill 400",
    "stmereeglise_offensive_us": "St Mere Eglise (US)",
    "carentan_warfare": "Carentan",
    "carentan_offensive_us": "Carentan"
}

NO_MOD_SHORT_HUMAN_MAP_NAMES = {
    "foy_warfare": "Foy",
    "stmariedumont_warfare": "St.Marie",
    "hurtgenforest_warfare": "Hurtgen", 
    "utahbeach_warfare": "Utah", 
    "omahabeach_offensive_us": "Omaha", 
    "stmereeglise_warfare": "SME",
    "stmereeglise_offensive_ger": "SME(Ger)", 
    "foy_offensive_ger": "Foy", 
    "purpleheartlane_warfare": "PHL",
    "purpleheartlane_offensive_us": "PHL",
    "hill400_warfare": "Hill400",
    "hill400_offensive_US": "Hill400",
    "stmereeglise_offensive_us": "SME (US)",
    "carentan_warfare": "Carentan",
    "carentan_offensive_us": "Carentan"
}


class FixedLenList:
    def __init__(self, key, max_len=100, serializer=json.dumps, deserializer=json.loads):
        self.red = redis.StrictRedis(connection_pool=get_redis_pool())
        self.max_len = max_len
        self.serializer = serializer
        self.deserializer = deserializer
        self.key = key

    def add(self, obj):
        self.red.lpush(self.key, self.serializer(obj))
        self.red.ltrim(self.key, 0, self.max_len - 1)

    def __getitem__(self, index):
        if isinstance(index, slice):
            if index.step:
                raise ValueError("Step is not supported")
            end = index.stop or -1
            start = index.start or 0
            return [
                self.deserializer(o) 
                for o in self.red.lrange(self.key, start, end)
            ]
        val = self.red.lindex(self.key, index)
        if val is None:
            raise IndexError("Index out of bound")
        return self.deserializer(val)

    def lpop(self):
        val = self.red.lpop(self.key)
        if val is None:
            return val
        return self.deserializer(val)

    def lpush(self, obj):
        self.red.lpush(self.key, self.serializer(obj))
