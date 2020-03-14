!/usr/bin/env python
# Copyright 2018 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import time
import gzip
import logging
import argparse
import datetime
from google.cloud import pubsub
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
TOPIC = 'sandiego'
INPUT = 'sensor_obs2008.csv.gz'
def publish(publisher, topic, events):
   numobs = len(events)
   if numobs > 0:
       logging.info('Publishing {0} events from {1}'.format(numobs, get_timestamp(events[0])))
       for event_data in events:
         publisher.publish(topic,event_data)
def get_timestamp(line):
   ## convert from bytes to str
   line = line.decode('utf-8')
   # look at first field of row
   timestamp = line.split(',')[0]
   return datetime.datetime.strptime(timestamp, TIME_FORMAT)
def simulate(topic, ifp, firstObsTime, programStart, speedFactor):
   # sleep computation
   def compute_sleep_secs(obs_time):
        time_elapsed = (datetime.datetime.utcnow() - programStart).seconds
        sim_time_elapsed = (obs_time - firstObsTime).seconds / speedFactor
        to_sleep_secs = sim_time_elapsed - time_elapsed
        return to_sleep_secs
   topublish = list() 
   for line in ifp:
       event_data = line   # entire line of input CSV is the message
       obs_time = get_timestamp(line) # from first column
