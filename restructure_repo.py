#!/usr/bin/env python3
"""
restructure_repo.py — Automated repository restructuring for FL-phishingemail
================================================================================
Usage:
    python restructure_repo.py --dry-run    # Preview all changes (NO modifications)
    python restructure_repo.py --execute    # Execute changes (creates backup first)

Safety guarantees:
    - Full backup (excluding .git) before any modification
    - SHA-256 hash verification for model file deduplication
    - All operations logged to timestamped log file
    - DELETE_EMPTY only removes truly empty directories
    - Git-aware: does NOT touch .git/ internals
"""

import os
import sys
import shutil
import hashlib
import logging
import argparse
from pathlib import Path
from datetime import datetime

# ─── Configuration ───────────────────────────────────────────────────────────
REPO_ROOT = Path(__file__).resolve().parent
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
BACKUP_DIR = REPO_ROOT.parent / f"FL-phishingemail_backup_{TIMESTAMP}"
LOG_FILE = REPO_ROOT / f"restructure_log_{TIMESTAMP}.txt"


# ─── Phase Definitions ──────────────────────────────────────────────────────
# Each phase is a list of (action, *args) tuples.
# Actions: CREATE, MOVE, MOVE_DIR, RENAME, DELETE_DIR, DELETE_EMPTY, GITKEEP

PHASE_1_CREATE_STRUCTURE = [
    # 00_admin
    ("CREATE", "00_admin"),
    ("CREATE", "00_admin/emails"),
    ("CREATE", "00_admin/forms"),
    # 01_literature
    ("CREATE", "01_literature/papers"),
    ("CREATE", "01_literature/reading_notes"),
    ("CREATE", "01_literature/framework_docs"),
    # 02_data
    ("CREATE", "02_data/raw"),
    ("CREATE", "02_data/processed"),
    ("CREATE", "02_data/partitioned"),
    ("CREATE", "02_data/metadata"),
    # 04_experiments
    ("CREATE", "04_experiments/saved_models"),
    ("CREATE", "04_experiments/checkpoints/client"),
    ("CREATE", "04_experiments/checkpoints/global"),
    ("CREATE", "04_experiments/logs/metrics"),
    ("CREATE", "04_experiments/logs/stdout"),
    ("CREATE", "04_experiments/logs/forensic"),
    ("CREATE", "04_experiments/results"),
    # 05_thesis (LaTeX/Overleaf structure)
    ("CREATE", "05_thesis/chapters"),
    ("CREATE", "05_thesis/figures"),
    ("CREATE", "05_thesis/tables"),
    # 06_outputs
    ("CREATE", "06_outputs/slides"),
    ("CREATE", "06_outputs/submissions"),
    ("CREATE", "06_outputs/posters"),
    # 07_archive
    ("CREATE", "07_archive/deprecated"),
    ("CREATE", "07_archive/old_reports"),
    ("CREATE", "07_archive/misc"),
    # Reorganized code folders
    ("CREATE", "docker"),
    ("CREATE", "extensions/thunderbird_detection"),
    ("CREATE", "extensions/thunderbird_labeling"),
]

PHASE_2_MOVE_FILES = [
    # ── Root files ──
    ("MOVE", "sample_logs.txt", "07_archive/misc/sample_logs.txt"),
    ("MOVE", "clientapp.Dockerfile", "docker/clientapp.Dockerfile"),
    ("MOVE", "serverapp.Dockerfile", "docker/serverapp.Dockerfile"),

    # ── Data ──
    ("MOVE", "data/raw/phishing-email-dataset.csv",
     "02_data/raw/phishing_email_dataset.csv"),

    # ── Models (gộp tất cả vào 04_experiments/saved_models/) ──
    ("MOVE", "saved_model/model.pt",
     "04_experiments/saved_models/bert_tiny.pt"),
    ("MOVE", "saved_model/model_distilbert.pt",
     "04_experiments/saved_models/distilbert_fl_trained.pt"),
    ("MOVE", "phishing-backend/model.pt",
     "04_experiments/saved_models/distilbert_backend_deployed.pt"),

    # ── Documentation → Literature ──
    ("MOVE", "docs/reference/flwr.md",
     "01_literature/framework_docs/flwr_reference.md"),
    ("MOVE", "docs/reference/NguyenDongHai_FinalReport_24072183.md",
     "07_archive/old_reports/2025_bachelor_final_report.md"),
    ("MOVE", "docs/research/literature-review.md",
     "01_literature/reading_notes/literature_review.md"),
    ("MOVE", "docs/research/Poisoning_and_Forensic_Analysis_FL_Phishing_Detection.md",
     "01_literature/reading_notes/poisoning_forensic_analysis.md"),

    # ── Extensions ──
    ("MOVE_DIR", "thunderbird-extension", "extensions/thunderbird_detection"),
    ("MOVE_DIR", "thunderbird-extenstion-label", "extensions/thunderbird_labeling"),
]

