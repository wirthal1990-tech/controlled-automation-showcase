# Sicherheits- und Lizenzprüfung des lokalen Kandidaten

Prüfumfang: exakt die folgenden 13 Dateien dieses Demo-Pakets; im getrennten Profilvorschlag zusätzlich eine `README.md`, zusammen 14 vorgeschlagene Public-Dateien. Die interne Prüfakte bleibt außerhalb dieser vorgeschlagenen Repo-Inhalte.

- `README.md`
- `LICENSE`
- `agent-approval-demo/README.md`
- `agent-approval-demo/demo.py`
- `agent-approval-demo/fixtures.json`
- `agent-approval-demo/test_demo.py`
- `revops-evidence-demo/README.md`
- `revops-evidence-demo/demo.py`
- `revops-evidence-demo/fixtures.json`
- `revops-evidence-demo/test_demo.py`
- `docs/REPRODUCTION.md`
- `docs/SECURITY_LICENSE_REVIEW.md`
- `docs/SOURCES_AND_LIMITS.md`

Code, Fixtures und Dokumentation wurden neu mit KI-Unterstützung erstellt. Die neue `LICENSE` übernimmt die offizielle MIT-Vorlage mit ausschließlich ersetztem Jahr und Rechteinhabernamen. Enthaltene Daten und IDs sind künstliche Platzhalter. Kein privater Quelltext, Kundenmaterial, echte Kontakte, Hosts, IPs, Credentials, Bilder, Logos oder Git-Historie gehören zum Paket. Es werden keine Drittanbieterpakete mitgeliefert. Python ist eine nicht mitgelieferte Laufzeitvoraussetzung.

Die lokale Prüfroutine umfasst die vollständige Dateiliste einschließlich versteckter Einträge, Typ-/Linkkontrolle und SHA-256-Fingerabdrücke. Der frühere vollständige Inhaltsscan und die Selbstprüfung bleiben historische Belege. Im lokalen Lizenz-Folgeabschnitt werden die neue Lizenz und die betroffenen Texte geprüft und der geänderte Demo-Baum erneut mit Gitleaks gescannt; der unveränderte Profiltext erhält keinen unnötigen zweiten Scan. Kein Scanner kann alle vertraulichen oder rechtlich geschützten Inhalte erkennen; ein unauffälliger Scan ist keine umfassende Sicherheitsfreigabe. Die Selbstprüfung durch denselben erstellenden Agenten ersetzt keine unabhängige menschliche Rechteprüfung.

Nur die Testdateien starten Unterprozesse, und ausschließlich die mitgelieferten Python-Demos mit festen Szenarien. Die Demo-Implementierungen lesen ihre lokale synthetische Fixture. Simulierte Aktionen schreiben ausschließlich in Python-Objekte. Es gibt keine Netzwerk-, Shell- oder externen Schreibfunktionen in den Implementierungen.

Lizenzstatus aller oben genannten Demo-Dateien: **MIT gemäß Operatorentscheidung; keine Publikationsfreigabe**. Die vollständige Root-`LICENSE` wird wortgenau gegen die offizielle Vorlage geprüft, nur Jahr und Name ersetzt. Die Operatorerklärung bestätigt nach seinem Kenntnisstand keine bekannten entgegenstehenden Drittrechte; sie ist keine juristisch geprüfte Urheberrechtsfreiheit. Die MIT-Lizenz gilt ausschließlich für die neu erstellten Inhalte dieses Demo-Repositories, nicht für private Vorlagen, den getrennten Profiltext oder externe Quellen. Für den Profiltext wurde keine separate Open-Source-Lizenz gewählt. Die bestehende Dataset-Lizenz wird nicht auf diesen Code übertragen.

Bekannte technische Grenzen: geskriptete statt authentifizierter Freigabe, frei zugänglicher Prozessspeicher, keine dauerhafte Wiederholungssperre, sichere Uhr oder Nebenläufigkeitskontrolle. Geprüfte synthetische Fälle sind kein Beweis einer produktiven Integration oder allgemeiner Angriffssicherheit.
