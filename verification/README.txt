Offline regression verification. BLE transport, cloud login, and selected setup
calls are mocked. These tests do not prove hardware behavior or real cloud login.
Separately, the author reports testing the 0.8.0b6 recovery behavior on an EcoFlow
DELTA 2 Max running firmware V1.0.0.204. After approximately 20 hours powered off,
the station connected within 1–2 seconds after power-on without a manual reload,
and all sensors worked. Version 0.8.1b1 retains that BLE code.
Use an isolated Python 3.14 environment, never a running Home Assistant install.
From the root of this repository or the unpacked release:

python -m pip install -r verification/requirements-tested.txt
PYTHONPATH=. python -m pytest -q verification/ --tb=short

The recorded test environment is Home Assistant 2026.9.1 / Python 3.14.7.
All 35 tests passed: 20 existing checks, 14 recovery/cleanup cases, and one AC
charging control case. Recovery
checks use the real Home Assistant Bluetooth manager, callback subscriptions,
entry states, and retry scheduling. Radio events and connection attempts are
simulated; a 20-hour absence is represented by old advertisement timestamps.
The reported physical test is separate from this reproducible automated suite.
Results for this build are in audit/tests_0.8.1b1.txt and audit/checks_0.8.1b1.json.
Other audit files retain the historical results for their original builds.
The audit and verification folders are not installed in Home Assistant.
