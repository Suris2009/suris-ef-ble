# Suris EcoFlow BLE 0.8.0b4

> [!CAUTION]
> **UNOFFICIAL / UNSTABLE BETA — USE WITH CAUTION AND AT YOUR OWN RISK.**
> The author has tested the integration on a real station. It remains an unstable beta.
> This project is not endorsed by EcoFlow and is not an official EcoFlow BLE / ha-ef-ble release.
> **No warranties are provided. To the maximum extent permitted by law, the authors
> and contributors accept no liability for its use or consequences.**
> Read the [full disclaimer](DISCLAIMER.md) before installation.

An independent Home Assistant integration for **EcoFlow DELTA 2 Max and one
Extra Battery in slot 1**, using Bluetooth. A separate `ef_ble` installation is
not required. The protocol implementation is based on EcoFlow BLE 1.1.1.
Use this beta for supervised testing with noncritical loads.

## Thanks to the EcoFlow BLE creators

**Thank you to [rabits](https://github.com/rabits) and everyone contributing to
[EcoFlow BLE / ha-ef-ble](https://github.com/rabits/ha-ef-ble)** for the Bluetooth
protocol implementation, device support, and continued development.
Special thanks to **[GnoX](https://github.com/GnoX)** for the connection and
authentication work credited in the [1.1.1 release](https://github.com/rabits/ha-ef-ble/releases/tag/v1.1.1).
This integration would not be possible without their work. Suris does not claim
authorship of the upstream library; Suris modifications are maintained separately.
These acknowledgments do not imply endorsement of this project.

## Features and limitations

| Device | Entities defined in code |
| --- | --- |
| DELTA 2 Max | 37 sensors, 5 switches, 4 number controls, 2 input-current selectors |
| Extra Battery 1 | 29 sensors, created after battery detection |
| Extra Battery 2 and other models | Not supported by this build |

The code defines up to 66 sensors. **This does not mean that all 66 are enabled
in an installed integration.** Some entities may be disabled in Home Assistant.
Extra Battery 1 sensors appear after its data is detected. Readings can remain
unknown or unavailable until the station sends the corresponding data.
Power difference is calculated as **Output minus Input**. The update preserves
the integration domain, unique IDs, entity inventory, and existing command logic.

**Car Input 2 remains experimental.** Both current selectors require fresh,
valid limits for both inputs before sending a command. This check does not
establish that the second input is interpreted correctly on every firmware.

Requires **Home Assistant Core 2026.8+** and a working Bluetooth adapter or proxy.

## Testing status

**The author has tested the integration on a real EcoFlow DELTA 2 Max station.**
This does not establish coverage of every feature, firmware, or configuration.
The release remains an **unofficial, unstable beta**.

Additional automated checks for publication ran on Home Assistant Core 2026.9.1
and Python 3.14.6: **20 tests passed**. Those automated checks used mocked BLE
and cloud calls; they did not exercise real hardware or a live cloud login.
The recorded results are included under `audit/` and `verification/`.

## Installation and update

> [!WARNING]
> **Use caution: create a full Home Assistant backup and keep your previous build.**
> Supervise initial testing and use noncritical loads. Installing this beta does
> not guarantee preservation of equipment, settings, or data.

1. Download `suris_ef_ble_0.8.0b4.zip` from [Releases](https://github.com/Suris2009/suris-ef-ble/releases).
   Select the release marked **Pre-release**. There is no stable release of this version.
2. Extract the ZIP on your computer and locate `custom_components/suris_ef_ble_xboost`.
3. Replace `/config/custom_components/suris_ef_ble_xboost` in Home Assistant with
   that complete folder. Do not merge old and new `_vendor` files. Restart Home Assistant.
4. Open **Settings → Devices & services → Add integration** and select
   **Suris EcoFlow BLE (Unofficial Beta)**. Select your discovered DELTA 2 Max.
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

## Credentials and use by other owners

**Other DELTA 2 Max owners can use this integration.** No personal passwords,
User ID, or station identifiers belonging to the author were found in the code.
Each user selects their own station and provides their own account details.
The compatibility restriction concerns the device model and battery slot.

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
