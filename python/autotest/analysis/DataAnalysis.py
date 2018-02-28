#! /usr/bin/env python
# _*_coding:utf-8_*_
import os
import multiprocessing
import time
from multiprocessing import cpu_count
from analysis.Data import Data
from analysis.DataAnalysisProcess import DataAnalysisProcess
from analysis.ReadWriteProcess import ReadWriteProcess

MAX_DATA_ANALYSIS_PROCESS_NUM = cpu_count()
MAX_DATA_READ_WRITE_PROCESS_NUM = 1

TEST_SUCCESS_DIR = 'success'
TEST_FAILURE_DIR = 'failure'
TEST_DAMAGE_DIR = 'damage'


class DataAnalysis(object):
    def __init__(self, analysis_dir, out_dir):
        self.analysis_dir = analysis_dir
        self.read_write_list = []
        self.out_dir = out_dir
        self.data_queue = multiprocessing.Queue()
        self.read_write_queue = multiprocessing.Queue()

    def data_analysis(self):
        self.__get_data_path()
        success_dir = self.__create_analysis_dir(TEST_SUCCESS_DIR)
        failure_dir = self.__create_analysis_dir(TEST_FAILURE_DIR)
        damage_dir = self.__create_analysis_dir(TEST_DAMAGE_DIR)
        start_time = time.time()
        for i in range(MAX_DATA_READ_WRITE_PROCESS_NUM):
            read_write_process = ReadWriteProcess(self.read_write_queue, success_dir, failure_dir, damage_dir)
            self.read_write_list.append(read_write_process)
            read_write_process.start()
        for i in range(MAX_DATA_ANALYSIS_PROCESS_NUM):
            process = DataAnalysisProcess(self.data_queue, self.read_write_queue)
            process.start()
        while True:
            time.sleep(1)
            if self.read_write_queue.empty() and self.data_queue.empty():
                end_time = time.time()
                print "total_time::"+str(end_time-start_time)+" s"
                for r_w_process in self.read_write_list:
                    r_w_process.stop()
                break
        print "xml parse finish!"

    def __create_analysis_dir(self, path):
        my_dir = os.path.join(self.out_dir, path)
        if not os.path.exists(my_dir):
            os.mkdir(my_dir)
        return my_dir

    def __get_data_path(self):
        for root, dirs, files in os.walk(self.analysis_dir):
            for f in files:
                if '.xml' in os.path.splitext(f)[1]:
                    data_path = os.path.join(root, f)
                    data_log_path = os.path.join(root, f.split('.')[0]+".log")
                    data = Data()
                    data.data_path = data_path
                    data.data_log_path = data_log_path
                    data.device = os.path.basename(os.path.dirname(data_path))
                    data.date = os.path.basename(os.path.dirname(os.path.dirname(data_path)))
                    self.data_queue.put_nowait(data)

if __name__ == "__main__":
    ANALYSIS_DIR = 'D:/CodeWork/Python/autotest/auto_test/2017_10_19_14_03_45'
    OUT_DIR = 'D:/CodeWork/Python/autotest/auto_test/2017_10_19_14_03_45/result'
    print 'cpu core number::'+str(cpu_count())
    DataAnalysis(ANALYSIS_DIR, OUT_DIR).data_analysis()
