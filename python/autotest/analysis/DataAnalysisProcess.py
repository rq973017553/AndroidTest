#! /usr/bin/env python
# _*_coding:utf-8_*_

try:
  import xml.etree.cElementTree as ET
except ImportError:
  import xml.etree.ElementTree as ET
import Queue
from Data import Data
from multiprocessing.process import Process


class DataAnalysisProcess(Process):
    def __init__(self, data_queue, read_write_queue):
        super(DataAnalysisProcess, self).__init__()
        self.data_queue = data_queue
        self.read_write_queue = read_write_queue

    def run(self):
        print "create DataAnalysisProcess::"+str(self.pid)
        while True:
            try:
                data = self.data_queue.get_nowait()
                tree = None
                try:
                    tree = ET.parse(data.data_path)
                except SyntaxError:
                    print data.data_path+"::xml parse error"
                if tree is not None:
                    list_node = tree.getiterator('testcase')
                    for node in list_node:
                        if data.data_status == Data.STATUS_FAILURE:
                            break
                        for children in node.getchildren():
                            text = children.text
                            if 'failure' in text:
                                data.data_status = Data.STATUS_FAILURE
                                break
                            elif 'success' in text:
                                data.data_status = Data.STATUS_SUCCESS
                    self.read_write_queue.put_nowait(data)
                else:
                    data.data_status = Data.STATUS_DAMAGE
                    self.read_write_queue.put_nowait(data)
                    continue
            except Queue.Empty:
                break
