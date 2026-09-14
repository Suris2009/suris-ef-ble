# Suris EcoFlow BLE 0.8.1b2 — 100% local BLE, no internet required

**100% local BLE operation. Works without internet or EcoFlow cloud.**

> [!CAUTION]
> **UNOFFICIAL INTEGRATION — USE WITH CAUTION AND AT YOUR OWN RISK.**
> Version 0.8.1b2 is an unstable beta based on the tested 0.8.0 release.
> This project is not endorsed by EcoFlow and is not an official EcoFlow BLE / ha-ef-ble release.
> **No warranties are provided. To the maximum extent permitted by law, the authors
> and contributors accept no liability for its use or consequences.**
> Read the [full disclaimer](DISCLAIMER.md) before installation.

This project is developed exclusively for the author's own Home Assistant
installation and EcoFlow equipment. It is published as-is for transparency and
reference, without any promise of support or compatibility with other installations.

## 100% local operation — no internet or EcoFlow cloud required

Suris EcoFlow BLE provides **100% local Bluetooth monitoring and control** for
**EcoFlow DELTA 2 Max and one Extra Battery in slot 1**:

- **No internet or EcoFlow cloud connection is needed for operation** after device authentication.
- **A direct BLE connection** carries readings and commands locally between Home Assistant and the station.
- **Monitoring and control continue without internet access**, provided Home Assistant,
  Bluetooth, and the station remain available.
- **No separate `ef_ble` installation or running parent integration is required.**
- **Cloud sign-in is optional during setup:** provide your User ID manually for BLE
  authentication, or use email/password sign-in to obtain it from EcoFlow.

The required protocol implementation is included and is based on EcoFlow BLE 1.1.1,
with the DELTA 2 Max AC charging pause command backported from EcoFlow BLE 1.1.2.
Home Assistant and a working Bluetooth adapter or proxy are still required.
Use this integration for supervised testing with noncritical loads.

## Thanks to the EcoFlow BLE creators

