from config import Config

if __name__ == '__main__':
    with Config("iforge_config.json") as cfg:
        """ update json from vendor.ini or bundle.ini """
        # cfg.update_from_ini("iForge.ini")

        # write
        cfg.write_vendor("iforge_config_vendor.ini")
        cfg.write_bundle("iforge_config_bundle.ini")
