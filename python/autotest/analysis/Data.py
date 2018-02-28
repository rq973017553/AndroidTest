#! /usr/bin/env python
# _*_coding:utf-8_*_

import os


class Data(object):
    STATUS_SUCCESS = 0
    STATUS_FAILURE = 1
    STATUS_DAMAGE = 2
    STATUS_UN_KNOWN = -1

    def __init__(self):
        self.data_path = ''
        self.data_log_path = ''
        self.date = ''
        self.device = ''
        self.data_status = Data.STATUS_UN_KNOWN

    def write(self, out_dir):
        new_data_path = os.path.join(out_dir, self.date+'_' +
                                     self.device+'_' +
                                     os.path.basename(self.data_path))
        new_data_log_path = os.path.join(out_dir, self.date + '_' +
                                         self.device + '_' +
                                         os.path.basename(self.data_log_path))
        self.__read_write(self.data_path, new_data_path)
        self.__read_write(self.data_log_path, new_data_log_path)

    @staticmethod
    def __read_write(read_path, write_path):
        with open(read_path, 'r') as input_stream:
            with open(write_path, 'w') as output_stream:
                for line in input_stream:
                    output_stream.write(line)
