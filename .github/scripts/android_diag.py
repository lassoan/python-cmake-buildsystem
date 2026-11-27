# Repeat the threaded lru_cache tests to measure how often the hang reproduces
import faulthandler, io, sys, time, unittest
from test import test_functools
loader = unittest.TestLoader()
loader.testNamePatterns = ["*lru_cache_threaded*"]
suite = loader.loadTestsFromModule(test_functools)
print("tests per iteration:", suite.countTestCases(), flush=True)
start = time.monotonic()
i = 0
while time.monotonic() - start < 900:
    i += 1
    faulthandler.dump_traceback_later(60, exit=True)
    result = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0).run(suite)
    faulthandler.cancel_dump_traceback_later()
    if not result.wasSuccessful():
        print(f"iteration {i}: failures={result.failures} errors={result.errors}", flush=True)
    if i % 50 == 0:
        print(f"{i} iterations in {time.monotonic() - start:.0f} s", flush=True)
print(f"NO HANG: {i} iterations in {time.monotonic() - start:.0f} s", flush=True)
