import os
import sys
sys.path.append("../dnp3/service")

from dnp3.master import MyMaster, MyLogger, AppChannelListener, SOEHandler, MasterApplication
from dnp3.dnp3_to_cim import CIMMapping
from pydnp3 import opendnp3, openpal

def run_master(HOST="127.0.0.1",PORT=20000, DNP3_ADDR=10, convertion_type='Shark', object_name='632633'):
    dnp3_to_cim = CIMMapping(conversion_dict="conversion_dict.json", model_line_dict="model_line_dict.json")
    elements_to_device = {'632633': 'Shark'}
    application_1 = MyMaster(HOST=HOST,  # "127.0.0.1
                            LOCAL="0.0.0.0",
                            PORT=int(PORT),
                            DNP3_ADDR=int(DNP3_ADDR),
                            log_handler=MyLogger(),
                            listener=AppChannelListener(),
                            soe_handler=SOEHandler(object_name, convertion_type, dnp3_to_cim),
                            master_application=MasterApplication())

    masters = [application_1]
    # application.channel.SetLogFilters(openpal.LogFilters(opendnp3.levels.ALL_COMMS))
    # print('Channel log filtering level is now: {0}'.format(opendnp3.levels.ALL_COMMS))
    import time
    SLEEP_SECONDS = 1
    time.sleep(SLEEP_SECONDS)
    # group_variation = opendnp3.GroupVariationID(32, 2)
    # time.sleep(SLEEP_SECONDS)
    # print('\nReading status 1')
    # application_1.master.ScanRange(group_variation, 0, 12)
    # time.sleep(SLEEP_SECONDS)
    # print('\nReading status 2')
    # application_1.master.ScanRange(opendnp3.GroupVariationID(32, 2), 0, 3, opendnp3.TaskConfig().Default())
    # time.sleep(SLEEP_SECONDS)
    print('\nReading status 3')
    # application_1.slow_scan.Demand()

    # application_1.fast_scan_all.Demand()

    for master in masters:
        master.fast_scan_all.Demand()
    while True:
        cim_full_msg = {'simulation_id': 1234, 'timestamp': 0, 'messages':{}}
        for master in masters:
            cim_msg = master.soe_handler._cim_msg
            cim_full_msg['messages'].update(cim_msg)
        print(cim_full_msg)
        time.sleep(60)


    print('\nStopping')
    for master in masters:
        master.shutdown()
    # application_1.shutdown()
    exit()

    # When terminating, it is necessary to set these to None so that
    # it releases the shared pointer. Otherwise, python will not
    # terminate (and even worse, the normal Ctrl+C won't help).
    application_1.master.Disable()
    application_1 = None
    application_1.channel.Shutdown()
    application_1.channel = None
    application_1.manager.Shutdown()

if __name__ == "__main__":

    import argparse
    import json
    parser = argparse.ArgumentParser()
    parser.add_argument("name", help="name of dnp3 outstation")
    # parser.add_argument("feeder_info",help='feeder info directory for y-matrix, etc.')
    args = parser.parse_args()
    with open("device_ip_port_config_all.json") as f:
        device_ip_port_config_all = json.load(f)

    device_ip_port_dict = device_ip_port_config_all[args.name]
    print(device_ip_port_dict)
    run_master(device_ip_port_dict['ip'],
               device_ip_port_dict['port'],
               device_ip_port_dict['link_local_addr'],
               device_ip_port_dict['conversion_type'],
               '632633')