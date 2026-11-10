# Lokal reproduzieren

1. Dieses Repository klonen oder als Archiv herunterladen und in einem lokalen Verzeichnis öffnen. Python 3.11 oder neuer verwenden. Lokal tatsächlich geprüft: Python 3.14.8 und am 10.11.2026 erneut Python 3.14.10. Zusätzlich wurden die 16 Agent- und 17 Evidence-Tests unter Python 3.13.5 unabhängig reproduziert. Diese Angaben betreffen die geprüften Codefassungen; andere Versionen sind nicht bestätigt.
2. Im kopierten Hauptverzeichnis ausführen, ohne Paketinstallation:

```sh
python3 -B -m unittest discover -s agent-approval-demo -p 'test_*.py' -v
python3 -B -m unittest discover -s revops-evidence-demo -p 'test_*.py' -v
```

3. Beide Aufrufe müssen Exit `0` und `OK` liefern. Agent: 16 Testmethoden; Evidence: 17 Testmethoden. Unterfälle prüfen zusätzliche Eingaben; sie sind keine separat gezählten Testmethoden.
4. Die [Agent-Szenarien](../agent-approval-demo/README.md) und [Evidence-Szenarien](../revops-evidence-demo/README.md) ausführen. Erwartete Verweigerung liefert bewusst Exit `3`. Ein ungültiges Szenario liefert Exit `2` und eine Nutzungsfehlermeldung auf stderr. Nicht als unerwarteten Testfehler behandeln oder mit Fehlerunterdrückung verstecken.

Die Suiten führen jedes reguläre CLI-Szenario zweimal aus, vergleichen Ausgabe und Exit-Code und prüfen die virtuellen Nebenwirkungen. Negative Fälle prüfen, dass kein weiterer Speicherzustand entsteht. Die Zeit der Agent-Fixture ist fest vorgegeben, keine Systemuhr-Abhängigkeit.

`-B` verhindert Python-Bytecode-Dateien. Keine Tests erzeugen Geschäftsdateien oder Netzwerkverkehr. Test-Unterprozesse starten nur die hier enthaltenen Demo-Dateien mit derselben Python-Laufzeit. Jede Testsuite in eigenem Prozess starten; keine globale Testentdeckung mit kollidierenden Modulnamen.

Reproduktion ist lokale Codeprüfung, kein GitHub-Actions-Ergebnis, keine Produktionsabnahme und keine Garantie für andere Python-Versionen.
