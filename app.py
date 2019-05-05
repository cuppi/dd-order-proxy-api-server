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
    success, data = safe_get_keys(args, 'ticket', 'startAddress', 'endAddress')
    if not success:
        return error(1001, '{} 参数不存在'.format(data))
    return DDOrderController().apply_order(ticket=data[0], start=data[1], end=data[2])


@app.route('/orderStatus', methods=['POST'])
def orderStatus():
    args = request.args
    success, data = safe_get_keys(args, 'jobId')
    if not success:
        return error(1001, '{} 参数不存在'.format(data))
    return DDOrderController().order_status(job_id=data[0])


if __name__ == '__main__':
    app.run(host='0.0.0.0')
