import os

ENV = 'DEFAULT'

ENV = os.environ.get('ENV', ENV)
DOMAIN = os.environ.get('DOMAIN', 'momodel.cn')

SMTP_SERVER = 'smtp.exmail.qq.com'
USERNAME = 'service@momodel.ai'
PASSWORD = 'Mo123456'
SENDER = 'service@momodel.ai'

if ENV == 'PROD':
    WEB_ADDR = 'https://s.momodel.cn'
elif ENV == 'K8S':
    WEB_ADDR = 'https://{DOMAIN}'.format(DOMAIN=DOMAIN)
elif ENV == 'MO':
    WEB_ADDR = 'https://momodel.cn'
elif ENV in ['ZJU', 'ZJUNEW']:
    WEB_ADDR = 'https://mo.zju.edu.cn'
elif ENV == 'TEST':
    WEB_ADDR = 'https://test.momodel.cn'
elif ENV == 'ZKY':
    WEB_ADDR = 'https://cas.momodel.cn'
else:
    WEB_ADDR = 'https://momodel.cn'
