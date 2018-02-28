#! /usr/bin/env python
# _*_coding:utf-8_*_

import os
import platform
import signal
from analysis.Data import Data
from multiprocessing.process import Process


class ReadWriteProcess(Process):
    def __init__(self, read_write_queue, success_dir, failure_dir, damage_dir):
        super(ReadWriteProcess, self).__init__()
        self.read_write_queue = read_write_queue
        self.success_dir = success_dir
        self.failure_dir = failure_dir
        self.damage_dir = damage_dir

    def run(self):
        while True:
            data = self.read_write_queue.get(block=True, timeout=5)
            if data.data_status == Data.STATUS_FAILURE:
                data.write(self.failure_dir)
            elif data.data_status == Data.STATUS_SUCCESS:
                data.write(self.success_dir)
            elif data.data_status == Data.STATUS_DAMAGE:
                data.write(self.damage_dir)

    def stop(self):
        pid = self.pid
        print str(pid)+"::stop"
        system = platform.system()
        if 'Windows' in system:
            os.system("taskkill /F /T /PID " + str(pid))
        else:
            os.kill(pid, signal.SIGILL)

