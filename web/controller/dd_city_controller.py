from util.global_constant import get_city_lines
from . import error, success


class DDCityController:
    def city_list(self, **kwargs):
        force_refresh = kwargs.get('force_refresh', False)
        return success({
            'cityList': get_city_lines(force_refresh)
        })


