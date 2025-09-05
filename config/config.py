import json
import os.path


class Config:
    def __init__(self):
        self.path = '.json'
        self.back_up_path = '.json/back'

        if not os.path.exists(self.back_up_path):
            os.mkdir(self.back_up_path)

        key = 'config.json'
        if not os.path.isfile(os.path.join(self.path, key)):
            data = {
                'MYSQL': {
                    'host': '',
                    'port': '',
                    'user': '',
                    'password': '',
                    'db': '',
                    'charset': 'utf8'
                },
            }
            self.write(key, data, False)
            self.write(key, data, True)
             
    def write(self, path, data, isBackup=False):
        if isBackup:
            _path = os.path.join(self.back_up_path, path)
        else:
            _path = os.path.join(self.path, path)
        with open(_path, 'w') as f:
            f.write(json.dumps(data, indent=4, ensure_ascii=False))
            f.close()

    def read(self, key):
        with open(os.path.join(self.path, key), 'r', encoding='utf-8') as f:
            data = f.read()
            data = json.loads(data)
            f.close()
        return data

    def get_config(self, db_type='MYSQL', is_local=True):
        key = 'config.json'
        if os.path.isfile(os.path.join(self.path, key)):
            data = self.read(key)
            if is_local:
                data[db_type]['host'] = '127.0.0.1'
        else:
            data = None
        return data[db_type]