PHASE_3_RENAME = [
    # ── Notebooks: CamelCase → snake_case ──
    ("RENAME", "notebooks/EDA_Phishing_Email_Dataset.ipynb",
     "notebooks/eda_phishing_vi.ipynb"),
    ("RENAME", "notebooks/EDA_Phishing_Email_Dataset_EN.ipynb",
     "notebooks/eda_phishing_en.ipynb"),
]

PHASE_4_CLEANUP = [
    # ── Remove deprecated empty dirs ──
    ("DELETE_DIR", "src/fl_test"),
    ("DELETE_DIR", "src"),
    ("DELETE_DIR", "fl_test/__pycache__"),

    # ── Remove emptied dirs (only if empty) ──
    ("DELETE_EMPTY", "saved_model"),
    ("DELETE_EMPTY", "data/partitioned"),
    ("DELETE_EMPTY", "data/raw"),
    ("DELETE_EMPTY", "data"),
    ("DELETE_EMPTY", "checkpoints/client"),
    ("DELETE_EMPTY", "checkpoints/global"),
    ("DELETE_EMPTY", "checkpoints"),
    ("DELETE_EMPTY", "logs/metrics"),
    ("DELETE_EMPTY", "logs/stdout"),
    ("DELETE_EMPTY", "logs/forensic"),
    ("DELETE_EMPTY", "logs"),
    ("DELETE_EMPTY", "docs/reference"),
    ("DELETE_EMPTY", "docs/research"),
]

# .DS_Store files to untrack from git
DS_STORE_FILES = [
    ".DS_Store",
    "fl_test/.DS_Store",
    "saved_model/.DS_Store",
    "phishing-backend/.DS_Store",
    "docs/.DS_Store",
    "thunderbird-extenstion-label/.DS_Store",
]

# Lines to append to .gitignore
GITIGNORE_ADDITIONS = """
# macOS metadata
.DS_Store
*/.DS_Store
**/.DS_Store

# Restructuring script logs
restructure_log_*.txt
restructure_repo.py
"""


# ─── Helpers ─────────────────────────────────────────────────────────────────

def file_hash(filepath: Path) -> str:
    """Compute SHA-256 hash for deduplication."""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def human_size(num_bytes: int) -> str:
    """Convert bytes to human-readable size."""
    for unit in ("B", "KB", "MB", "GB"):
        if abs(num_bytes) < 1024:
            return f"{num_bytes:.1f} {unit}"
        num_bytes /= 1024
    return f"{num_bytes:.1f} TB"


