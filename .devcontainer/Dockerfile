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

#
#   docker build -t automatous-io/shelly-gen4-esphome-builder:2026.8.2 .devcontainer
#
# The official ESPHome image and nothing else. The Home Assistant add-on is
# built from the same image, so a build here uses the toolchain an adopted
# device rebuilds with. Pinned by digest because the tag is republished.
FROM ghcr.io/esphome/esphome:2026.8.2@sha256:000c5ee5ee96d57208ee48f2d255f73713236f183959803e64cd0b00c39b277b

# The image's entrypoint execs `esphome` with its arguments, which would
# swallow the dev container's keep-alive command. What it otherwise does is
# point PlatformIO and the native ESP-IDF install at /cache, done here as
# image env so an interactive shell sees the same paths.
ENV PLATFORMIO_PLATFORMS_DIR=/cache/platformio/platforms \
    PLATFORMIO_PACKAGES_DIR=/cache/platformio/packages \
    PLATFORMIO_CACHE_DIR=/cache/platformio/cache \
    ESPHOME_ESP_IDF_PREFIX=/cache/idf
ENTRYPOINT []

RUN esphome version > /opt/esphome-version.txt

WORKDIR /workspaces
CMD ["/bin/bash"]
