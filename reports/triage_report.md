# Security Alert Triage Report: ALERT-001

## 1. Executive Summary
On November 12, 2026 (`03:14:22Z`), host `SRV-RDP-01` (`10.0.1.20`) experienced a rapid RDP brute-force attack consisting of 47 failed logon attempts (Event ID 4625, Logon Type 10) within 5 minutes targeting the privileged `administrator` account. 

Based on Threat Intelligence enrichment, the source IP (`83.172.35.6`, geolocated in Russia) is **malicious**, carrying an abuse confidence score of **100%** with **1,045 reports** from **404 distinct users** (and is not whitelisted).

---

## 2. MITRE ATT&CK Mapping
* **Tactic:** Credential Access (`TA0006`)
* **Technique:** Brute Force: Password Guessing (`T1110.001`) — *Parent Technique: Brute Force (`T1110`)*

*(Note: Attackers are leveraging exposed External Remote Services (`T1133`) as the vector for this brute-force activity.)*

---

## 3. Assessed Severity
* **Assessed Severity:** **High** *(Escalated from original severity: Medium)*
* **Justification:** Although all 47 observed logon attempts failed (`Status: 0xC000006D`), escalating the severity from Medium to High is warranted due to three compounding risk factors:
  1. The source IP is a confirmed, high-confidence malicious actor actively conducting widespread attacks.
  2. The attack specifically targets the high-privilege `administrator` account.
  3. The presence of Logon Type 10 from an external IP indicates that RDP on a server (`SRV-RDP-01`) is directly exposed to the public internet, presenting a significant attack surface risk.

---

## 4. Recommended Next Steps (Tier 2)
1. **Check for Successful Compromise:** Search Windows Security Logs on `SRV-RDP-01` (and across the environment) for Event ID `4624` (Successful Logon) associated with `83.172.35.6` or the `administrator` account around and after `2026-11-12T03:14:22Z` to confirm no subsequent attempts succeeded.
2. **Containment & Exposure Remediation:** Block `83.172.35.6` at the perimeter firewall/IPS immediately. Investigate why RDP (TCP/3389) on `SRV-RDP-01` is reachable from the public internet and restrict access behind a VPN, jump host, or strict IP allowlist.
3. **Scope & Hardening Review:** Pivot on `83.172.35.6` in firewall and SIEM logs to determine if other internal assets were targeted. Verify that account lockout policies, MFA for remote access, and best practices regarding the built-in `administrator` account (e.g., disabling or renaming) are enforced on `SRV-RDP-01`.

---

# SOC Triage Report: ALERT-002

## 1. Executive Summary
At `2026-11-12T03:21:05Z`, a successful interactive Remote Desktop Protocol (RDP, Logon Type 10) logon (`Event ID 4624`) occurred for the privileged `administrator` account on host `SRV-RDP-01` (`10.0.1.20`) from external IP `83.172.35.6`. This successful authentication followed 47 failed logon attempts from the same IP minutes earlier (referenced in `ALERT-001`).

Based on Threat Intelligence enrichment, the source IP `83.172.35.6` is **malicious**. It is not whitelisted, originates from Russia (`RU`, ISP: *The municipal enterprise Severskelektrosviaz*), and holds an **Abuse Confidence Score of 100** with **1,045 abuse reports** from **404 distinct users**.

## 2. MITRE ATT&CK Mapping
* **Primary Tactic:** Credential Access (`TA0006`)
  * **Technique:** `T1110` – Brute Force (specifically `T1110.001` – Password Guessing), evidenced by 47 failed attempts followed by a successful logon.
* **Secondary Tactic:** Initial Access (`TA0001`)
  * **Technique:** `T1133` – External Remote Services / `T1078` – Valid Accounts, evidenced by the external RDP logon using the `administrator` account.

## 3. Assessed Severity
* **Assessed Severity:** **Critical** *(upgraded from Original Severity: **High**)*
* **Justification:** While the original rule rated this as *High*, Threat Intelligence confirms the source IP is actively malicious (`abuseConfidenceScore: 100`), and the attack progressed beyond brute-force attempts to a **confirmed successful logon into a privileged `administrator` account** on a server (`SRV-RDP-01`). This indicates an active unauthorized intrusion requiring immediate containment.

