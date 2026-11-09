"""
optimize_laptop_to_d.py — Optimizador de almacenamiento y recursos (C: -> D:)
1. Mueve instaladores (.exe/.msi) y archivos .zip pesados de C:\\Users\\ASUS\\Downloads a D:\\Respaldo_Pesados_C\\Descargas
2. Mueve bases de datos legacy inactivas (chroma_db, qdrant_export.parquet) a D:\\Respaldo_Pesados_C\\Backups_Legacy
3. Limpia caché de pip (AppData\\Local\\pip\\cache) y archivos temporales desbloqueados en %TEMP%
"""
import os
import shutil
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

DEST_ROOT = Path(r"D:\Respaldo_Pesados_C")
DEST_DOWNLOADS = DEST_ROOT / "Descargas_Instaladores_Zips"
DEST_LEGACY = DEST_ROOT / "Lifextreme_Legacy_DB_Backups"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DOWNLOADS_DIR = Path(r"C:\Users\ASUS\Downloads")


def get_free_gb(drive: str) -> float:
    try:
        usage = shutil.disk_usage(drive)
        return round(usage.free / (1024 ** 3), 2)
    except Exception:
        return 0.0


def move_safely(src: Path, dst_dir: Path) -> int:
    if not src.exists():
        return 0
    dst_dir.mkdir(parents=True, exist_ok=True)
    size = 0
    if src.is_file():
        size = src.stat().st_size
    else:
        size = sum(f.stat().st_size for f in src.rglob("*") if f.is_file())

    target = dst_dir / src.name
    if target.exists():
        if src.is_file():
            src.unlink(missing_ok=True)
            return size
        return 0

    try:
        shutil.move(str(src), str(target))
        print(f"  [MOVIDO -> D:] {src.name} ({size / (1024**2):.1f} MB)")
        return size
    except Exception as e:
        print(f"  [-] No se pudo mover {src.name}: {e}")
        return 0


def clean_directory_contents(folder: Path, label: str) -> int:
    if not folder.exists():
        return 0
    freed = 0
    for item in folder.iterdir():
        try:
            if item.is_file():
                sz = item.stat().st_size
                item.unlink()
                freed += sz
            elif item.is_dir():
                sz = sum(f.stat().st_size for f in item.rglob("*") if f.is_file())
                shutil.rmtree(item, ignore_errors=True)
                freed += sz
        except Exception:
            pass
    print(f"  [LIMPIADO] {label}: {freed / (1024**2):.1f} MB liberados")
    return freed


def main():
    c_before = get_free_gb("C:\\")
    d_before = get_free_gb("D:\\")
    print(f"=== ESTADO INICIAL: C: {c_before} GB libres | D: {d_before} GB libres ===\n")

    total_bytes = 0

    # 1. Mover instaladores (.exe, .msi) y archivos takeout*.zip de Downloads a D:
    print("[1/4] Moviendo instaladores (.exe/.msi) y archivos .zip pesados de Descargas a D:...")
    if DOWNLOADS_DIR.exists():
        for f in DOWNLOADS_DIR.iterdir():
            if f.is_file():
                low = f.name.lower()
                if low.endswith((".exe", ".msi")) or low.startswith("takeout-") or (low.endswith(".zip") and f.stat().st_size > 20 * 1024 * 1024):
                    total_bytes += move_safely(f, DEST_DOWNLOADS)

    # 2. Mover respaldos legacy pesados del proyecto (chroma_db antiguo y qdrant_export.parquet estático) a D:
    print("\n[2/4] Moviendo respaldos pesados inactivos del proyecto a D:...")
    legacy_targets = [
        PROJECT_ROOT / "chroma_db",
        PROJECT_ROOT / "data" / "qdrant_export.parquet",
        PROJECT_ROOT / "data" / "tupas" / "TUPA_Loreto.zip",
    ]
    for lt in legacy_targets:
        total_bytes += move_safely(lt, DEST_LEGACY)

    # 3. Limpiar caché de pip en C:\Users\ASUS\AppData\Local\pip\cache
    print("\n[3/4] Limpiando caché de paquetes pip en C:...")
    pip_cache = Path(r"C:\Users\ASUS\AppData\Local\pip\cache")
    total_bytes += clean_directory_contents(pip_cache, "Caché de pip")

    # 4. Limpiar archivos temporales desbloqueados en AppData\Local\Temp
    print("\n[4/4] Limpiando temporales del sistema (%TEMP%)...")
    temp_dir = Path(os.environ.get("TEMP", r"C:\Users\ASUS\AppData\Local\Temp"))
    total_bytes += clean_directory_contents(temp_dir, "Temporales de Windows (%TEMP%)")

    c_after = get_free_gb("C:\\")
    d_after = get_free_gb("D:\\")
    print(f"\n=============================================================")
    print(f"✅ TOTAL PROCESADO/MOVIDO/LIBERADO: {total_bytes / (1024**3):.2f} GB ({total_bytes / (1024**2):.0f} MB)")
    print(f"=== ESTADO FINAL: C: {c_after} GB libres (antes {c_before} GB) | D: {d_after} GB libres ===")
    print(f"📁 Archivos respaldados en: {DEST_ROOT}")


if __name__ == "__main__":
    main()
