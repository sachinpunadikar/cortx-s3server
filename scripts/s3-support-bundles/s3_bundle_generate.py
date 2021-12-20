#!/usr/bin/env python3

# Copyright (c) 2021 Seagate Technology LLC and/or its Affiliates
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
# For any questions about this software or licensing,
# please email opensource@seagate.com or cortx-questions@seagate.com.

import sys
import os
import shutil
import tarfile
import argparse
from cortx.utils.cortx.const import Const
from s3confstore.cortx_s3_confstore import S3CortxConfStore

class S3SupportBundle:
    """ Generate support bundle for S3."""

    bundle_id = None
    target_path = None
    cluster_conf = None
    services = None
    files = []
    tmp_dir = None

    # Constant service names from utils.
    self.service_haproxy = Const.SERVICE_S3_HAPROXY.value
    self.service_s3server = Const.SERVICE_S3_SERVER.value
    self.service_authserver = Const.SERVICE_S3_AUTHSERVER.value
    self.service_bgscheduler = Const.SERVICE_S3_BGSCHEDULER.value
    self.service_bgworker = Const.SERVICE_S3_BGWORKER.value

    def generate_bundle_common(self):
        """ Generate support bundle for the S3 common logs"""
        print("Collect Support logs for common started")
        # Collect s3cluster config file if available

        # Collect S3 deployment log

        # Collect disk usage info
        disk_usage = os.path.join (self.tmp_dir, "disk_usage.txt")
        os.system(f"df -k > {disk_usage}")
        files.append(disk_usage)

        # Collect ram usage
        ram_usage = os.path.join (self.tmp_dir, "ram_usage.txt")
        os.system(f"free -h > {ram_usage}")
        files.append(ram_usage)

        # Colelct CPU info
        cpu_info = os.path.join (self.tmp_dir, "cpuinfo.txt")
        os.system(f"cat /proc/cpuinfo > {cpu_info}")
        files.append(cpu_info)


        # Collect listening port numbers
        node_port_info = os.path.join (self.tmp_dir, "node_port_info.txt")
        os.system("netstat -tulpn | grep -i listen > {node_port_info} 2>&1")
        files.append(node_port_info)

        # Collect rpm package names of s3
        rpm_info = os.path.join (self.tmp_dir, "s3_rpm_info.txt")
        os.system("rpm -qa | grep cortx-s3 > {rpm_info} 2>&1")
        files.append(rpm_info)

        # Collect System Audit logs if available
        files.append("/var/log/audit")

        print("Collect Support logs for common completed")

    def generate_bundle_s3server(self):
        """ Generate support bundle for the S3 Server logs"""
        print("Collect Support logs for S3 server started")
        print("Collect Support logs for S3 Server completed")

    def generate_bundle_authserver(self):
        """ Generate support bundle for the Authserver logs"""
        print("Collect Support logs for AuthServer started")
        print("Collect Support logs for AuthServer completed")

    def generate_bundle_bgscheduler(self):
        """ Generate support bundle for the BG delete scheduler logs"""
        print("Collect Support logs for BG delete scheduler started")
        print("Collect Support logs for BG delete scheduler completed")

    def generate_bundle_bgworker(self):
        """ Generate support bundle for the BG delete worker logs"""
        print("Collect Support logs for BG delete worker started")
        print("Collect Support logs for BG delete worker completed")

    def generate_bundle_haproxy(self):
        """ Generate support bundle for the haproxy logs"""
        print("Collect Support logs for haproxy started")
        print("Collect Support logs for haproxy completed")

    def generate_bundle(self):
        """ Generate support bundle for the S3 logs"""
        print(f"bundle_id: {self.bundle_id}")
        print(f"target_path: {self.target_path}")
        print(f"cluster_conf: {self.cluster_conf}")
        print(f"services: {self.services}")

        self.tmp_dir = os.path.join(self.target_path, "s3", "temp_data")
        print(f"tmp_dir: {self.tmp_dir}")
        os.makedirs(self.tmp_dir, exist_ok=True)

        # parse services param
        self.services = self.services.split(",")

        # common logs for support bundle
        self.generate_bundle_common()
        if self.service_haproxy in self.services:
            self.generate_bundle_haproxy()
        if self.service_s3server in self.services:
            self.generate_bundle_s3server()
        if self.service_authserver in self.services:
            self.generate_bundle_authserver()
        if self.service_bgscheduler in self.services:
            self.generate_bundle_bgscheduler()
        if self.service_bgworker in self.services:
            self.generate_bundle_bgworker()

        # Generate bundle using tar
        tar_name = "s3_" + self.bundle_id
        print(f"tar_name: {tar_name}")
        tar_file_name = os.path.join(self.target_path, "s3", tar_name + '.tar.gz')
        os.makedirs(os.path.dirname(tar_file_name), exist_ok=True)
        print(f"tar_file_name: {tar_file_name}")
        with tarfile.open(tar_file_name, 'w:gz') as tar:
            for file in self.files:
                tar.add(file)
        tar.close()
        print(f"S3 support bundle generated successfully at {tar_file_name} !!!")

def main():
    parser = argparse.ArgumentParser(description='''Support Bundle for S3 logs.''')
    parser.add_argument('-b', dest='bundle_id', help='Unique bundle id')
    parser.add_argument('-t', dest='path', help='Path to store the created bundle')
    parser.add_argument('-c', dest='cluster_conf', help="Cluster config file path")
    parser.add_argument('-s', dest='services', help='List of services for Support Bundle')
    args = parser.parse_args()
    S3SupportBundle(args.bundle_id, args.path, args.cluster_conf, args.services).generate_bundle()

if __name__ == '__main__':
    main()