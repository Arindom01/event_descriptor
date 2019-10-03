import yaml
import anyconfig
import os
import sys
from pathlib import Path
import logging
sys.path.append(".")
sys.path.append("..")
sys.path.append("...")


logging.basicConfig(
        datefmt = '%Y-%m-%d %H:%M:%S ',
        format = '%(asctime)s %(message)s',
        level=logging.INFO)

class App_Conf:


    proj_dir_path = os.path.dirname(os.path.realpath(__file__))
    _conf = anyconfig.load(os.path.join(Path(__file__).parent.parent , "src/config/config.yml"))
        
    @staticmethod
    def config():
        try:
            if os.environ['DEPLOY_ENV'] == 'LOCAL':
                ret = App_Conf._conf['non-prod']
            elif os.environ['DEPLOY_ENV'] == 'PROD':
                ret = App_Conf._conf['prod']
            else:
                ret = App_Conf._conf['non-prod']
        except Exception as ex:
            ret = App_Conf._conf['non-prod']
            logging.info("Envoronment Variable DEPLOY_ENV not set")
        return ret