def setup_logging():
    """Configure dual logging: file + console."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE, encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )


def is_effectively_empty(dir_path: Path) -> bool:
    """Check if dir is empty or only contains .DS_Store / .gitkeep."""
    if not dir_path.exists() or not dir_path.is_dir():
        return True
    return not any(
        f for f in dir_path.iterdir()
        if f.name not in (".DS_Store", ".gitkeep")
    )


# ─── Core Operations ────────────────────────────────────────────────────────

def create_backup(dry_run: bool):
    """Create a full backup excluding .git directory."""
    if dry_run:
        logging.info(f"[DRY-RUN] Would backup → {BACKUP_DIR}")
        return
    logging.info(f"📦 Creating backup → {BACKUP_DIR}")
    shutil.copytree(
        REPO_ROOT, BACKUP_DIR,
        ignore=shutil.ignore_patterns(".git"),
        dirs_exist_ok=False,
    )
    logging.info(f"✅ Backup complete ({human_size(sum(f.stat().st_size for f in BACKUP_DIR.rglob('*') if f.is_file()))})")


def dedup_report():
    """Print a deduplication report for .pt model files."""
    logging.info("")
    logging.info("=" * 65)
    logging.info("  MODEL DEDUPLICATION REPORT (SHA-256)")
    logging.info("=" * 65)

    model_files = [f for f in REPO_ROOT.rglob("*.pt") if ".git" not in str(f)]
    hashes: dict[str, list[Path]] = {}
    for f in sorted(model_files):
        h = file_hash(f)
        hashes.setdefault(h, []).append(f)
        rel = f.relative_to(REPO_ROOT)
        logging.info(f"  {str(rel):<55}  {human_size(f.stat().st_size):>10}  {h[:16]}...")

    logging.info("-" * 65)
    dupes = {h: fs for h, fs in hashes.items() if len(fs) > 1}
    if dupes:
        for h, files in dupes.items():
            logging.warning(f"  ⚠️  DUPLICATE SET (hash {h[:16]}...):")
            for f in files:
                logging.warning(f"      → {f.relative_to(REPO_ROOT)}")
    else:
        logging.info("  ✅ No duplicate models found — all files are unique.")
    logging.info("=" * 65)
    logging.info("")


def execute_phase(phase_name: str, operations: list, dry_run: bool):
    """Execute a list of (action, *args) operations."""
    logging.info("")
    logging.info(f"{'─' * 5} {phase_name} {'─' * (55 - len(phase_name))}")

    success = 0
    skipped = 0
    failed = 0

    for op in operations:
        action = op[0]
        try:
            if action == "CREATE":
                target = REPO_ROOT / op[1]
                if target.exists():
                    skipped += 1
                    continue
                if dry_run:
                    logging.info(f"  [DRY] MKDIR    {op[1]}/")
                else:
                    target.mkdir(parents=True, exist_ok=True)
                    # Add .gitkeep to leaf dirs
                    gitkeep = target / ".gitkeep"
                    gitkeep.touch()
                    logging.info(f"  ✅   MKDIR    {op[1]}/")
                success += 1

            elif action == "MOVE":
                src = REPO_ROOT / op[1]
                dst = REPO_ROOT / op[2]
                if not src.exists():
                    logging.warning(f"  ⚠️   SKIP     {op[1]}  (not found)")
                    skipped += 1
                    continue
                if dst.exists():
                    logging.warning(f"  ⚠️   SKIP     {op[1]}  (destination exists: {op[2]})")
                    skipped += 1
                    continue
                if dry_run:
                    logging.info(f"  [DRY] MOVE     {op[1]}")
                    logging.info(f"               → {op[2]}")
                else:
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(src), str(dst))
                    logging.info(f"  ✅   MOVE     {op[1]}")
                    logging.info(f"               → {op[2]}")
                success += 1

            elif action == "MOVE_DIR":
                src = REPO_ROOT / op[1]
                dst = REPO_ROOT / op[2]
                if not src.exists():
                    logging.warning(f"  ⚠️   SKIP     {op[1]}/  (not found)")
                    skipped += 1
                    continue
                if dry_run:
                    items = [f.name for f in src.iterdir() if f.name != ".DS_Store"]
                    logging.info(f"  [DRY] MOVEDIR  {op[1]}/  ({len(items)} items)")
                    logging.info(f"               → {op[2]}/")
                else:
                    dst.mkdir(parents=True, exist_ok=True)
                    for item in src.iterdir():
                        if item.name == ".DS_Store":
                            continue
                        dest_item = dst / item.name
                        if item.is_dir():
                            shutil.copytree(str(item), str(dest_item))
                        else:
                            shutil.copy2(str(item), str(dest_item))
                    shutil.rmtree(str(src))
                    logging.info(f"  ✅   MOVEDIR  {op[1]}/  → {op[2]}/")
                success += 1

            elif action == "RENAME":
                src = REPO_ROOT / op[1]
                dst = REPO_ROOT / op[2]
                if not src.exists():
                    logging.warning(f"  ⚠️   SKIP     {op[1]}  (not found)")
                    skipped += 1
                    continue
                if dry_run:
                    logging.info(f"  [DRY] RENAME   {op[1]}")
                    logging.info(f"               → {op[2]}")
                else:
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    src.rename(dst)
                    logging.info(f"  ✅   RENAME   {op[1]}  → {op[2]}")
                success += 1

            elif action == "DELETE_DIR":
                target = REPO_ROOT / op[1]
                if not target.exists():
                    skipped += 1
                    continue
                if dry_run:
                    logging.info(f"  [DRY] RMDIR    {op[1]}/")
                else:
                    shutil.rmtree(str(target))
                    logging.info(f"  ✅   RMDIR    {op[1]}/")
                success += 1

            elif action == "DELETE_EMPTY":
                target = REPO_ROOT / op[1]
                if not target.exists():
                    skipped += 1
                    continue
                if not is_effectively_empty(target):
                    logging.warning(f"  ⚠️   SKIP     {op[1]}/  (not empty)")
                    skipped += 1
                    continue
                if dry_run:
                    logging.info(f"  [DRY] RMEMPTY  {op[1]}/")
                else:
                    shutil.rmtree(str(target))
                    logging.info(f"  ✅   RMEMPTY  {op[1]}/")
                success += 1

        except Exception as e:
            logging.error(f"  ❌   FAILED   {action} {op[1]}: {e}")
            failed += 1

    logging.info(f"  → Results: {success} done, {skipped} skipped, {failed} failed")


def git_cleanup(dry_run: bool):
    """Remove .DS_Store from git tracking and update .gitignore."""
    logging.info("")
    logging.info(f"{'─' * 5} Git Cleanup {'─' * 48}")

    # Untrack .DS_Store files
    for f in DS_STORE_FILES:
        fp = REPO_ROOT / f
        if fp.exists():
            if dry_run:
                logging.info(f"  [DRY] git rm --cached {f}")
            else:
                os.system(f'cd "{REPO_ROOT}" && git rm --cached "{f}" 2>/dev/null')
                logging.info(f"  ✅   git rm --cached {f}")

    # Update .gitignore
    gitignore = REPO_ROOT / ".gitignore"
    if gitignore.exists():
        content = gitignore.read_text()
        if "**/.DS_Store" not in content:
            if dry_run:
                logging.info("  [DRY] Append .DS_Store rules to .gitignore")
            else:
                with open(gitignore, "a") as f:
                    f.write(GITIGNORE_ADDITIONS)
                logging.info("  ✅   Updated .gitignore with .DS_Store + script log rules")


def update_backend_model_path(dry_run: bool):
    """Update phishing-backend/app.py to load model from new location."""
    logging.info("")
    logging.info(f"{'─' * 5} Update Backend Model Path {'─' * 35}")

    app_py = REPO_ROOT / "phishing-backend" / "app.py"
    if not app_py.exists():
        logging.warning("  ⚠️   phishing-backend/app.py not found")
        return

    content = app_py.read_text()
    old_line = 'torch.load("model.pt"'
    new_line = 'torch.load(os.path.join(os.path.dirname(__file__), "..", "04_experiments", "saved_models", "distilbert_backend_deployed.pt")'

    if old_line not in content:
        logging.info("  ⚠️   model.pt reference not found (already updated?)")
        return

    if dry_run:
        logging.info(f"  [DRY] Would update app.py model path:")
        logging.info(f"         OLD: {old_line})")
        logging.info(f"         NEW: ...04_experiments/saved_models/distilbert_backend_deployed.pt...")
    else:
        # Add import os if not present
        if "import os" not in content:
            content = "import os\n" + content
        content = content.replace(old_line, new_line)
        app_py.write_text(content)
        logging.info("  ✅   Updated app.py to use new model path")


def create_thesis_template(dry_run: bool):
    """Create LaTeX thesis template files."""
    logging.info("")
    logging.info(f"{'─' * 5} Create LaTeX Thesis Templates {'─' * 30}")

    templates = {
        "05_thesis/references.bib": """\