**Thank you to [rabits](https://github.com/rabits) and everyone contributing to
[EcoFlow BLE / ha-ef-ble](https://github.com/rabits/ha-ef-ble)** for the Bluetooth
protocol implementation, device support, and continued development.
Special thanks to **[GnoX](https://github.com/GnoX)** for the connection and
authentication work credited in the [1.1.1 release](https://github.com/rabits/ha-ef-ble/releases/tag/v1.1.1)
and the AC charging pause control included in the
[1.1.2 release](https://github.com/rabits/ha-ef-ble/releases/tag/v1.1.2).
This integration would not be possible without their work. Suris does not claim
authorship of the upstream library; Suris modifications are maintained separately.
These acknowledgments do not imply endorsement of this project.

## Features and limitations

| Device | Entities defined in code |
| --- | --- |
| DELTA 2 Max | 37 sensors, 6 switches, 4 number controls, 2 input-current selectors |
| Extra Battery 1 | 29 sensors, created after battery detection |
| Extra Battery 2 and other models | Not supported by this build |

The code defines up to 66 sensors and creates them enabled by default.
Extra Battery 1 sensors appear after its data is detected. Readings can remain
unknown or unavailable until the station sends the corresponding data.
Power difference is calculated as **Output minus Input**. The update preserves
the integration domain, entity names, and all existing unique IDs.

**Car Input 2 remains experimental.** Both current selectors require fresh,
valid limits for both inputs before sending a command. This check does not
establish that the second input is interpreted correctly on every firmware.

**AC Charging Speed** uses a numeric entry field from **200 W to 2400 W** in
**100 W steps**, matching the range shown in the EcoFlow app for the author's
DELTA 2 Max. Enter 200, 300, 400, and so on up to 2400. Out-of-range values and
values between 100 W steps are rejected; they are not rounded automatically.
The **AC Charging** switch pauses or resumes grid charging without changing
the configured power.

**Max Charge Limit** and **Min Discharge Limit** also use numeric entry fields,
with their existing limits and 1% step. **Energy Backup Level** retains its
existing display mode and behavior.

Requires **Home Assistant Core 2026.8+** and a working Bluetooth adapter or proxy.

## BLE recovery retained from 0.8.0

When Home Assistant is waiting to retry setup and receives a new connectable BLE
advertisement from the configured station, the integration requests one early
retry through Home Assistant's existing reload mechanism. It ignores cached
advertisements during subscription and does not interrupt a working connection,
setup in progress, a disabled entry, or Home Assistant shutdown.

Repeated advertisements do not keep restarting setup. If the early attempt fails,
Home Assistant's ordinary retry schedule continues. A new disappearance and
reappearance, as reported by Home Assistant Bluetooth, permits another early retry.
This uses the existing scanner; it adds no polling timer or active scan request.
The Bluetooth adapter or proxy must be receiving the station's advertisements.

Failed BLE connections also skip platform unloading when platform setup has not
started. This avoids the misleading `Config entry was never loaded!` cleanup errors.
Existing XT60 controls, commands, authentication, sensors, and entity IDs are unchanged.

## Testing status

The author reports a physical test on an **EcoFlow DELTA 2 Max running firmware
V1.0.0.204**. After the station remained powered off for approximately 20 hours,
version 0.8.0b6 connected within 1–2 seconds after power-on without a manual
integration reload, and all sensors worked. Version 0.8.1b2 retains that BLE code.
The new AC charging controls have not yet been physically verified on the station.
This single reported test does not establish coverage of every feature, firmware,
Bluetooth environment, or configuration.

The recorded automated regression results are from **0.8.1b1**:
**35 tests passed** on Home Assistant Core 2026.9.1 and Python 3.14.7. They are
historical results, not a new test run for 0.8.1b2. The 0.8.1b2 release workflow
validates JSON, Python syntax, license notices, and the HACS archive layout.
The existing regression test now expects numeric entry for AC Charging Speed.
Phone rendering has not been checked on a live Home Assistant installation.
Recovery checks use the real Home Assistant Bluetooth manager and
configuration-entry APIs with synthetic advertisements and simulated connection
attempts. No live cloud login was exercised. Results and reproducible checks
are included under `audit/` and `verification/`.

## Installation and update

> [!WARNING]
> **Use caution: create a full Home Assistant backup and keep your previous build.**
> Supervise initial testing and use noncritical loads. Installing this software does
> not guarantee preservation of equipment, settings, or data.


### HACS installation (recommended)

Until this repository is accepted into the default HACS catalogue, add it
as a custom repository:

1. In HACS, open the top-right menu and select **Custom repositories**.
2. Add `https://github.com/Suris2009/suris-ef-ble` with category **Integration**.
3. Open the repository, select **Download**, expand **Need a different version?**,
   and select `v0.8.1b2`, the beta release.
4. Restart Home Assistant before configuring or testing the integration.

HACS downloads the dedicated `suris_ef_ble_xboost.zip` asset. Integration
files are stored directly at the archive root so HACS installs them into
`/config/custom_components/suris_ef_ble_xboost` without nested directories.

### Manual installation

1. Use the supplied `suris_ef_ble_0.8.1b2.zip`, or download it from
   [Releases](https://github.com/Suris2009/suris-ef-ble/releases).
2. Extract the ZIP on your computer and locate `custom_components/suris_ef_ble_xboost`.
3. Replace `/config/custom_components/suris_ef_ble_xboost` in Home Assistant with
   that complete folder. Do not merge old and new `_vendor` files. Restart Home Assistant.
4. Open **Settings → Devices & services → Add integration** and select
   **Suris EcoFlow BLE — 100% Local BLE (Unofficial)**. Select your discovered DELTA 2 Max.
5. Choose the EcoFlow sign-in option or manual User ID entry, using your own
   account associated with the station, and wait for BLE authentication.
6. Check readings, then verify each command directly on the station before
   connecting automations.

When updating an existing Suris installation, keep its integration entry to
preserve entity IDs. Older entry formats have migration and reauthentication
support. Disable the old `ef_ble` entry **for the same station**; entries for
other devices can remain. Close the EcoFlow app if it occupies the BLE connection:
the station supports only one such connection at a time.

The ZIP includes source code, licenses, and verification material. Home Assistant
needs only the complete component folder, including its LICENSE and NOTICE.
The root documents, `audit/`, and `verification/` do not need to be copied into `/config`.

## Use with caution

> [!CAUTION]
> Commands can turn outputs on or off and change charging settings.
> **Verify the actual state of the station. Supervise initial tests.**
> Incorrect or delayed readings must not be the sole basis for controlling
> critical equipment. This integration does not replace hardware protections.

After changes to Home Assistant, Bluetooth, or EcoFlow firmware, recheck the
connection, readings, and commands. If behavior is unexpected, stop testing and
disable the integration in **Settings → Devices & services**. To roll back,
restore your previous component folder and, if needed, your Home Assistant backup.

## Personal project and credentials

This project is developed exclusively for the author's own setup. Anyone choosing
to evaluate the published code must use their own station and account details and
accept that support and compatibility are not promised. No personal passwords,
User ID, or station identifiers belonging to the author are included in the code.

Email/password sign-in contacts the EcoFlow API over HTTPS to obtain a User ID.
The integration does not retain the email and password in its configuration entry.
The User ID, serial number, and Bluetooth address are stored locally in Home
Assistant configuration and may appear in backups. Manual User ID entry avoids
cloud sign-in through Suris. Device control after authentication uses local BLE.
Do not publish passwords, User IDs, serial numbers, addresses, or unredacted debug logs.

## License and attribution

Code and documentation are distributed under **Apache-2.0**. The upstream
license and original notices are preserved, and modified files are identified.
EcoFlow and DELTA names identify compatibility; no trademark rights are granted.
The license review is not a guarantee against intellectual-property, patent,
or contractual claims.

- [LICENSE](LICENSE), [NOTICE](NOTICE), [UPSTREAM_NOTICE.md](UPSTREAM_NOTICE.md).
- [Third-party components and trademarks](THIRD_PARTY_NOTICES.md).
- [Warnings and disclaimer of warranties and liability](DISCLAIMER.md).

**Use with caution and at your own risk. No warranties; no liability to the
maximum extent permitted by law. Mandatory legal rights remain unaffected.**
