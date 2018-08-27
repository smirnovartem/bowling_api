from flask import send_from_directory
from bowling_app import bowling


bowling.static_url_path = ''


@bowling.route('/demo')
def demo():
    return send_from_directory('demo', 'demo.html')


@bowling.route('/demo/<path:path>')
def demo_file(path):
    return send_from_directory('demo', path)
