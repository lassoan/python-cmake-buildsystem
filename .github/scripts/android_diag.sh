# Repeat the threaded lru_cache tests to measure how often the hang reproduces
set -u
device_dir=/data/local/tmp/python
adb shell getprop ro.build.version.sdk
adb shell getprop ro.build.version.release
# 3.12 threading-heavy tests, repeated until a failure or the time limit
timeout 1200 adb shell "cd ${device_dir} && HOME=${device_dir} TMPDIR=${device_dir} PYTHONHOME=${device_dir} ./bin/python -m test -u none --timeout 60 -F test_functools -m '*lru_cache_threaded*' -m '*test_lru_cache_threaded*' 2>&1 | tail -n 60; echo @@exit=\$?@@" | tr -d '\r' | tail -n 70
echo "== done"
