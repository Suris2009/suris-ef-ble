Offline regression verification. BLE transport, cloud login, and selected setup
calls are mocked. These tests do not prove hardware behavior or real cloud login.
Separately, the author reports testing the 0.8.0b6 recovery behavior on an EcoFlow
DELTA 2 Max running firmware V1.0.0.204. After approximately 20 hours powered off,
the station connected within 1–2 seconds after power-on without a manual reload,
and all sensors worked. Version 0.8.1 retains that BLE code.
Use an isolated Python 3.14 environment, never a running Home Assistant install.
From the root of this repository or the unpacked release:

python -m pip install -r verification/requirements-tested.txt
PYTHONPATH=. python -m pytest -q verification/ --tb=short

The recorded 0.8.1b1 test environment is Home Assistant 2026.9.1 / Python 3.14.7.
All 35 tests passed for 0.8.1b1: 20 existing checks, 14 recovery/cleanup cases,
and one AC charging control case. Recovery
checks use the real Home Assistant Bluetooth manager, callback subscriptions,
entry states, and retry scheduling. Radio events and connection attempts are
simulated; a 20-hour absence is represented by old advertisement timestamps.
The reported physical test is separate from this reproducible automated suite.
Those historical results are in audit/tests_0.8.1b1.txt and audit/checks_0.8.1b1.json.
For 0.8.1, all 36 tests passed in the isolated Python 3.14.7 environment.
The new Sound switch test checks heartbeat state, BLE packet fields, and
disconnected behavior. The author confirmed Sound works on a physical DELTA 2
Max after installing 0.8.1b3 on 27 September 2026.
Other audit files retain the historical results for their original builds.
The audit and verification folders are not installed in Home Assistant.
