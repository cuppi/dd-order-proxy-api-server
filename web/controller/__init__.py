from flask import jsonify


def create_network_result(data=None, error_code=None, message='系统繁忙'):
    if error_code is None:
        return jsonify({
            'data': {
                **data
            },
            'errorCode': 0,
            'message': ''
        })
    else:
        return jsonify({
            'data': {},
            'errorCode': error_code,
            'message': message
        })


def success(data):
    return create_network_result(data)


def error(error_code, message='系统繁忙'):
    return create_network_result(error_code=error_code, message=message)
