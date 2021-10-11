#!/bin/bash
#
# Copyright (c) 2021 Seagate Technology LLC and/or its Affiliates
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# For any questions about this software or licensing,
# please email opensource@seagate.com or cortx-questions@seagate.com.
#

set -euo pipefail # exit on failures

source ./config.sh
source ./env.sh
source ./sh/functions.sh

add_separator "Creating Message Bus PODs"

if kubectl get pods | grep zookeeper; then
  add_separator  zookeeper pod is already deployed.
else
  replace_tags ./k8s-blueprints/zookeper.yaml.template
  pull_images_for_pod ./k8s-blueprints/zookeper.yaml
  kubectl create -f ./k8s-blueprints/zookeper.yaml
fi

if kubectl get pods | grep kafka; then
  add_separator  kafka pod is already deployed.
else
  replace_tags ./k8s-blueprints/kafka.yaml.template
  pull_images_for_pod ./k8s-blueprints/kafka.yaml
  kubectl create -f ./k8s-blueprints/kafka.yaml
fi

set +x
while [ "$(kubectl get pod | safe_grep 'zookeper\|kafka' | safe_grep Running | wc -l)" -lt 1 ]; do
  echo
  kubectl get pod | grep 'NAME\|zookeper\|kafka'
  echo
  echo Zookeper/Kafka pod is not yet in Running state, re-checking ...
  echo '(hit CTRL-C if it is taking too long)'
  sleep 5
done
set -x

set_var_SVC_IP zoo1
echo "ZOOKEPER_SVC='$SVC_IP'" >> env.sh
set_var_SVC_IP kaf1
echo "KAFKA_SVC='$SVC_IP'" >> env.sh
set_var_SVC_EXTERNAL_IP kaf1
echo "KAFKA_EXTERNAL_IP='$SVC_EXTERNAL_IP'" >> env.sh

set +x

add_separator SUCCESSFULLY CREATED OPENLDAP PODS