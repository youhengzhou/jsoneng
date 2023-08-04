import os
import json


class JsonDB:
    def __init__(self, dictionary=None, path=None, indent=4):
        self.path = path or os.path.join(os.getcwd(), "jdb")
        self.indent = indent
        if dictionary is not None:
            self.create(dictionary)

    def _get_file_path(self, *args):
        dir_path = os.path.join(self.path, *args)
        file_path = os.path.join(dir_path, "jdb.json")
        return dir_path, file_path

    def _write_json(self, data, file_path):
        with open(file_path, "w") as f:
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
            with open(file_path, "r") as f:
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
            with open(file_path, "r+") as f:
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
        print("The selected file does not exist")
        return False

    def delete_k(self, key, *args):
        _, file_path = self._get_file_path(*args)
        if os.path.exists(file_path):
            with open(file_path, "r+") as f:
                data = json.load(f)
                if key in data:
                    del data[key]
                    f.seek(0)
                    f.truncate()
                    self._write_json(data, file_path)
                    return True
                print("The selected key does not exist")
                return False
        print("The selected file does not exist")
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
        self.update_kv(key, value, *args)

    def d(self, key, *args):
        self.delete_k(key, *args)

    def p(self, key, value, *args):
        self.patch_kv(key, value, *args)

    def ptr(self, key, *args):
        value = self.retrieve_k(key, *args)
        if value:
            print({key: value})
        else:
            print("Key not found")

    def i(self, value, *args):
        data = self.retrieve(*args)
        highest = max(map(int, data.keys()), default=-1)
        self.patch_kv(str(highest + 1), value, *args)

    # def k(self, desc, value, *args):
    #     data = self.retrieve(*args)
    #     highest = max(map(int, data.keys()), default=-1)
    #     self.patch_kv(str(highest + 1) + ' ' + desc, value, *args)

    def v(self, desc, value="", *args):
        if value:
            value = " " + value
        self.i(desc + value, *args)

    def f(self, key, value, *args):
        if not self.retrieve_k(key, *args):
            self.patch_kv(key, value, *args)
