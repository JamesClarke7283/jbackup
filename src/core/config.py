import os
import tomllib
import tomli_w
from appdirs import user_config_dir

class Config:
    def __init__(self):
        self.app_name = "jbackup"
        self.config_dir = user_config_dir(self.app_name)
        self.config_file = os.path.join(self.config_dir, "config.toml")
        self.config = self.load_config()

    def load_config(self):
        if not os.path.exists(self.config_file):
            return self.create_default_config()
        
        with open(self.config_file, "rb") as f:
            return tomllib.load(f)

    def create_default_config(self):
        default_config = {
            "backup": {
                "source": "",
                "destination": "",
                "schedule": "daily",
                "compression_level": 3,
            },
            "remote": {
                "enabled": False,
                "host": "",
                "path": "",
                "delete_older_than": 30  # days
            }
        }

        self.save_config(default_config)
        return default_config

    def save_config(self, config=None):
        if config is None:
            config = self.config

        os.makedirs(self.config_dir, exist_ok=True)
        
        with open(self.config_file, "wb") as f:
            tomli_w.dump(config, f)

    def get(self, key, default=None):
        keys = key.split('.')
        value = self.config
        for k in keys:
            if k in value:
                value = value[k]
            else:
                return default
        return value

    def set(self, key, value):
        keys = key.split('.')
        config = self.config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value
        self.save_config()

    def set_source(self, source):
        self.set("backup.source", source)

    def set_destination(self, destination):
        self.set("backup.destination", destination)

    def set_schedule(self, schedule):
        self.set("backup.schedule", schedule)

    def set_compression_level(self, level):
        self.set("backup.compression_level", level)

    def set_remote_enabled(self, enabled):
        self.set("remote.enabled", enabled)

    def set_remote_host(self, host):
        self.set("remote.host", host)

    def set_remote_path(self, path):
        self.set("remote.path", path)

    def set_delete_older_than(self, days):
        self.set("remote.delete_older_than", days)

    def get_full_config(self):
        return self.config

    def reset_to_defaults(self):
        self.config = self.create_default_config()
        self.save_config()