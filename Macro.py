#!/usr/bin/env python3
from pipython import GCSDevice
import time
from typing import Callable, Dict
from dataclasses import dataclass

@dataclass
class Cmd:
    name:str
    run: Callable[[], None]

class E727Device(GCSDevice):
    def __init__(self,model):
        super().__init__(model)
        print('connected: {}'.format(self.qIDN().strip()))
        self.Poll=0.05
        self.cmds=self.buildCmdList()
    def buildCmdList(self)->Dict[int,Cmd]:
        return {
        0b1111: Cmd("IDLE",  lambda: None),
        0b0001: Cmd("MOVE_1", lambda: self.MVR(0, 0.001)),
        0b0010: Cmd("MOVE_2", lambda: self.MVR(0, 0.002)),
        0b0011: Cmd("MOVE_5", lambda: self.MVR(0, 0.005)),
        0b0100: Cmd("MOVE_10",lambda: self.MVR(0, 0.010)),
        0b0000: Cmd("HALT",  lambda: self.HLT()),
        }   
    def qISQ(self):
        """
        Query the signal sequence of all digital input lines.
        """
        num_lines=self.qTIO()[0]
        if num_lines!=4:
            raise ValueError("This function only supports 4 digital input lines.")
        dic_input={}
        for i in range(4):
            dic_input[i]=int(self.qDIO(i+1))
        return dic_input
    def inputTimer(self):
        while True:
            dic_input=self.qISQ()
            bits=[dic_input[i]for i in range(4)]
            seq_input=''.join(str(b) for b in bits)
            cmd=self.cmds.get(int(seq_input,2))
            if cmd:
                print(f"Executing Command: {cmd.name} for input sequence: {seq_input}")
                cmd.run()
            else:
                print(f"No command mapped for input sequence: {seq_input}")
            time.sleep(self.Poll)

if __name__ == '__main__':
    dev=E727Device('E-727')
    dev.inputTimer()
