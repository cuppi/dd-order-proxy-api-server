import requests
from . import error, success
from util.job_manager import JobManager
from util.global_constant import city_lines
from util.math_tool import MathTool


class DDOrderController:

    def combin_crawl_url(self, ticket):
        base_url = 'https://open.es.xiaojukeji.com/webapp/entry'
        client_id = '7f96250878304f8b6f554ec27dd1a82a_test'
        crawl_url = '{}?client_id={}&ticket={}'.format(base_url, client_id, ticket)
        return crawl_url

    def apply_order(self, ticket, start, end, city):
        if city not in [c['name'] for c in city_lines]:
            return error(1101, '不存在的城市')

        project_name = 'default'
        spider_name = 'dd_order'
        crawl_url = self.combin_crawl_url(ticket)
        params = {
            'project': project_name,
            'spider': spider_name,
            'crawl_url': crawl_url,
            'version': 'v1',

            'start': start,
            'end': end,
            'city': city,
        }
        res = requests.post('http://scrapyd:6800/schedule.json', params)
        data = res.json()
        if data['status'] == 'error':
            return error(1001, data['message'])
        if data['status'] == 'ok':
            return success({
                'jobId': data['jobid']
            })
        return error(1000, '系统繁忙')

    def apply_order_v2(self, **kwargs):
        ticket = kwargs.get('ticket', None)
        start_name = kwargs.get('start_name', None)
        start_addr = kwargs.get('start_addr', None)
        start_lat, start_lng = kwargs.get('start_location', None)
        end_name = kwargs.get('end_name', None)
        end_addr = kwargs.get('end_addr', None)
        end_lat, end_lng = kwargs.get('end_location', None)
        city_id = kwargs.get('city_id', None)
        city_name = kwargs.get('city_name', None)

        if city_id is None and city_name is None:
            return error(1101, '城市参数为空')

        if city_id and str(city_id) not in [c['id'] for c in city_lines] or \
                city_name and city_name not in [c['name'] for c in city_lines]:
            return error(1101, '不存在的城市')

        if MathTool.distance_between_location((start_lat, start_lng), (end_lat, end_lng)) < 0.1:
            return error(1102, '起点与终点过近')
        crawl_url = self.combin_crawl_url(ticket)
        project_name = 'default'
        spider_name = 'dd_order'

        params = {
            'project': project_name,
            'spider': spider_name,
            'crawl_url': crawl_url,
            'version': 'v2',
            'cityId': city_id,
            'startAddr': start_addr,
            'startName': start_name,
            'start_location': '{}, {}'.format(start_lat, start_lng),
            'endAddr': end_addr,
            'endName': end_name,
            'end_location': '{}, {}'.format(end_lat, end_lng),
        }
        res = requests.post('http://scrapyd:6800/schedule.json', params)
        data = res.json()
        if data['status'] == 'error':
            return error(1001, data['message'])
        if data['status'] == 'ok':
            return success({
                'jobId': data['jobid']
            })
        return error(1000, '系统繁忙')

    def order_status(self, job_id):
        data = JobManager.get_job(job_id)
        if data is None:
            return success({
                'status': 'running'
            })
        if data['data']:
            return success({
                'status': 'finished',
                'data': data['data']
            })
        else:
            return error(error_code=data['errorCode'], message=data['message'])

