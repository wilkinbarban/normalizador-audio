import csv
import os
from datetime import datetime


def summarize(before_after_data: dict) -> dict:
    total = len(before_after_data)
    ok = sum(1 for item in before_after_data.values() if item.get("status") == "✅ Éxito")
    fail = total - ok
    before = [
        float(item["before"]["input_i"])
        for item in before_after_data.values()
        if "before" in item and item.get("status") == "✅ Éxito"
    ]
    after = [
        float(item["after"].get("input_i", 0))
        for item in before_after_data.values()
        if "after" in item and item.get("status") == "✅ Éxito"
    ]
    avg_before = sum(before) / len(before) if before else 0
    avg_after = sum(after) / len(after) if after else 0
    return {
        "total": total,
        "ok": ok,
        "fail": fail,
        "ratio": (ok / total * 100) if total else 0,
        "avg_before": avg_before,
        "avg_after": avg_after,
        "delta": avg_after - avg_before,
    }


def export_csv(path: str, before_after_data: dict):
    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "Video",
            "Antes_I",
            "Antes_LRA",
            "Antes_TP",
            "Después_I",
            "Después_LRA",
            "Después_TP",
            "Estado",
        ])
        for key, data in before_after_data.items():
            display_name = data.get("name", os.path.basename(key))
            if "before" in data and "after" in data:
                before = data["before"]
                after = data["after"]
                writer.writerow([
                    display_name,
                    f"{float(before['input_i']):.2f}",
                    f"{float(before['input_lra']):.2f}",
                    f"{float(before['input_tp']):.2f}",
                    f"{float(after.get('input_i', 0)):.2f}",
                    f"{float(after.get('input_lra', 0)):.2f}",
                    f"{float(after.get('input_tp', 0)):.2f}",
                    data.get("status", "N/A"),
                ])
            else:
                writer.writerow([display_name, "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", data.get("status", "N/A")])


def export_txt(path: str, before_after_data: dict):
    summary = summarize(before_after_data)
    with open(path, "w", encoding="utf-8") as file:
        file.write("═" * 80 + "\n")
        file.write("REPORTE DE NORMALIZACIÓN\n")
        file.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        file.write("═" * 80 + "\n\n")
        file.write(
            f"Total: {summary['total']}  Exitosos: {summary['ok']}  Fallidos: {summary['fail']}\n\n"
        )
        for key, data in before_after_data.items():
            display_name = data.get("name", os.path.basename(key))
            file.write(f"📹 {display_name}\nEstado: {data.get('status', 'N/A')}\n")
            if "before" in data:
                b = data["before"]
                file.write(
                    f"  ANTES:   I={float(b['input_i']):.2f} LUFS  "
                    f"LRA={float(b['input_lra']):.2f} LU  "
                    f"TP={float(b['input_tp']):.2f} dB\n"
                )
            if "after" in data and data["after"]:
                a = data["after"]
                file.write(
                    f"  DESPUÉS: I={float(a.get('input_i', 0)):.2f} LUFS  "
                    f"LRA={float(a.get('input_lra', 0)):.2f} LU  "
                    f"TP={float(a.get('input_tp', 0)):.2f} dB\n"
                )
            file.write("\n")
