import requests
from util.global_constant import get_city_lines
from util.tool import UrlTool
from . import error, success


class DDCityController:
    def city_list_from_local(self, **kwargs):
        force_refresh = kwargs.get('force_refresh', False)
        return success({
            'cityList': get_city_lines(force_refresh)
        })

    def city_list(self, ticket):
        project_name = 'default'
        spider_name = 'dd_city'
        crawl_url = UrlTool.combin_crawl_url(ticket)
        params = {
            'project': project_name,
            'spider': spider_name,
            'crawl_url': crawl_url,
        }
        res = requests.post('http://scrapyd:6800/schedule.json', params)
        data = res.json()
        if data['status'] == 'error':
            return error(1001, data['message'])
        if data['status'] == 'ok':
            return success(data)
        return error(1000, '系统繁忙')


