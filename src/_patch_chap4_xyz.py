from pathlib import Path
import shutil

p = Path("osdagbridge/core/reports/chap4.py")
s = p.read_text(encoding="utf-8")
marker = "    _span_m"

if "    horizontal_rows = []" in s:
    print("XYZ builder already exists; no change")
elif marker not in s:
    print("INSERT POINT NOT FOUND; no change")
else:
    addition = r'''
    horizontal_rows = []
    for lc in all_lcs:
        support_data = rxn_summary.get(lc, {}) or {}
        for support_name, components in (support_data.get("supports_xyz_kN", {}) or {}).items():
            horizontal_rows.append(
                _tex(lc) + r" & " + _tex(support_name) + r" & " +
                _fmt(components.get("Rx")) + r" & " +
                _fmt(components.get("Ry")) + r" & " +
                _fmt(components.get("Rz")) + r" \\[6pt]"
            )
    horizontal_body = ("\n\\hline\n").join(horizontal_rows) if horizontal_rows else r"--- & --- & --- & --- & --- \\[6pt]"

'''
    shutil.copy2(p, str(p) + ".before_xyz_reactions")
    p.write_text(s.replace(marker, addition + marker, 1), encoding="utf-8")
    print("XYZ builder inserted; backup created")