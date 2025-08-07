#The MIT License (MIT)
#
# Copyright (c) 2025 Konrad Peter
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from machine import Pin

class input_buttons:
    
    
    def __init__(self):
        
        self.keyup = Pin(18,Pin.IN)
        self.keydown = Pin(16,Pin.IN)
        self.keymiddle = Pin(17,Pin.IN)
        self.prevvals = [0] * 3
        self.currvals = [0] * 3

    def get_button_pushed(self):
        
        
        self.currvals[0] = self.keyup.value()
        self.currvals[1] = self.keymiddle.value()
        self.currvals[2] = self.keydown.value()
        
        #print(self.currvals[0])
        
        for i in range(len(self.currvals)):
            
            if self.currvals[i] == 0 and self.prevvals[i] == 1:
                retval = i
                break
            else:
                retval = -1
        
        #print("currval " + str(self.currvals[0]) + "prevval" + str(self.prevvals[0]))
        self.prevvals = self.currvals.copy()
        
        return retval
            