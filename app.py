"""
title:   RealSenseOPC client application config class
author:  Nicholas Loehrke 
date:    June 2022
license: TODO
"""

import configparser
import logging as log
from typing import Union

MSG_ERROR_SHUTDOWN = "~~~~~~~~~~~~~~~Error Exited Application~~~~~~~~~~~~~~\n"


class Config():
    def __init__(self, file_name, required_data=None):
        """creates config object

        :param file_name: name of file
        :type file_name: string
        :param required_data: nested dictionary with section titles and key. Values
        be anything or None
        :type required_data: dict
        :raises FileNotFoundError: if unable to open file
        :raises RuntimeError: if there is a discrepency between the configuration
        file data and the requried data dict
        """
        self._file_name = file_name
        config_file = configparser.ConfigParser()
        try:
            file_list = config_file.read(self._file_name)
        except configparser.Error as e:
            raise e

        if len(file_list) <= 0:
            raise FileNotFoundError(f'"{self._file_name}" was not found')

        self._data = config_file.__dict__['_sections'].copy()

        if required_data is not None:
            self._required_data = required_data
            validity = self.is_valid()
            if len(validity) > 0:
                raise RuntimeError(
                    f'"{self._file_name}" is missing required configuration data: "{validity}"')

    def get_value(self, section: str, key: str, fallback=None) -> str:
        """gets config file value at specified location

        :param section: values section title
        :type section: string
        :param key: values key title
        :type key: string
        :param fallback: fallback value if unable to find value in file
        :type fallback: string
        :return: value
        :rtype: string
        """
        try:
            return self._data[section][key]
        except KeyError:
            if isinstance(fallback, str):
                log.warning(
                    f'Failed to get value from "[{section}]: {key}". Defaulting to "{fallback}"')
                return fallback
            log.error(f'Failed to get value from "[{section}]: {key}"')
            raise KeyError

    def is_valid(self) -> Union[bool, list]:
        """checks if configuration file contains the required data

        :return: validity
        :rtype: bool
        """
        missing = []
        for section in self._required_data:
            if section == 'nodes':
                if len(self._data[section]) < 1:
                    missing.append((section, 'any_node'))
            else:
                for key in self._required_data[section]:
                    if key not in self._data[section]:
                        missing.append((section, key))
        return missing

    @property
    def data(self) -> dict:
        """configuration file contents

        :return: config file dictionary 
        :rtype: dict
        """
        return self._data


    @property
    def name(self) -> str:
        """file name getter"""
        return self._file_name