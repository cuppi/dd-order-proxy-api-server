import os


class LuaLoader:
    @staticmethod
    def load_script(file_name: str):
        lua_script: str = ''
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'DDOrderProxy', 'lua_script', file_name), 'r') as f:
            lua_script += f.read()
        return lua_script
