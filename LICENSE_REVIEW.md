# License review and publication preparation — 0.8.0b4

**Suris EcoFlow BLE: 100% local BLE operation. No internet or EcoFlow cloud connection is required during operation.**

Date: September 6, 2026. Reviewed the supplied `suris_ef_ble_0.8.0b3.zip` and
the resulting 0.8.0b4. This is a source, attribution, and open-source license
review, not a legal opinion covering every possible right.

**Release status: UNOFFICIAL, UNSTABLE BETA. Use with caution. No warranties;
the disclaimer applies to the maximum extent permitted by law.**

## Verified provenance

Upstream: [rabits/ha-ef-ble](https://github.com/rabits/ha-ef-ble),
release [v1.1.1](https://github.com/rabits/ha-ef-ble/releases/tag/v1.1.1),
commit `ef02d81a2720de256548a5d515af814cc3244ee9`.
The source archive for that exact tag was downloaded rather than the mutable main branch.

| Item reviewed | Finding |
| --- | --- |
| 40 Python files under `_vendor/eflib` | Provenance traced to upstream 1.1.1 |
| 34 unchanged files | Byte-identical to upstream |
| Six modified files | Full differences recorded; prominent modification headers added |
| Upstream SHA-256 values recorded in the input archive | All match files from the public 1.1.1 tag |
| LICENSE in the input archive | Identical to LICENSE at the exact upstream commit |
| Separate upstream NOTICE | Absent from the reviewed upstream source tree |
| Docker notice in LICENSE | Present in upstream itself; retained verbatim |
| Font files, APKs, firmware, manuals, equipment photographs | Not distributed in this release |
| Third-party Python packages | Installed separately; their bytes are not bundled in the ZIP |

Download provenance: `audit/upstream_provenance.json`.
Per-file hashes: `audit/vendored_sources.json`.
Changes relative to upstream: `audit/protocol_changes.diff`.

## License conditions and publication changes

[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) permits modification
and redistribution subject to its conditions. The release preserves the license
text and original notices, identifies modifications and provenance, and adds a
separate NOTICE for attribution.

The input ZIP already contained LICENSE and UPSTREAM_NOTICE inside the component.
It would be incorrect to describe that archive as entirely unlicensed.
The following changes prepare it for public distribution:

1. LICENSE and NOTICE are also present at the repository root. Installed copies
   remain inside the component so that manual installation retains attribution.
2. The six modified upstream files carry explicit modification headers. Unchanged
   files remain byte-identical, and no original notice has been removed.
3. Suris additions and adaptations explicitly use Apache-2.0. The borrowed library
   is not presented as an exclusively original Suris implementation.
4. Credits thank rabits, GnoX, and all EcoFlow BLE contributors without claiming
   that they support or endorse Suris modifications.
5. Third-party dependencies and trademarks are documented.
6. Unofficial and unstable status, testing limits, lack of warranties, and the
   liability disclaimer with mandatory legal exceptions are stated.
7. Caution notices appear before installation, before commands, in release notes,
   and in the English and Ukrainian HA setup forms. Documentation is in English.
8. The version is 0.8.0b4. Metadata links to the separate Suris repository rather
   than presenting the upstream wiki as documentation for this independent release.

After these changes, this review found no omitted source-redistribution obligations
explicitly listed in Section 4 of Apache-2.0 for the reviewed materials. This is
a finding about those materials, not an unconditional legal guarantee.

## Matters not resolved by documentation changes

**EcoFlow and other third-party rights.** The ha-ef-ble authors' open-source license
does not by itself establish ownership of every underlying protocol datum, absence
of patents, or permission for every use of EcoFlow services. `keydata.py` and the
inherited authentication code match upstream, but the independent origin and rights
history of the table were not established. The inherited cloud request retains
`bundleId: com.ef.EcoFlow`; that does not establish official client status or
EcoFlow authorization to use the API.

**Trademarks.** EcoFlow and DELTA names identify compatibility. Apache-2.0 does not
grant trademark rights. The [EcoFlow website terms](https://account.ecoflow.com/agreement/en-us/TermsOfUse.html)
assert rights in names and logos. These website terms are not presented as a
universal agreement for every device, region, or BLE session; the user's exact
applicable agreements were not available to the reviewer.

**Artwork.** Four PNGs with turquoise SEF branding and the Suris name were retained
from the supplied archive. They contain no personal photograph or claim of official
EcoFlow branding. Documentation establishing original artwork and font authorship
was not supplied. Appearance and the absence of a font file do not establish all
rights in the raster images. This review does not claim to establish exclusive
rights to those PNGs.

**Liability disclaimer.** It cannot guarantee immunity in every jurisdiction and
situation. The text therefore retains the maximum-extent-permitted-by-law limit
and preserves liability and rights that cannot lawfully be excluded. It adds no
restrictions to the rights granted by Apache-2.0.

The review found no concrete basis to remove the public library, alter its
authentication, or declare all materials infringing. Remaining third-party rights
questions are disclosed rather than treated as resolved by a disclaimer.

## Personal data and use by other owners

**No restriction to the author's account or individual station was found in the code.**

- No personal password, User ID, MAC address, or station serial number belonging
  to the author was found.
- The publication package contains no HA configuration files, `.storage`,
  `secrets.yaml`, `.env`, private keys, or GitHub tokens.
- Test emails, passwords, and Bluetooth addresses are synthetic, including the
  `example.test` domain. The tests do not contact a real account.
- The Bluetooth manufacturer number and serial-number prefixes identify the model;
  they are not personal restrictions on users.
- Each user selects their own DELTA 2 Max and supplies their own credentials.
  Email/password are used for HTTPS sign-in but are not retained in the configuration
  entry. User ID, serial number, and address are stored in that user's HA instance.
- `keydata.py` contains the same shared protocol table as public upstream,
  rather than secrets extracted from the author's station.

Support is limited to **DELTA 2 Max + Extra Battery 1**. Other models and slot 2
are unsupported by this build. Car Input 2 remains experimental.

## Behavior and testing

Application Python syntax trees were compared with input 0.8.0b3; only the VERSION
constant changes executable code. License comments do not affect execution.
Artwork hashes, configuration-field structure, translation placeholders, platform,
domain, and dependencies were checked separately. English and Ukrainian setup
translations remain; the Russian translation was removed at the owner's request.
Results: `audit/release_checks.json`; test log: `audit/tests_0.8.0b4.txt`.

Automated publication checks used mocked BLE and cloud calls rather than a real
station or live EcoFlow login. Separately, **the author reports testing the
integration on a real EcoFlow DELTA 2 Max station**. That report does not establish
coverage of every feature, firmware, or configuration. The code defines up to
66 sensors, which does not mean all are enabled in an existing installation.
Successful offline tests do not change the **unstable beta** status.
