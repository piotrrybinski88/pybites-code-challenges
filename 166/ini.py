import configparser
import re

class ToxIniParser:

    def __init__(self, ini_file):
        """Use configparser to load ini_file into self.config"""
        self.config = configparser.ConfigParser()
        self.config.read(ini_file, encoding='ASCII')

    @property
    def number_of_sections(self):
        """Return the number of sections in the ini file.
           New to properties? -> https://pybit.es/property-decorator.html
        """

        return len(self.config.sections())

    @property
    def environments(self):
        """Return a list of environments
           (= "envlist" attribute of [tox] section)"""
        list_of_environments = re.split(r'[,\s]', self.config['tox']['envlist'].replace('\n', ' '))
        return [word.encode('utf-8').strip() for word in list_of_environments if word]

    @property
    def base_python_versions(self):
        """Return a list of all basepython across the ini file"""
        return set([
            self.config[smth].get('basepython').encode('utf-8')
            for smth in self.config
            if self.config[smth].get('basepython')
            ])
