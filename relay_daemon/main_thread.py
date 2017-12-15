#!/usr/bin/env python
#############################################
#   Title: Relay Daemon Main Thread         #
# Project: VTGS Relay Control Daemon        #
# Version: 2.0                              #
#    Date: Dec 15, 2017                     #
#  Author: Zach Leffke, KJ4QLP              #
# Comment:                                  #
#   -Relay Control Daemon Main Thread       #
#   -Intended for use with systemd          #
#############################################

import threading
import time

from logger import *
import numato

class Main_Thread(threading.Thread):
    def __init__ (self, args):
        threading.Thread.__init__(self, name = 'Main_Thread')
        self._stop      = threading.Event()
        self.args = args
        self.ssid = args.ssid

        self.state  = 'BOOT' #BOOT, STANDBY, ACTIVE, FAULT
        self.main_log_fh = setup_logger(self.ssid, ts=args.startup_ts, log_path=args.log_path)
        self.logger = logging.getLogger(self.ssid) #main logger

    def run(self):
        print "Main Thread Started..."
        self.logger.info('Launched main thread')
        try:
            while (not self._stop.isSet()): 
                if self.state == 'BOOT':
                    #Daemon activating for the first time
                    #Activate all threads
                    #State Change:  BOOT --> STANDBY
                    #All Threads Started
                    if self._init_threads():#if all threads activate succesfully
                        self.logger.info('Successfully Launched Threads, Switching to ACTIVE State')
                        #self.set_state_standby()
                        self.set_state('ACTIVE')
                    else:
                        self.set_state('FAULT')
                    pass
                elif self.state == 'ACTIVE':
                    #Describe ACTIVE here
                    #read uplink Queue from C2 Radio thread
                    print 'ACTIVE'
                    time.sleep(1)
                    pass

        except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
            print "\nCaught CTRL-C, Killing Threads..."
            self.logger.warning('Caught CTRL-C, Terminating Threads...')
            self.relay_thread.stop(self.name)
            self.relay_thread.join() # wait for the thread to finish what it's doing
            #self.server_thread.stop(self.name)
            #self.server_thread.join() # wait for the thread to finish what it's doing
            self.logger.warning('Terminating Main Thread...')

            sys.exit()
        sys.exit()

    def set_state(self, state):
        self.state = state
        self.logger.info('Changed STATE to: {:s}'.format(self.state))
        if self.state == 'ACTIVE':
            time.sleep(1)
            self.tlm_bcn_wd.start()
        if self.state == 'FAULT':
            pass
            time.sleep(10)

    def _init_threads(self):
        try:
            #Initialize Relay Thread
            self.logger.info('Setting up Relay Thread')
            self.relay_thread = numato.Ethernet_Relay(self.args) 
            self.relay_thread.daemon = True

            #Initialize Server Thread
            #self.logger.info('Setting up Server Thread')
            #self.server_thread = Server_Thread(self.args) 
            #self.server_thread.daemon = True

            #Launch threads
            self.logger.info('Launching Relay Thread')
            self.relay_thread.start() #non-blocking
    
            #self.logger.info('Launching Server Thread')
            #self.server_thread.start() #non-blocking

            return True
        except Exception as e:
            self.logger.warning('Error Launching Threads:')
            self.logger.warning(str(e))
            self.logger.warning('Setting STATE --> FAULT')
            self.state = 'FAULT'
            return False

    def stop(self):
        print '{:s} Terminating...'.format(self.name)
        self.logger.info('{:s} Terminating...'.format(self.name))
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()
