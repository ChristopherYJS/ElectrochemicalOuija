import sys, pkgutil, inspect, re
hits = []
for m in pkgutil.iter_modules():
    if m.name in ("PySide6", "pyside6uic"):
        mod = __import__(m.name)
        base = mod.__path__[0]
        # brute-force scan
        import os
        for root, _, files in os.walk(base):
            for f in files:
                if f.endswith(".py"):
                    p = os.path.join(root, f)
                    try:
                        with open(p, "r", encoding="utf-8", errors="ignore") as fh:
                            txt = fh.read()
                        if re.search(r'ui_.*\.py', txt):
                            hits.append(p)
                    except Exception:
                        pass
print("\n".join(sorted(set(hits))))