## 4. Recommended Next Steps
1. **Immediate Containment:** Isolate `SRV-RDP-01` (`10.0.1.20`) via EDR or network segmentation, terminate active RDP sessions for `administrator`, block `83.172.35.6` at the perimeter firewall, and rotate/disable the `administrator` credentials.
2. **Investigate Post-Authentication Activity:** Review EDR telemetry, Windows Security/System logs, PowerShell logs, and process creation events on `SRV-RDP-01` from `2026-11-12T03:21:05Z` onward for signs of lateral movement, payload execution, or persistence (e.g., new accounts, scheduled tasks, or services).
3. **Scope Exposure & Harden Access:** Pivot across firewall and authentication logs (including `ALERT-001`) to determine if `83.172.35.6` targeted or accessed other internal hosts, and verify why RDP on `SRV-RDP-01` is externally reachable without MFA or IP allowlisting.

---

# SOC Tier 1 Triage Report: ALERT-003

## 1. Executive Summary
On `2026-11-12T09:42:51Z`, Suricata IDS detected potential Command-and-Control (C2) beaconing from finance workstation `WS-FINANCE-07` (`10.0.2.57`, user `m.ionescu`) to external IP `50.16.16.211` over TCP port `8080`. The host is sending periodic 312-byte HTTP `POST` requests to `/gate.php` every 60 seconds.

Based on Threat Intelligence enrichment, `50.16.16.211` is an AWS EC2 instance (`ec2-50-16-16-211.compute-1.amazonaws.com`) with an `abuseConfidenceScore` of **20%** across 86 reports from 5 distinct users (most recently reported on `2026-11-12`). While a 20% score alone is inconclusive and not definitively malicious on its own, cloud-hosted infrastructure is frequently abused for ephemeral C2 servers. Combined with the `/gate.php` URI, non-standard port `8080`, and regular 60-second beaconing pattern, the activity is **suspicious and potentially malicious**, warranting immediate Tier 2 investigation.

## 2. MITRE ATT&CK Mapping
* **Tactic:** Command and Control (`TA0011`)
* **Technique:** `T1071.001` – Application Layer Protocol: Web Protocols (periodic HTTP `POST` beaconing to `/gate.php` over port `8080`)

## 3. Assessed Severity
* **Assessed Severity:** **High** (unchanged from the original alert severity of `high`)
* **Justification:** Although the Threat Intelligence confidence score is relatively low (20%)—meaning the IP cannot be confirmed malicious from TI alone—the behavioral indicators strongly match active malware C2 communication (60-second HTTP `POST` intervals to `/gate.php` on port `8080`). Additionally, the affected asset (`WS-FINANCE-07`) belongs to a finance department user (`m.ionescu`), elevating the potential business and data-exfiltration risk. The severity should remain **High** until the originating process on the endpoint is verified.

## 4. Recommended Next Steps
1. **Endpoint Process Triage:** Check EDR or host telemetry on `WS-FINANCE-07` (`10.0.2.57`) around `09:42:51Z` to identify the exact binary/process establishing outbound connections to `50.16.16.211:8080`, and verify its file hash, signature, and parent process.
2. **Network & Scope Analysis:** Review firewall, proxy, and full HTTP logs (including `User-Agent` and `POST` body/headers) for `WS-FINANCE-07` to determine when the beaconing began and search for any other internal hosts communicating with `50.16.16.211`.
3. **Containment (If Unauthorized):** If the communicating process is not a verified legitimate application, isolate `WS-FINANCE-07` via EDR, block `50.16.16.211` at the perimeter firewall/proxy, and revoke active sessions / reset credentials for user `m.ionescu`.

---

# Tier 1 SOC Triage Report: ALERT-004

