Offline regression verification. BLE transport, cloud login, and selected setup
calls are mocked. These tests do not prove hardware behavior or real cloud login.
Separately, the author reports physical testing of earlier releases. The new BLE
recovery behavior in 0.8.0b6 has not been tested on a physical station.
Use an isolated Python 3.14 environment, never a running Home Assistant install.
From the root of this repository or the unpacked release:

python -m pip install -r verification/requirements-tested.txt
PYTHONPATH=. python -m pytest -q verification/ --tb=short

The recorded test environment is Home Assistant 2026.9.1 / Python 3.14.6.
All 34 tests passed: 20 existing checks and 14 recovery/cleanup cases. Recovery
checks use the real Home Assistant Bluetooth manager, callback subscriptions,
entry states, and retry scheduling. Radio events and connection attempts are
simulated; a 20-hour absence is represented by old advertisement timestamps.
No 20-hour hardware endurance test was performed.
Results for this build are in audit/tests_0.8.0b6.txt and audit/checks_0.8.0b6.json.
Other audit files retain the historical results for their original builds.
The audit and verification folders are not installed in Home Assistant.
