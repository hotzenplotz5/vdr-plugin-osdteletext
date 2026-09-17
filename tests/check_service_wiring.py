#!/usr/bin/env python3
from pathlib import Path

root = Path(__file__).resolve().parent.parent
osdteletext = (root / "osdteletext.c").read_text(encoding="utf-8")
txtrecv = (root / "txtrecv.c").read_text(encoding="utf-8")
service = (root / "teletextservice.h").read_text(encoding="utf-8")

required_osd = (
    '#include "teletextservice.h"',
    'virtual bool Service(const char *Id, void *Data = NULL);',
    'return TeletextService::Handle(Id, Data);',
)
required_receiver = (
    '#include "teletextservice.h"',
    'TeletextService::Publish(',
    'TeletextService::SetLiveService(',
    'TeletextService::ClearLiveService();',
    'TeletextService::SetReceiverActive(',
)
forbidden_service = (
    'openForReading(',
    'getFilename(',
    '/var/cache/vdr/vtx',
)

for needle in required_osd:
    if needle not in osdteletext:
        raise SystemExit(f"missing osdteletext service wiring: {needle}")
for needle in required_receiver:
    if needle not in txtrecv:
        raise SystemExit(f"missing receiver service wiring: {needle}")
for needle in forbidden_service:
    if needle in service:
        raise SystemExit(f"service must not depend on disk cache path/read API: {needle}")

print("teletext service wiring: PASS")
