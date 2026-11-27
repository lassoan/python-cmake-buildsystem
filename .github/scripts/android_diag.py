# Check timed lock acquisition (sem_timedwait in Python 3.12 without sem_clockwait)
import subprocess, sys, textwrap

CASES = {
    "A: timed acquire of a held lock times out": """
        import _thread, time
        lock = _thread.allocate_lock(); lock.acquire()
        t0 = time.monotonic(); got = lock.acquire(True, 0.5)
        print(f"got={got} after {time.monotonic() - t0:.2f} s")
    """,
    "B: timed acquire wakes up on release": """
        import _thread, threading, time
        lock = _thread.allocate_lock(); lock.acquire()
        threading.Timer(0.2, lock.release).start()
        t0 = time.monotonic(); got = lock.acquire(True, 10)
        print(f"got={got} after {time.monotonic() - t0:.2f} s")
    """,
    "C: 5 threads waiting on an Event, 1 us switch interval": """
        import sys, threading, time
        sys.setswitchinterval(1e-6)
        for rep in range(20):
            start = threading.Event()
            threads = [threading.Thread(target=start.wait, args=(10,)) for _ in range(5)]
            for t in threads: t.start()
            t0 = time.monotonic(); start.set()
            for t in threads: t.join()
            if time.monotonic() - t0 > 5: print(f"rep {rep}: slow {time.monotonic() - t0:.1f} s")
        print("20 repetitions done")
    """,
}
for name, code in CASES.items():
    for attempt in range(3):
        watchdog = "import faulthandler; faulthandler.dump_traceback_later(20, exit=True)\n"
        r = subprocess.run([sys.executable, "-c", watchdog + textwrap.dedent(code)], capture_output=True, text=True)
        out = (r.stdout + r.stderr).strip().splitlines()
        print(f"{name} [{attempt}] rc={r.returncode}: " + (" | ".join(out[:3]) if out else ""), flush=True)
