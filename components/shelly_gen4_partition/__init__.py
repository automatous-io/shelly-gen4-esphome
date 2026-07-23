#
# Copyright 2026 AUTOMATOUS.IO
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
#
from pathlib import Path

import esphome.config_validation as cv
from esphome.components import esp32

DEPENDENCIES = ["esp32"]
CODEOWNERS = ["@automatous-io"]

CONFIG_SCHEMA = cv.Schema({})


async def to_code(config):
    # ESPHome skips auto-generated partition table when one is already
    # registered; remote/adopted builds can't reach files outside the cloned
    # repo; the stock table must ship inside this component.
    esp32.add_extra_build_file(
        "partitions.csv",
        Path(__file__).parent / "shelly-gen4-stock.csv",
    )
