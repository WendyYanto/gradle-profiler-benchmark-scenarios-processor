import time
import os
from pprint import pprint
import csv
from typing import List
from datetime import datetime
from zoneinfo import ZoneInfo

class BuildInfo:
    def __init__(self, 
                 date_str,
                 epoch_time,
                 build_type = "", 
                 config_time = "", 
                 execution_time = "", 
                 local_build_cache_size = "", 
                 gc_time = "", 
                 gradle_version = "",
                 scenario = ""):
        self.date_str = date_str
        self.epoch_time = epoch_time
        self.build_type = build_type
        self.config_time = config_time
        self.execution_time = execution_time
        self.local_build_cache_size = local_build_cache_size
        self.gc_time = gc_time
        self.gradle_version = gradle_version
        self.scenario = scenario

    def __repr__(self):
        return f"BuildInfo(scenario={self.scenario}, date_str={self.date_str}, epoch={self.epoch_time}, build_type={self.build_type}, config_time={self.config_time}, execution_time={self.execution_time}, local_build_cache_size={self.local_build_cache_size}, gc_time={self.gc_time}, gradle_version={self.gradle_version}"

def parse_csv_to_build_infos(filepath: str) -> List[BuildInfo]:
    with open(filepath, newline='') as csvfile:
        reader = csv.reader(csvfile)
        scenarios = next(reader)
        gradle_version = next(reader)[1]
        next(reader) # skip the tasks

        column_name = next(reader)

        time_zone = ZoneInfo("Asia/Singapore")
        now = datetime.now(time_zone)
        current_date_time = now.strftime("%Y-%m-%d %H:%M:%S")

        epoch_time= time.time()
        build_info_dict = {}

        for row in reader:
            for idx, col in enumerate(row):
                if idx == 0:
                    continue
                # row[0] is the iteration such as 'warm-up build #1'
                # scenarios[idx] is scenario name of the iteration such as 'full build'
                key = f"{scenarios[idx]}_${row[0]}"
                if not key in build_info_dict:
                    build_info_dict[key] = BuildInfo(
                        date_str=current_date_time,
                        epoch_time = epoch_time,
                        build_type = row[0],
                        scenario = scenarios[idx],
                        gradle_version = gradle_version
                    )

                if (column_name[idx] == 'value'):
                    build_info_dict[key].build_type = col
                if (column_name[idx] == 'total execution time'):
                    build_info_dict[key].execution_time = col
                if (column_name[idx] == 'task start'):
                    build_info_dict[key].config_time = col
                if (column_name[idx] == 'garbage collection time'):
                    build_info_dict[key].gc_time = col
                if (column_name[idx] == 'local build cache size'):
                    build_info_dict[key].local_build_cache_size = col

    return sorted(build_info_dict.values(), key = lambda build_info: build_info.scenario)

build_infos = parse_csv_to_build_infos('profile-out/benchmark.csv')

pprint(build_infos)
