from flask import Flask, request
from web.controller.dd_order_controller import DDOrderController
from web.controller import error
app = Flask(__name__)


def safe_get_keys(dict, *args):
    values = []
    for key in args:
        if key not in dict:
            return False, key
        values.append(dict[key])
    return True, values


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
    args = request.args
    success, data = safe_get_keys(args,
                                  'ticket',
                                  'startName',
                                  'startLat',
                                  'startLng',
                                  'endName',
                                  'endLat',
                                  'endLng',
                                  'city')
    if not success:
        return error(1001, '{} 参数不存在'.format(data))

    startAddr = args['startAddr'] if 'startAddr' in args else ''
    endAddr = args['endAddr'] if 'endAddr' in args else ''
    return DDOrderController().apply_order_v2(
        ticket=data[0],
        start_name=data[1],
        start_lat=data[2],
        start_lng=data[3],
        end_name=data[4],
        end_lat=data[5],
        end_lng=data[6],
        city_id=data[7],
        start_addr=startAddr,
        end_addr=endAddr
    )


@app.route('/orderStatus', methods=['POST'])
def orderStatus():
    args = request.args
    success, data = safe_get_keys(args, 'jobId')
    if not success:
        return error(1001, '{} 参数不存在'.format(data))
    return DDOrderController().order_status(job_id=data[0])


if __name__ == '__main__':
    app.run(host='0.0.0.0')
