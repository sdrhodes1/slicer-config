import re
import json
import os


class Config:
    def __enter__(self):
        if os.path.exists(self.storage_filename):
            with open(self.storage_filename, 'r') as file:
                self.config_dict = json.load(file)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.storage_filename:
            with open(self.storage_filename, 'w+') as file:
                json.dump(self.config_dict, file)
        pass

    def __init__(self, json_filename):
        self.storage_filename = json_filename
        self.config_dict = {}

    def merge_dicts(self, d1, d2):
        for k in d2.keys():
            if k in d1.keys() and isinstance(d1[k], dict) and isinstance(d2[k], dict):
                self.merge_dicts(d1[k], d2[k])
            else:
                d1[k] = d2[k]

    def merge_new_config(self, new_dict):
        self.merge_dicts(self.config_dict, new_dict)

    def update_from_ini(self, filename):
        filename_root = '.'.join(filename.split(".")[:-1])
        big_dict = {}
        config_items = {}
        running_key = None
        with open(f"{filename_root}.ini") as file:
            line = f"\n{file.readline()}"  # prepend line with \n for regex detection
            while line != "\n":
                matches = re.findall("(?<=\s\[)[a-zA-Z]+.*[a-zA-Z]*(?=\]\s)", line)
                if matches:
                    matches = matches[0].split(":") + [""]
                    running_key = matches[1]
                    config_items[f"{running_key}"] = {"type": matches[0], "name": matches[1], "settings": {}}
                else:
                    if re.findall(" = ", line):
                        ln = line.strip('\n').split(" = ")
                        key = ln[0]
                        val = ""
                        if len(ln) > 1:
                            val = " = ".join(ln[1:])
                        config_items[running_key]["settings"].update({key: val})

                line = f"\n{file.readline()}"

        for name, value in config_items.items():
            try:
                big_dict[f"{value['type']}s"][name] = value
            except (TypeError, KeyError):
                big_dict[f"{value['type']}s"] = {name: value}

        self.merge_new_config(big_dict)

    def write_vendor(self, filename):
        filename_root = '.'.join(filename.split(".")[:-1])

        with open(f"{filename_root}.ini", 'w+') as file:
            file.write("# Generated by python config manager\n\n")

            for key in ['vendors', 'printer_models', 'prints', 'filaments', 'printers']:
                for k, v in self.config_dict[key].items():
                    type = v["type"]
                    name = v["name"]
                    output = [f"[{type}{f':{name}' if name else ''}]"]
                    for field, value in v["settings"].items():
                        output.append(f"{field} = {value}")

                    for ln in output:
                        file.write(f"{ln}\n")
                    file.write("\n")

    def write_bundle(self, filename):
        filename_root = '.'.join(filename.split(".")[:-1])

        with open(f"{filename_root}.ini", 'w+') as file:
            file.write("# Generated by python config manager\n\n")

            for key in ['printer_models', 'prints', 'filaments', 'printers', 'presetss']:
                for k, v in self.config_dict[key].items():
                    type = v["type"]
                    name = v["name"]
                    output = [f"[{type}{f':{name}' if name else ''}]"]
                    for field, value in v["settings"].items():
                        output.append(f"{field} = {value}")

                    for ln in output:
                        file.write(f"{ln}\n")
                    file.write("\n")