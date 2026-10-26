# Control before action

Eine vollständig synthetische Anfrage `write_report` schreibt nach einer passenden Freigabe nur einen Text in `Simulator.reports`, ein Python-Wörterbuch. Es entstehen keine Dateien und keine externe Aktion.

## Eingaben und Bindung

`fixtures.json` enthält Anfrage, ausdrückliche Beispielsentscheidung und eine feste Testzeit. Anfragefelder exakt: `action`, `report`, `text`. Nur `write_report`, `SYNTHETIC_REPORT_A` bis `SYNTHETIC_REPORT_Z` und 1–80 ASCII-Zeichen aus Buchstaben, Zahlen, Leerzeichen, Unterstrich, Punkt und Bindestrich sind erlaubt.

Kanonische Serialisierung bedeutet hier exakt `json.dumps(request, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")`. Nur dieses eingeschränkte flache Schema wird gehasht; dies ist kein allgemeines JCS-Verfahren. Der SHA-256-Hash dient als Inhaltsfingerabdruck.

Freigabefelder exakt: `approval_id` (`APPROVAL_A` bis `APPROVAL_Z`), `request_sha256` (64 kleine Hex-Zeichen), `decision` (`APPROVED` oder `DENIED`), `expires_at` (nichtnegative ganze Testzeit). `now` muss ebenfalls eine nichtnegative ganze Zahl sein; Boolean ist ausgeschlossen. Bei `now >= expires_at` ist die Freigabe abgelaufen.

## Ausführen

Vom Paket-Hauptverzeichnis:

```sh
python3 -B agent-approval-demo/demo.py approved
python3 -B agent-approval-demo/demo.py tampered
python3 -B agent-approval-demo/demo.py replay
python3 -B -m unittest discover -s agent-approval-demo -p 'test_*.py' -v
```

Szenarien: `approved`, `missing`, `denied`, `tampered`, `expired`, `replay`. Exit `0`: `EXECUTED`. Exit `3`: erwartete Verweigerung `REFUSED`. Exit `2`: falscher Kommandozeilenaufruf. Tests insgesamt Exit `0`, wenn auch die negativen Fälle korrekt verweigert wurden.

`REFUSED` liefert genau einen Grund aus `INVALID_REQUEST`, `INVALID_CLOCK`, `INVALID_APPROVAL`, `DENIED`, `HASH_MISMATCH`, `EXPIRED`, `REPLAY`; geprüft in dieser Reihenfolge. Eine fehlende Freigabe erfüllt das Freigabeschema nicht und fällt daher unter `INVALID_APPROVAL`. `EXECUTED` enthält den gebundenen Hash. Alle Ergebnisse sind parsebares JSON. Tests prüfen außerdem fehlende/zusätzliche Felder, falsche Datentypen und unveränderten virtuellen Speicher bei Verweigerung.

## Grenzen

Ein Simulator verbraucht jede Freigabe-ID und jeden Anfrage-Hash höchstens einmal. Im `replay`-Szenario wurde die erste Aktion bereits simuliert; der zweite Versuch wird verweigert, ein Bericht bleibt bestehen. Eine gescheiterte Prüfung verbraucht keine Freigabe.

Die Wiederholungssperre gilt nur für dasselbe Simulator-Objekt in einem einzelnen Prozess. Öffentliche Python-Objekte sind kein manipulationsgeschützter Speicher. Keine sichere Uhr, Signatur, Identitätsprüfung, dauerhafte Transaktion oder Nebenläufigkeitskontrolle. Fixtures simulieren eine vertrauenswürdig übergebene Entscheidung; ein Angreifer könnte sie selbst neu schreiben. Der Hash allein verhindert dies nicht. Keine Produktionsintegration oder Sicherheitsgarantie.
