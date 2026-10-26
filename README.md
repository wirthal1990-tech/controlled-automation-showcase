# Controlled automation showcase

Zwei kleine, eigenständig neu erstellte Offline-Demos: **Control before action** und **Evidence before go**. Sämtliche Eingaben sind synthetisch. Die Demo-Implementierungen enthalten keine Netzwerkaufrufe, Provider oder Hooks für Betriebssystem-Befehle. Keine echten Geschäftsdaten. Simulierte Aktionen verändern nur Python-Objekte im Arbeitsspeicher. Die Tests starten ausschließlich die mitgelieferten Python-Demos als Unterprozesse.

Dieses Paket ist ein lokaler Veröffentlichungsvorschlag (`PROPOSED`). Die Code-Erstellung war KI-gestützt. Es ist keine ursprüngliche Implementierung eines privaten Systems und bietet keine Schema-Kompatibilität zu anderen Projekten.

## Start in drei Schritten

1. Python 3.11 oder neuer bereitstellen; keine Pakete installieren. Lokal verifiziert wurde Python 3.14.8. Zusätzlich dokumentiert der Operator eine frühere unabhängige Reproduktion unter Python 3.13.5; diese wurde hier nicht neu ausgeführt. Weitere Versionen sind `NOT_TESTED`.
2. Im Hauptverzeichnis dieses Pakets beide Testsuiten ausführen:

```sh
python3 -B -m unittest discover -s agent-approval-demo -p 'test_*.py' -v
python3 -B -m unittest discover -s revops-evidence-demo -p 'test_*.py' -v
```

3. Die [Agent-Demo](agent-approval-demo/README.md) und [Evidence-Demo](revops-evidence-demo/README.md) einzeln ausprobieren:

```sh
python3 -B agent-approval-demo/demo.py approved
python3 -B revops-evidence-demo/demo.py review
```

Die Tests laufen in getrennten Prozessen, weil beide Teilverzeichnisse ein eigenes `demo.py` enthalten. Die Suiten testen auch die Kommandozeilenprogramme mit tatsächlichen Unterprozessen.

## Welche Grenze demonstriert wird

- Agent-Demo: Der SHA-256-Hash bindet den Inhalt einer Anfrage an eine ausdrückliche Entscheidung. Ohne passende, gültige und unverbrauchte Freigabe keine simulierte Aktion.
- Evidence-Demo: Fehlende, negative oder widersprüchliche Belege bedeuten `NO_GO`. Ein technischer Demo-Score hebt das niemals auf. Vollständige Belege erlauben nur menschliche Prüfung; eine separate Freigabe bindet sich an exakt dieselben Eingaben.

Freigaben in Fixtures sind **geskriptete Beispieldaten**. Niemand wird dadurch authentifiziert. Ein Hash beweist gleiche Inhalte, keine menschliche Identität oder Berechtigung. Keine signierten Entscheidungen, dauerhafte Wiederholungssperre, Nebenläufigkeit, echte Integration oder produktive Sicherheitsgarantie. Ein Neustart erzeugt einen neuen, leeren Simulator.

[Reproduktion und Exit-Codes](docs/REPRODUCTION.md) · [Herkunft und Grenzen](docs/SOURCES_AND_LIMITS.md) · [Sicherheits- und Lizenzprüfung](docs/SECURITY_LICENSE_REVIEW.md)

## Lizenz und Rechtegrenze

Die neu erstellten Inhalte dieses Demo-Repositories stehen gemäß der dokumentierten Operatorentscheidung unter der [MIT-Lizenz](LICENSE), Copyright (c) 2026 Alexander Wirth. Der Operator bestätigt nach seinem Kenntnisstand, dass ihm keine entgegenstehenden Rechte Dritter bekannt sind. Diese Erklärung ist keine juristisch geprüfte Urheberrechtsfreiheit und keine Veröffentlichungsfreigabe. Die MIT-Lizenz erfasst ausschließlich die neu erstellten Showcase-Inhalte dieses Demo-Repositories, keine privaten Vorlagen oder externen verlinkten Quellen. Für den getrennten Profiltext wurde keine separate Open-Source-Lizenz gewählt. Der Kandidat bleibt lokal; Veröffentlichung erfordert eine eigene Freigabe.
