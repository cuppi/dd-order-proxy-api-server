from flask import Flask, request
from web.controller.dd_order_controller import DDOrderController
from web.controller.dd_city_controller import DDCityController
from web.controller import error
from util.settings import BUILD_MODE
from logging.config import dictConfig
from datetime import datetime

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s-%(levelname)s]: %(message)s',
        'datefmt': '%Y-%m-%d %H:%M:%S %p',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default',
    }, 'file': {
        'class': 'logging.FileHandler',
        'filename': './logs/{}.log'.format(datetime.now().strftime('%Y-%m-%d_%H_%M_%S')),
        'formatter': 'default',
    }},
    'root': {
        'level': 'WARN',
        'handlers': ['wsgi', 'file'],
    }
})

app = Flask(__name__)


def safe_get_keys(dict, *args):
    values = []
    for key in args:
        if key not in dict:
            return False, key
        values.append(dict[key])
    return True, values


def do_main_process(is_get_estimate_fee):
    args = request.args
    success, data = safe_get_keys(
        args,
        'ticket',
        'startName',
        'startLocation',
        'endName',
        'endLocation',
    )
    if not success:
        return error(1001, '{} 参数不存在'.format(data))
    try:
        start_lat, start_lng = [float(n) for n in data[2].split(',')]
        end_lat, end_lng = [float(n) for n in data[4].split(',')]
    except ValueError as e:
        print(e)
        return error(1001, '无效经纬度信息')
    start_addr = args.get('startAddr', '')
    end_addr = args.get('endAddr', '')
    city_id = args.get('cityId', None)
    city_name = args.get('cityName', None)
    get_estimate_fee = 'yes' if is_get_estimate_fee else args.get('get_estimate_fee', None)

    return DDOrderController().apply_order_v2(
        ticket=data[0],
        start_name=data[1],
        start_location=(start_lat, start_lng),
        end_name=data[3],
        end_location=(end_lat, end_lng),
        city_id=city_id,
        city_name=city_name,
        start_addr=start_addr,
        end_addr=end_addr,
        get_estimate_fee=get_estimate_fee
    )

# @app.errorhandler(Exception)
# def all_exception_handler(e):
#    return error(1000)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/applyOrder', methods=['POST'])
def apply_order():
    args = request.args
    success, data = safe_get_keys(args, 'ticket', 'startAddress', 'endAddress', 'city')
    if not success:
        return error(1001, '{} 参数不存在'.format(data))
    return DDOrderController().apply_order(ticket=data[0], start=data[1], end=data[2], city=data[3])


@app.route('/applyOrderV2', methods=['POST'])
def apply_order_v2():
    do_main_process(False)


@app.route('/getEstimateFee', methods=['POST'])
def get_order_estimate_fee():
    do_main_process(True)



@app.route('/orderStatus', methods=['POST'])
def order_status():
    args = request.args
    success, data = safe_get_keys(args, 'jobId')
    if not success:
        return error(1001, '{} 参数不存在'.format(data))
    return DDOrderController().order_status(job_id=data[0])


@app.route('/cityList', methods=['POST'])
def city_list():
    args = request.args
    success, data = safe_get_keys(
        args,
        'ticket',
    )

    if not success:
        return error(1001, '{} 参数不存在'.format(data))
    return DDCityController().city_list(data[0])


@app.route('/cityListFromLocal', methods=['POST'])
def city_list_from_local():
    args = request.args
    force_refresh = int(args.get('forceRefresh', 1))
    return DDCityController().city_list_from_local(force_refresh=force_refresh == 1)


@app.route('/test', methods=['POST', 'GET'])
def test():
    return error(1006, 'mode is : {}'.format(BUILD_MODE))

if __name__ == '__main__':
    app.run(host='0.0.0.0')
