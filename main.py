#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2020, Bosch Rexroth AG
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os 
import sys
import signal
import time
import sqlite3
from sqlite3 import Error
import json

import ctrlxdatalayer
from ctrlxdatalayer.variant import Variant

import app.nodes
import app.utils


def main():

    with ctrlxdatalayer.system.System("") as datalayer_system:
        datalayer_system.start(False)

        provider = datalayer_system.factory().create_provider("ipc://")  # alt: "tcp://boschrexroth:boschrexroth@127.0.0.1:2070"
        if provider is None:
            sys.exit(1)

        with provider:  # provider.close() is called automatically when leaving with block    

            db = os.environ.get("SNAP_COMMON") + "/rfs_parts.db"

            result = provider.start()
            if result is not ctrlxdatalayer.variant.Result.OK:
                print("ERROR Starting Data Layer Provider failed with:", result)
                return

            node_push = app.nodes.Push(provider, db)          # add part to db
            node_push.register_node()

            node_update = app.nodes.Update(provider, db)      # update part 
            node_update.register_node()

            node_archive = app.nodes.Archive(provider, db)    # create Archive file
            node_archive.register_node()

            node_restore = app.nodes.Restore(provider, db)    # restore Archive file
            node_restore.register_node()

            while provider.is_connected():
                time.sleep(5.0)                               # sleep in seconds

            node_push.unregister_node()
            del node_push

            node_update.unregister_node()
            del node_update

            node_archive.unregister_node()
            del node_archive                                    

            node_restore.unregister_node()
            del node_restore


    stop_ok = datalayer_system.stop(False)  


if __name__ == '__main__':
    main()
    





# def run_provider(provider : datalayer.provider.Provider):
#     offset = [0, 0]  # fetch offsets [queue, history]
    
#     db = os.environ.get("SNAP_COMMON") + "/rfs_parts.db"
    
#     node_push = app.nodes.Push(db)          # add part to db
#     node_update = app.nodes.Update(db)      # update part 
#     node_archive = app.nodes.Archive(db)    # create Archive file
#     node_restore = app.nodes.Restore(db)    # create Archive file


#     with datalayer.provider_node.ProviderNode(node_push.cbs, 1234) as node_1,       \
#             datalayer.provider_node.ProviderNode(node_update.cbs, 1234) as node_2,  \
#             datalayer.provider_node.ProviderNode(node_archive.cbs, 1234) as node_3, \
#             datalayer.provider_node.ProviderNode(node_restore.cbs, 1234) as node_4:   
#         result = provider.register_node("rfs/add_part", node_1)
#         if result != datalayer.variant.Result.OK:
#             print("Register add_part failed with: ", result)

#         result = provider.register_node("rfs/update_part", node_2)
#         if result != datalayer.variant.Result.OK:
#             print("Register update_part failed with: ", result)

#         result = provider.register_node("rfs/archive", node_3)
#         if result != datalayer.variant.Result.OK:
#             print("Register job_request failed with: ", result)

#         result = provider.register_node("rfs/restore", node_4)
#         if result != datalayer.variant.Result.OK:
#             print("Register pop failed with: ", result)

#         print('rfs-parts-db starting...')
#         result= provider.start()
#         if result != datalayer.variant.Result.OK:
#             print("Starting rfs-parts-db failed with: ", result)
            
#         while provider.is_connected():
#             time.sleep(5)
        
#         result = provider.stop()
 
#         result = provider.unregister_node("rfs/add_part")
#         result = provider.unregister_node("rfs/update_part")
#         result = provider.unregister_node("rfs/archive")
#         result = provider.unregister_node("rfs/restore")    