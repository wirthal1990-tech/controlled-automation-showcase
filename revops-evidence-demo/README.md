# Evidence before go

Ein rein technisches Beispiel mit fiktiven Platzhaltern `EXAMPLE_ORG_A` bis `EXAMPLE_ORG_Z`. Die Bezeichnung RevOps dient nur der Einordnung einer Belegprüfung vor einer Entscheidung. Keine reale Vertriebsqualifizierung, private Scoring-Formel, Firma oder Kontaktaufnahme.

## Eingaben, Bewertung und Freigabe

`fixtures.json` trennt vollständige, fehlende und widersprüchliche Eingaben. Ein Objekt hat exakt `object` und `evidence`. Jeder Beleg hat exakt `id`, `criterion`, `observed`; IDs `EVIDENCE_A` bis `EVIDENCE_Z` sind nicht leer und eindeutig. 1–16 Belege sind erlaubt, `observed` ist ein echter Boolean. Unbekannte Felder/Kriterien und falsche Typen werden verweigert.

Die zwei Pflichtkriterien `format_checked` und `review_note_present` sind willkürlich gewählte technische Demonstrationsmerkmale. Je 50 Punkte für mindestens einen positiven Beleg, Gesamtwert 0–100. Die Gewichtung ist nur eine transparente Demo-Rubrik, kein Wert für Umsatz, Kaufbereitschaft oder Kundenqualität. Deshalb kann selbst Score 100 bei widersprüchlichen Belegen `NO_GO` bedeuten.

`assess(record)` ergibt genau `NO_GO` oder `REVIEW_REQUIRED`. Ungültiges Schema ergibt `NO_GO`, Score 0 und `INVALID_RECORD` ohne Evidence-IDs (explizit evidence-freier Validierungsfehler). Bei gültigem Schema bedeuten fehlendes Pflichtkriterium, widersprüchliche Wahrheitswerte oder mindestens ein negativer Beleg immer `NO_GO`. Gründe werden in der Reihenfolge `MISSING_EVIDENCE`, `CONTRADICTORY_EVIDENCE`, `NEGATIVE_EVIDENCE` gesammelt. Sonst `REVIEW_REQUIRED`, Score 100, leere Gründe und mindestens zwei auf die eingebetteten positiven Belege auflösbare IDs. Die Bewertung ist keine Wahrheitsermittlung außerhalb der synthetischen Eingabe.

`Simulator.release(record, approval)` bewertet erneut und ergibt genau `NOT_RELEASED` oder `RELEASED_SIMULATED`. Erst `REVIEW_REQUIRED`, dann eine separate Freigabe mit exakt `decision="APPROVED"` und `record_sha256`, dann Wiederholungskontrolle. Gründe bei Verweigerung: zuerst `EVIDENCE_BLOCKED`, dann `APPROVAL_REQUIRED`, dann `REPLAY`. Eine erfolgreiche Freigabe trägt nur den Objekt-Platzhalter in die Python-Liste `releases` ein. Es gibt keinen Datei- oder externen Schreibpfad.

Der Hash umfasst die vollständige Eingabe, nicht nur den Score: `json.dumps(record, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")`, dann SHA-256. Array-Reihenfolge bleibt relevant. Ein neuer Objektname oder eine geänderte Beleg-ID benötigt eine neue Freigabe. Kein JCS-/Originalschema-Kompatibilitätsclaim.

## Ausführen

Vom Paket-Hauptverzeichnis:

```sh
python3 -B revops-evidence-demo/demo.py review
python3 -B revops-evidence-demo/demo.py contradiction
python3 -B revops-evidence-demo/demo.py unapproved
python3 -B revops-evidence-demo/demo.py approved
python3 -B -m unittest discover -s revops-evidence-demo -p 'test_*.py' -v
```

Szenarien: `review`, `missing`, `contradiction`, `unapproved`, `approved`, `tampered`. Exit `0`: `REVIEW_REQUIRED` oder `RELEASED_SIMULATED`. Exit `3`: `NO_GO` oder `NOT_RELEASED`. Exit `2`: falscher Kommandozeilenaufruf. Alle regulären Ergebnisse sind JSON; die Testsuite liefert Exit `0`, wenn auch sämtliche Negativfälle korrekt verweigert werden.

## Grenzen

Die `approved`-Variante setzt eine ausdrückliche Freigabe als geskriptete Eingabe; sie ermittelt keine menschliche Identität. Hashes sind keine Signaturen. Kein dauerhaftes Audit, sicherer Approval-Kanal, Schutz vor Speicheränderungen oder Wiederanlauf-/Nebenläufigkeitsgarantie. Wiederholungsschutz gilt nur innerhalb desselben Simulator-Objekts. Keine produktive Vertriebspipeline oder tatsächliche Wirkung belegt.
