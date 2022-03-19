from config import Config

if __name__ == '__main__':
    with Config("iforge_config.json") as cfg:
        """ update json from vendor.ini or bundle.ini """
        # cfg.update_from_ini("iForge.ini")

        # write
        cfg.write_vendor("vendor/iForge.ini")
        cfg.write_bundle("iForge-PrusaSlicer-config-bundle.ini")
