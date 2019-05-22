from math import sin, cos, sqrt, atan2, radians
from util.settings import BUILD_MODE


class MathTool:
    @staticmethod
    def distance_between_location(l1, l2):
        # approximate radius of earth in km
        R = 6373.0
        lat1 = l1[0]
        lng1 = l1[1]
        lat2 = l2[0]
        lng2 = l2[1]

        dlng = lng2 - lng1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlng / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return R * c


class UrlTool:
    @staticmethod
    def combin_crawl_url(ticket):
        base_url = ''
        if BUILD_MODE == 'beta':
            base_url = 'https://open.es.xiaojukeji.com/webapp/entry'
        if BUILD_MODE == 'pro':
            base_url = 'https://open.es.xiaojukeji.com/webapp/home/index'
        client_id = '7f96250878304f8b6f554ec27dd1a82a_test'
        crawl_url = '{}?client_id={}&ticket={}'.format(base_url, client_id, ticket)
        return crawl_url
