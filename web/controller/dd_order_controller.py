import requests
from . import error, success
from util.job_manager import JobManager
import csv
import os

class DDOrderController:
    def apply_order(self, ticket, start, end, city):
        with open(os.path.join(os.getcwd(), 'city.csv'), 'r') as readFile:
            reader = csv.reader(readFile)
            lines = [city[1] for city in list(reader)]
            if city not in lines:
                return error(1101, '不存在的城市')
        base_url = 'https://open.es.xiaojukeji.com/webapp/entry'
        client_id = '7f96250878304f8b6f554ec27dd1a82a_test'
        crawl_url = '{}?client_id={}&ticket={}'.format(base_url, client_id, ticket)
        project_name = 'default'
        spider_name = 'dd_order'
        params = {
            'project': project_name,
            'spider': spider_name,
            'crawl_url': crawl_url,
            'start': start,
            'end': end,
            'city': city
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

