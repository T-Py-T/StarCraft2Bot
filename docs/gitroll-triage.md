# GitRoll triage

This change audits all 47 findings in the 12 open `gitroll:` issues against
the scanned revision (`4f700828276569040cbc8b01fd4954936e9f3cf2`). None were
stale, generated, vendored, upstream, or unsafe to change. All 47 are addressed.

| Issue | File | Findings | Disposition |
| --- | --- | ---: | --- |
| #4 | `src/incredibot-sct.py` | 25 | Fixed: blocking async file access moved to thread-backed atomic IPC; `on_step` was decomposed; bare exception, builtin shadows, redundant nesting/comment/pass, and unused locals were removed. |
| #5 | `run/linux/download_maps.py` | 1 | Fixed: wildcard import replaced with an explicit configuration import; project path resolution was corrected. |
| #6 | `run/macos/setup_maps.py` | 1 | Fixed: the constant f-string was removed. The script also stopped writing plain XML with a misleading `.SC2Map` extension because real maps are MPQ archives. |
| #7 | `run/windows/create_simple_map.py` | 1 | Fixed: wildcard import replaced with an explicit configuration import; path resolution was corrected and the invalid XML map placeholder was replaced with copying a genuine map archive. |
| #8 | `src/config.py` | 1 | Fixed: constant f-string replaced with a plain string. |
| #9 | `src/diagnose_sc2.py` | 5 | Fixed: repeated CrossOver paths centralized and made configurable, socket cleanup made deterministic, bare exception narrowed, and constant f-strings removed. |
| #10 | `src/load-train-mlpp.py` | 2 | Fixed: constant f-strings replaced with plain strings. |
| #11 | `src/sc2_crossover_launcher_v2.py` | 1 | Fixed: constant f-string replaced with a plain string. |
| #12 | `src/sc2_crossover_launcher_v3.py` | 2 | Fixed: socket exception narrowed and constant f-string replaced with a plain string. |
| #13 | `src/sc2_crossover_launcher.py` | 1 | Fixed: constant f-string replaced with a plain string. |
| #14 | `src/sc2env.py` | 5 | Fixed: `step` decomposed; builtin shadows and unused retry/exception locals removed. The trainer and bot now share one path, wait for the correct response state, back off between retries, normalize observations, and manage the child process lifecycle. |
| #15 | `src/trainppo.py` | 2 | Fixed: constant f-strings replaced with plain strings. |

The tracked pickle files and result log were runtime artifacts rather than
source inputs. They are removed in favor of ignored `src/.runtime/` state. The
replacement NumPy archive loader disables object payloads. Separate single-writer
request/response channels, episode/request correlation, and unique temporary
files prevent executable pickle deserialization, lost updates, stale responses,
and partial-read races.

## Verification scope

Focused tests cover safe state round-trips, rejection of object payloads, action
handshake ordering, retry failure behavior, observation shape, and child-process
reuse/cleanup. Static checks cover all active Python source and setup scripts.
Live StarCraft II launches remain platform-dependent and require a licensed SC2
installation and genuine map archive; they are not suitable for headless CI.
