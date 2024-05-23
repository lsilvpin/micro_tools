import sys, os
sys.path.insert(0, os.path.abspath("."))
from main.library.utils.core.path_helper import get_root_dir


class SettingsTool:
    def get(self, key: str) -> str | None:
        settings_dict: dict = self.__get_settings_dict()
        if key == "env":
            key = "MICRO_TOOLS_SYS_ENV"
        setting_from_env: str = os.getenv(key)
        if setting_from_env is not None:
            return setting_from_env
        elif key in settings_dict:
            return settings_dict[key]
        else:
            return None

    def set(self, key: str, value: str) -> None:
        settings_dict: dict = self.__get_settings_dict()
        settings_dict[key] = value
        root_dir: str = get_root_dir()
        env_var_value: str = os.getenv("MICRO_TOOLS_SYS_ENV")
        assert env_var_value is not None, "Environment variable 'MICRO_TOOLS_SYS_ENV' is not set."
        settings_file_path: str = root_dir + "/.env." + env_var_value + ".env"
        with open(settings_file_path, "w") as file:
            for key, value in settings_dict.items():
                file.write(key + "=\"" + value + "\"\n")
    
    def delete(self, key: str) -> None:
        settings_dict: dict = self.__get_settings_dict()
        if key in settings_dict:
            settings_dict.pop(key)
            root_dir: str = get_root_dir()
            env_var_value: str = os.getenv("MICRO_TOOLS_SYS_ENV")
            assert env_var_value is not None, "Environment variable 'MICRO_TOOLS_SYS_ENV' is not set."
            settings_file_path: str = root_dir + "/.env." + env_var_value + ".env"
            with open(settings_file_path, "w") as file:
                for key, value in settings_dict.items():
                    file.write(key + "=\"" + value + "\"\n")

    def __get_settings_dict(self) -> dict:
        root_dir: str = get_root_dir()
        env_var_value: str = os.getenv("MICRO_TOOLS_SYS_ENV")
        assert env_var_value is not None, "Environment variable 'MICRO_TOOLS_SYS_ENV' is not set."
        settings_file_path: str = root_dir + "/.env." + env_var_value + ".env"
        assert os.path.exists(settings_file_path), "Settings file not found: " + settings_file_path
        settings_dict: dict = {}
        with open(settings_file_path, "r") as file:
            for line in file:
                key, value = line.split("=")
                valueWithoutNewLine: str = value.replace("\n", "")
                valueWithoutQuotes: str = valueWithoutNewLine.replace("\"", "")
                settings_dict[key] = valueWithoutQuotes
        assert len(settings_dict) > 0, "Settings file is empty: " + settings_file_path
        settings_dict_keys: list = list(settings_dict.keys())
        assert "sys_name" in settings_dict_keys, "Setting 'sys_name' not found in settings file: " + settings_file_path
        return settings_dict