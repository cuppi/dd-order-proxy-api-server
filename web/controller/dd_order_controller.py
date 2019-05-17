import requests
from . import error, success
from util.job_manager import JobManager
from util.global_constant import city_lines


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
        ticket = kwargs.get('', None)
        start_name = kwargs.get('start_name', None)
        start_lat = kwargs.get('start_lat', None)
        start_lng = kwargs.get('start_lng', None)
        end_name = kwargs.get('end_name', None)
        end_lat = kwargs.get('end_lat', None)
        end_lng = kwargs.get('end_lng', None)
        city_id = kwargs.get('city_id', None)
        start_addr = kwargs.get('start_addr', None)
        end_addr = kwargs.get('end_addr', None)

        if city_id not in [c['id'] for c in city_lines]:
            return error(1101, '不存在的城市')

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
            'start_location': (start_lat, start_lng),
            'endAddr': end_addr,
            'endName': end_name,
            'end_location': (end_lat, end_lng),
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
            return error({
                'status': 'running'
            })
        if data['data']:
            return success({
                'status': 'finished',
                'data': data['data']
            })
        else:
            return error(error_code=data['errorCode'], message=data['message'])

