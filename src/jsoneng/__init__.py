import os
import json

path = os.getcwd() + '\\jdb\\'
path_string = ''

def set_path(string):
    global path
    path = os.getcwd() + string

def dictionary_kv(dictionary, key, value):
    dictionary[key] = value
    return dictionary

def set_path_string(args, create_flag):
    global path_string
    if (args):
        path_string = str(args[0]) + '\\'
    if os.path.exists(path + path_string) == False:
        if create_flag == True:
            os.makedirs(path + path_string)
        else:
            return False
    return path_string

def save(dictionary, name=''):
    if (name):
        with open(str(name) + '.json', 'w') as outfile:
            json.dump(dictionary, outfile, indent=4)
    else:
        with open('eng.json', 'w') as outfile:
            json.dump(dictionary, outfile, indent=4)

def create(dictionary, *args):
    path_string = set_path_string(args, True)
    with open(path + path_string + 'eng.json', 'w') as outfile:
        json.dump(dictionary, outfile, indent=4)

def retrieve(*args):
    path_string = set_path_string(args, False)
    if path_string == False:
        return False
    with open(path + path_string + 'eng.json', 'r') as f:
        return(json.load(f))

def retrieve_k(key, *args):
    path_string = set_path_string(args, False)
    if path_string == False:
        return False
    with open(path + path_string + 'eng.json', 'r') as f:
        if key in json.load(f):
            with open(path + path_string + 'eng.json', 'r') as f:
                return(json.load(f)[key])
        else:
            return False

def update(dictionary, *args):
    path_string = set_path_string(args, False)
    if path_string == False:
        return False
    with open(path + path_string + 'eng.json', 'w') as outfile:
        json.dump(dictionary, outfile, indent=4)
        return True

def update_kv(key, value, *args):
    path_string = set_path_string(args, False)
    if path_string == False:
        return False
    with open(path + path_string + 'eng.json', 'w') as outfile:
        json.dump({key: value}, outfile, indent=4)
        return True

def patch(dictionary, *args):
    path_string = set_path_string(args, False)
    if path_string == False:
        return False
    with open(path + path_string + 'eng.json', 'r') as f:
        data=(json.load(f))
        data.update(dictionary)
        with open(path + path_string + 'eng.json', 'w') as outfile:
            json.dump(data, outfile, indent=4)
            return True

def patch_kv(key, value, *args):
    path_string = set_path_string(args, False)
    if path_string == False:
        return False
    with open(path + path_string + 'eng.json', 'r') as f:
        data=(json.load(f))
        data.update({key: value})
        with open(path + path_string + 'eng.json', 'w') as outfile:
            json.dump(data, outfile, indent=4)
            return True

def delete(*args):
    if (args):
        path_string = str(args[0]) + '\\'
    if os.path.exists(path + path_string + 'eng.json'):
        os.remove(path + path_string + 'eng.json')
        os.rmdir(path + path_string)
        return True
    else:
        print('The selected file does not exist')
        return False

def delete_k(key, *args):
    if (args):
        path_string = str(args[0]) + '\\'
    if os.path.exists(path + path_string + 'eng.json'):
        with open(path + path_string + 'eng.json', 'r') as f:
            if key in json.load(f):
                data = json.load(f)
                data.pop(key)
                with open(path + path_string + 'eng.json', 'w') as outfile:
                    json.dump(data, outfile, indent=4)
                    return True
            else:
                print('The selected key does not exist')
                return False
    else:
        print('The selected file does not exist')
        return False

class JsonDB:
    def __init__(self, path=None, indent=4):
        self.path = path or os.path.join(os.getcwd(), 'jdb')
        self.indent = indent

    def _get_file_path(self, *args):
        dir_path = os.path.join(self.path, *args)
        file_path = os.path.join(dir_path, 'jdb.json')
        return dir_path, file_path
    
    def _write_json(self, data, file_path):
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=self.indent)
    
    def set_indent(self, indent):
        self.indent = indent

    def create(self, dictionary, *args):
        dir_path, file_path = self._get_file_path(*args)
        os.makedirs(dir_path, exist_ok=True)
        self._write_json(dictionary, file_path)

    def retrieve(self, *args):
        _, file_path = self._get_file_path(*args)
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                return json.load(f)
        return False

    def retrieve_k(self, key, *args):
        data = self.retrieve(*args)
        return data.get(key, False) if data else False

    def update(self, dictionary, *args):
        _, file_path = self._get_file_path(*args)
        if os.path.exists(file_path):
            self._write_json(dictionary, file_path)
            return True
        return False

    def update_kv(self, key, value, *args):
        return self.update({key: value}, *args)

    def patch(self, dictionary, *args):
        _, file_path = self._get_file_path(*args)
        if os.path.exists(file_path):
            with open(file_path, 'r+') as f:
                data = json.load(f)
                data.update(dictionary)
                f.seek(0)
                self._write_json(data, file_path)
            return True
        return False

    def patch_kv(self, key, value, *args):
        return self.patch({key: value}, *args)

    def delete(self, *args):
        dir_path, file_path = self._get_file_path(*args)
        if os.path.exists(file_path):
            os.remove(file_path)
            os.rmdir(dir_path)
            return True
        print('The selected file does not exist')
        return False

    def delete_k(self, key, *args):
        _, file_path = self._get_file_path(*args)
        if os.path.exists(file_path):
            with open(file_path, 'r+') as f:
                data = json.load(f)
                if key in data:
                    del data[key]
                    f.seek(0)
                    f.truncate()
                    self._write_json(data, file_path)
                    return True
                print('The selected key does not exist')
                return False
        print('The selected file does not exist')
        return False

    def print(self, *args):
        data = self.retrieve(*args)
        if data:
            print(json.dumps(data, indent=4))
        else:
            print("Database not found")

    def c(self, key, value, *args):
        self.create({key: value}, *args)

    def r(self, key, *args):
        return self.retrieve_k(key, *args)

    def u(self, key, value, *args):
        self.patch_kv(key, value, *args)

    def d(self, key, *args):
        self.delete_k(key, *args)
    
    def p(self, key, *args):
        value = self.retrieve_k(key, *args)
        if value:
            print({key: value})
        else:
            print("Key not found")

    def i(self, value, *args):
        data = self.retrieve(*args)
        highest = max(map(int, data.keys()), default=-1)
        self.update_kv(str(highest + 1), value, *args)

    def l(self, desc, value='', *args):
        if value:
            value = ' ' + value
        self.i(desc + value, *args)

    def f(self, key, value, *args):
        if not self.retrieve_k(key, *args):
            self.update_kv(key, value, *args)