## 1. Executive Summary
On **2026-11-12 at 11:08:37 UTC**, user `a.popescu` on host `WS-HR-03` (`10.0.3.14`) opened an email attachment named `Invoice_November.zip` via Microsoft Outlook (`OUTLOOK.EXE`) and extracted an executable file named `invoice.com` into `C:\Users\a.popescu\Downloads\Invoice_November\`. Microsoft Defender for Endpoint flagged the extracted file via heuristics and automatically **quarantined** it.

Based on the Threat Intelligence enrichment data, the file hash (`275a021bbfb6489e54d471899f7db9d1663fc695ec2fe2a2c4538aabf651fd0f`) is confirmed **malicious**, with **65 engines flagging it as malicious** and 0 marking it harmless.

---

## 2. MITRE ATT&CK Mapping
* **Primary Tactic:** Initial Access (TA0001)
  * **Technique:** **T1566.001** – *Phishing: Spearphishing Attachment* (malicious archive `Invoice_November.zip` delivered via email and opened in Outlook).
* **Secondary Tactic (Contextual):** Execution (TA0002)
  * **Technique:** **T1204.002** – *User Execution: Malicious File* (user extracted an executable `.com` file disguised as an invoice).

---

## 3. Assessed Severity
* **Assessed Severity:** **High** *(Escalated from original severity: Medium)*
* **Justification:** While Microsoft Defender for Endpoint successfully quarantined `invoice.com`, Threat Intelligence confirms with high confidence (65 malicious detections) that the payload is malicious rather than a heuristic false positive. Furthermore, the user actively interacted with the phishing email and extracted an executable disguised as a business document (`.com` masquerading as an invoice), requiring immediate verification that no prior execution occurred and that other users did not receive the same campaign.

---

## 4. Recommended Next Steps (For Tier 2 Analyst)
1. **Verify Quarantine & Rule Out Execution:** Inspect EDR process creation, file modification, and network telemetry on `WS-HR-03` (`10.0.3.14`) around `2026-11-12T11:08:37Z` to confirm `invoice.com` was blocked prior to execution and check for any suspicious child processes or persistence artifacts.
2. **Scope & Purge Email Campaign:** Search email gateway / Microsoft 365 Defender logs for the message containing `Invoice_November.zip` and the hash `275a021bbfb6489e54d471899f7db9d1663fc695ec2fe2a2c4538aabf651fd0f`. Purge the email from all impacted mailboxes and block the sender address/domain.
3. **Host Scan & User Verification:** Run a full EDR/antivirus scan on `WS-HR-03` to ensure no other malicious files remain from the archive, and contact `a.popescu` to confirm whether any other attachments or links from the email were opened.

---

# SOC Triage Report: ALERT-005

## 1. Executive Summary
On **2026-11-12 at 14:30:12Z**, workstation **`WS-DEV-02`** (`10.0.4.22`), associated with user **`d.stan`**, initiated an outbound UDP connection on port 53 (74 bytes) to external IP **`8.8.8.8`**, which was permitted by firewall rule `OUTBOUND-DNS-MONITOR`. This triggered an alert because the host bypassed the internal corporate DNS resolver.

Based on Threat Intelligence enrichment, **`8.8.8.8` is benign**. It is a whitelisted IP belonging to **Google LLC** (`dns.google` / `google.com`) with an **abuse confidence score of 0**. While the destination is legitimate public DNS infrastructure (likely a local misconfiguration or developer tool behavior rather than malicious infrastructure), direct external DNS queries still warrant verification against corporate policy and potential DNS-based evasion.

## 2. MITRE ATT&CK Mapping
* **Tactic:** Command and Control (TA0011)
* **Technique:** Application Layer Protocol: DNS (T1071.004)
  *(Note: Rules monitoring unauthorized external DNS traffic primarily detect potential C2/tunneling over DNS or Defense Evasion via internal DNS logging bypass, though no malicious activity is confirmed here.)*

## 3. Assessed Severity
* **Assessed Severity:** **Low** *(Unchanged from Original Severity: `low`)*
* **Justification:** The destination (`8.8.8.8`) is a verified, whitelisted public DNS service (`dns.google`) with a 0% abuse confidence score, and the observed traffic is minimal (a single 74-byte UDP/53 packet). Given that the source host is a developer workstation (`WS-DEV-02`), this is most likely benign developer tool behavior, hardcoded DNS configuration, or application fallback rather than an active compromise.

## 4. Recommended Next Steps
1. **Identify the Initiating Process and Queried Domain:** Check EDR telemetry or host firewall logs on `WS-DEV-02` around `2026-11-12T14:30:12Z` to determine which application/process opened UDP port 53 to `8.8.8.8` (e.g., browser, Docker, WSL, or custom script) and inspect packet/proxy logs if available to verify the queried domain.
2. **Assess Traffic Volume and Frequency:** Query firewall logs for `10.0.4.22` (`WS-DEV-02`) over the past 7–30 days to confirm whether this was a one-off/low-volume event or part of recurring, high-frequency, or unusually large DNS queries indicative of DNS tunneling.
3. **Remediate Policy Violation (If Benign):** If confirmed to be a benign misconfiguration or local network override, coordinate with `d.stan` or IT Operations to ensure the workstation uses the internal corporate DNS resolver, and evaluate switching `OUTBOUND-DNS-MONITOR` from `allow` to `deny` if corporate policy prohibits external DNS.

---

