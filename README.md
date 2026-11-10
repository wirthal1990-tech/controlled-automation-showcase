# Controlled Automation Showcase

Zwei kleine Python-Beispiele zeigen, wie ich Freigaben und Belege vor einer technischen Aktion prüfbar mache. **Beide Demos sind veröffentlicht, vollständig synthetisch und lokal ausführbar.** Sie greifen nicht auf private Projekte, Netzwerke oder echte Geschäftsdaten zu.

## Die beiden Beispiele

**[Control before action](agent-approval-demo/README.md)** – Eine simulierte Freigabe gilt nur für den gebundenen Inhalt. Manipulation, Ablauf und Wiederholung führen zur Verweigerung. Die Aktion verändert ausschließlich ein Python-Objekt im Arbeitsspeicher.

**[Evidence before go](revops-evidence-demo/README.md)** – Fehlende oder widersprüchliche Belege führen zu `NO_GO`. Vollständige Belege ermöglichen eine anschließende Prüfung, aber noch keine Freigabe. Eine zusätzliche, an dieselben Daten gebundene simulierte Zustimmung ist nötig.

## Lokal ausprobieren

Benötigt wird Python ab Version 3.11; zusätzliche Pakete werden nicht installiert.

- **Frühere Prüfung (historisch dokumentiert):** Tests erfolgreich mit Python 3.14.8; die 16 Agent- und 17 Evidence-Tests unabhängig reproduziert mit Python 3.13.5.
- **Erneute Prüfung am 10.11.2026:** dieselben 16 + 17 Tests erfolgreich mit Python 3.14.10 auf dem aktuellen Code.

Daraus folgt keine bestätigte Kompatibilität für andere Versionen.

```sh
python3 -B -m unittest discover -s agent-approval-demo -p 'test_*.py' -v
python3 -B -m unittest discover -s revops-evidence-demo -p 'test_*.py' -v
python3 -B agent-approval-demo/demo.py approved
python3 -B revops-evidence-demo/demo.py review
```

Die Befehle im Root dieses Repositories ausführen. **33 Testmethoden** prüfen unter anderem erlaubte und verweigerte Aktionen. Negative CLI-Szenarien geben absichtlich einen anderen Exit-Code zurück – siehe [Reproduktion](docs/REPRODUCTION.md).

## Was die Demos belegen – und was nicht

Die Beispiele machen Eingabevalidierung, Inhaltsbindung, Ablehnung unsicherer Zustände und nachvollziehbare Testfälle sichtbar. Sie sind **keine produktive Agent-Integration**. Die Freigaben stammen aus synthetischen Testdaten; es gibt weder Identitätsprüfung noch Signaturen, dauerhafte Wiederholungssperre, Transaktionssicherheit oder produktive Sicherheitsgarantie. Ein neuer Prozess beginnt mit leerem Speicher.

Der Code und die Texte wurden neu mit KI-Unterstützung erstellt. Die Beispiele demonstrieren technische Prüflogik und QA – nicht die tatsächliche Laufzeit oder eine kommerzielle Leistung privater AgentOS-/RevOps-Systeme.

[**Technische Herkunft und Grenzen**](docs/SOURCES_AND_LIMITS.md) · [**Sicherheits- und Lizenzprüfung**](docs/SECURITY_LICENSE_REVIEW.md) · [**Tests und Exit-Codes**](docs/REPRODUCTION.md)

## Lizenz

Die neu erstellten Inhalte dieses Repositories stehen unter der [MIT-Lizenz](LICENSE), Copyright (c) 2026 Alexander Wirth. Die verlinkten externen Datenquellen und die privaten Original-Repositories sind davon nicht umfasst.
