set -u
device_dir=/data/local/tmp/python
adb shell getprop ro.build.version.release
adb push "$(dirname "$0")/android_diag.py" "${device_dir}/" > /dev/null
adb shell "cd ${device_dir} && HOME=${device_dir} TMPDIR=${device_dir} PYTHONHOME=${device_dir} ./bin/python -X faulthandler android_diag.py 2>&1; echo @@exit=\$?@@" | tr -d '\r'
echo "== done"
