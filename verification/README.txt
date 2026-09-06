Offline regression verification. BLE transport, cloud login, and selected setup
calls are mocked. These tests do not prove hardware behavior or real cloud login.
Separately, the author reports testing the integration on a real EcoFlow DELTA 2 Max.
That report does not establish coverage of every feature, firmware, or configuration.
Use an isolated Python 3.14 environment, never a running Home Assistant install.
From the root of this repository or the unpacked release:

python -m pip install -r verification/requirements-tested.txt
PYTHONPATH=. python -m pytest -q verification/test_integration.py --tb=short

The recorded test environment is Home Assistant 2026.9.1 / Python 3.14.6.
The original 0.8.0b1 audit is historical; current results are recorded separately
in audit/tests_0.8.0b4.txt and audit/release_checks.json.
The audit and verification folders are not installed in Home Assistant.
