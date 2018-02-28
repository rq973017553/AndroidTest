from multiprocessing.pool import Pool
from core.NoDaemonProcess import NoDaemonProcess


class NoDaemonPool(Pool):

    Process = NoDaemonProcess
