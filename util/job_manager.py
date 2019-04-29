import os
import json
from pathlib import Path


class JobManager:

    @staticmethod
    def parse_json(data, keys):
        for key in keys:
            if key in data:
                data[key] = json.loads(data[key])
        return data

    @staticmethod
    def get_job(job_id):
        path_name = '{}.json'.format(job_id)
        file_path = Path(os.path.join(os.path.dirname(__file__), '..', 'jobs', path_name))
        if not file_path.exists():
            return None
        with open(file_path, 'r') as f:
            try:
                data = json.load(f)
                if data['data'] is not None:
                    data['data'] = JobManager.parse_json(data['data'], ['poiStartName', 'poiEndName'])
            except BaseException as error:
                return {
                    'data': None,
                    'errorCode': 1001,
                    'message': '产生异常数据',
                }
            return {
                'data': data.get('data', None),
                'errorCode': data.get('errorCode', None),
                'message': data.get('message', None),
            }