%% Master Thesis Bibliography
%% Federated Learning for Phishing Email Detection with Poison-Forensics
%% Author: Nguyen Dong Hai
%% Managed via: LaTeX/Overleaf + BibTeX
%%
%% Usage: Add entries below. Use Google Scholar "Cite as BibTeX" or DBLP.
%% In your .tex file: \\bibliography{references}

@inproceedings{mcmahan2017fedavg,
  title     = {Communication-Efficient Learning of Deep Networks from Decentralized Data},
  author    = {McMahan, Brendan and Moore, Eider and Ramage, Daniel and Hampson, Seth and Arcas, Blaise Ag{\\"u}era y},
  booktitle = {Proceedings of the 20th International Conference on Artificial Intelligence and Statistics (AISTATS)},
  year      = {2017},
}

@inproceedings{jia2024flforensics,
  title     = {Tracing Back the Malicious Clients in Poisoning Attacks to Federated Learning},
  author    = {Jia, Yuqi and Fang, Minghong and Liu, Hongbin and Zhang, Jinghuai and Gong, Neil Zhenqiang},
  booktitle = {Advances in Neural Information Processing Systems (NeurIPS)},
  year      = {2024},
}
""",
        "05_thesis/main.tex": """\
%% =============================================================================
%% Master Thesis: Federated Learning for Phishing Email Detection
%%                with Poison-Forensics
%% Author: Nguyen Dong Hai (24072183)
%% University: International University - VNU HCM
%% =============================================================================
%% This is a placeholder template. Replace with your Overleaf project structure.
%% =============================================================================

\\documentclass[12pt,a4paper]{report}
\\usepackage[utf8]{inputenc}
\\usepackage{graphicx}
\\usepackage{hyperref}
\\usepackage{amsmath}
\\usepackage{booktabs}
\\usepackage{natbib}

\\title{Federated Learning for Phishing Email Detection with Poison-Forensics}
\\author{Nguyen Dong Hai \\\\ Student ID: 24072183}
\\date{\\today}

\\begin{document}
\\maketitle
\\tableofcontents

\\chapter{Introduction}
% \\input{chapters/ch01_introduction}

\\chapter{Literature Review}
% \\input{chapters/ch02_literature_review}

\\chapter{Methodology}
% \\input{chapters/ch03_methodology}

\\chapter{Implementation}
% \\input{chapters/ch04_implementation}

\\chapter{Experiments and Results}
% \\input{chapters/ch05_experiments}

\\chapter{Conclusion}
% \\input{chapters/ch06_conclusion}

\\bibliographystyle{plainnat}
\\bibliography{references}

\\end{document}
""",
    }

    for rel_path, content in templates.items():
        target = REPO_ROOT / rel_path
        if target.exists():
            logging.info(f"  ⚠️   SKIP {rel_path} (already exists)")
            continue
        if dry_run:
            logging.info(f"  [DRY] CREATE   {rel_path}")
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
            logging.info(f"  ✅   CREATE   {rel_path}")


def create_dataset_card(dry_run: bool):
    """Create a dataset card for the phishing email dataset."""
    card_path = REPO_ROOT / "02_data" / "metadata" / "dataset_card.md"
    content = """\
# 📊 Dataset Card: Phishing Email Dataset

| Field | Value |
|-------|-------|
| **Name** | Phishing Email Dataset |
| **Source** | [Cần bổ sung: Kaggle URL hoặc nguồn gốc] |
| **Size** | ~52 MB |
| **Format** | CSV |
| **Rows** | [Cần bổ sung: số dòng] |
| **Columns** | `Email Text`, `Email Type` (0=Safe, 1=Phishing) |
| **Class Balance** | [Cần bổ sung: tỷ lệ phishing/safe] |
| **Language** | English |
| **License** | [Cần bổ sung] |

## Preprocessing Notes

- Tokenized using `distilbert-base-uncased` tokenizer
- Max sequence length: 512 tokens
- Partitioned using Dirichlet distribution (α configurable)
- Non-IID partitioning across 4 FL clients

## Known Issues

- [Cần bổ sung: missing values, encoding issues, etc.]
"""
    if card_path.exists():
        logging.info(f"  ⚠️   SKIP dataset_card.md (already exists)")
        return
    if dry_run:
        logging.info(f"  [DRY] CREATE   02_data/metadata/dataset_card.md")
    else:
        card_path.parent.mkdir(parents=True, exist_ok=True)
        card_path.write_text(content, encoding="utf-8")
        logging.info(f"  ✅   CREATE   02_data/metadata/dataset_card.md")


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="🗂️ Restructure FL-phishingemail repository",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  python restructure_repo.py --dry-run    # Safe preview — no changes made
  python restructure_repo.py --execute    # Full restructure with backup
        """,
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true",
                       help="Preview all changes without modifying anything")
    mode.add_argument("--execute", action="store_true",
                       help="Execute restructuring (creates backup first)")
    args = parser.parse_args()
    dry_run = args.dry_run

    setup_logging()

    logging.info("=" * 65)
    logging.info("  🗂️  FL-phishingemail Repository Restructuring")
    logging.info(f"  Mode:   {'🔍 DRY-RUN (preview only)' if dry_run else '🚀 EXECUTE (live changes)'}")
    logging.info(f"  Repo:   {REPO_ROOT}")
    logging.info(f"  Branch: master-research")
    logging.info(f"  Time:   {datetime.now().isoformat()}")
    logging.info("=" * 65)

    # ── Step 0: Dedup report ──
    dedup_report()

    # ── Step 1: Backup ──
    if not dry_run:
        create_backup(dry_run=False)
    else:
        logging.info(f"\n  [DRY-RUN] Would create backup at:")
        logging.info(f"  {BACKUP_DIR}")

    # ── Step 2: Git cleanup (.DS_Store) ──
    git_cleanup(dry_run)

    # ── Step 3: Create new directory structure ──
    execute_phase("Phase 1: Create Directory Structure", PHASE_1_CREATE_STRUCTURE, dry_run)

    # ── Step 4: Move files to new locations ──
    execute_phase("Phase 2: Move Files", PHASE_2_MOVE_FILES, dry_run)

    # ── Step 5: Rename files ──
    execute_phase("Phase 3: Rename Files", PHASE_3_RENAME, dry_run)

    # ── Step 6: Clean up empty directories ──
    execute_phase("Phase 4: Cleanup Empty Dirs", PHASE_4_CLEANUP, dry_run)

    # ── Step 7: Update backend model path ──
    update_backend_model_path(dry_run)

    # ── Step 8: Create LaTeX thesis templates ──
    create_thesis_template(dry_run)

    # ── Step 9: Create dataset card ──
    create_dataset_card(dry_run)

    # ── Summary ──
    logging.info("")
    logging.info("=" * 65)
    if dry_run:
        logging.info("  🔍 DRY-RUN COMPLETE — No changes were made.")
        logging.info("")
        logging.info("  Review the output above carefully, then run:")
        logging.info("    python restructure_repo.py --execute")
        logging.info("")
        logging.info("  ⚠️  BEFORE executing, make sure to:")
        logging.info("    1. git add -A && git commit -m 'snapshot before restructure'")
        logging.info("    2. git push origin master-research")
    else:
        logging.info("  🎉 RESTRUCTURING COMPLETE!")
        logging.info("")
        logging.info(f"  📦 Backup:  {BACKUP_DIR}")
        logging.info(f"  📝 Log:     {LOG_FILE}")
        logging.info("")
        logging.info("  Next steps:")
        logging.info("    1. Review:  git status")
        logging.info("    2. Verify:  ls -la 04_experiments/saved_models/")
        logging.info("    3. Stage:   git add -A")
        logging.info("    4. Commit:  git commit -m 'refactor: restructure repo for thesis phase'")
        logging.info("    5. Push:    git push origin master-research")
    logging.info("=" * 65)


if __name__ == "__main__":
    main()
