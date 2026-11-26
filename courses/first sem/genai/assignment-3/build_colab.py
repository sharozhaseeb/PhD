"""Build a self-contained notebook without downloading model weights locally."""

import base64
import json
import zlib
from pathlib import Path
import nbformat as nb

HERE = Path(__file__).resolve().parent
code = nb.v4.new_code_cell
markdown = nb.v4.new_markdown_cell
files = ["track3_preflight.py", "train_group3.py", "collect_results.py",
         "group3_run_plan.json", "track3_preflight.json", "colab_requirements.txt"]
payload = base64.b64encode(zlib.compress(json.dumps(
    {name: (HERE / name).read_text(encoding="utf-8-sig") for name in files}
).encode())).decode()

notebook = nb.v4.new_notebook(cells=[
    markdown("""# Advanced GenAI Assignment 3: Urdu tweet sentiment
Provisional Group 3, seeds 3 and 103. Use a Colab T4.
First run the setup and eight smoke checks. Full training is opt-in.
The compressed bundle is just the readable files provided alongside this notebook."""),
    code(f"""from pathlib import Path
import base64, json, zlib, sys, subprocess
WORK = Path('/content/genai_a3_code')
WORK.mkdir(exist_ok=True)
for name, contents in json.loads(zlib.decompress(base64.b64decode({payload!r}))).items():
    (WORK / name).write_text(contents, encoding='utf-8')
subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', '-r', str(WORK/'colab_requirements.txt')], check=True)
subprocess.run(['nvidia-smi', '--query-gpu=name,memory.total', '--format=csv'], check=True)
"""),
    markdown("## Verified dataset and tokenizer setup\nThe original pinned TSV is read directly; there is no character reversal. Split membership, tokenizer audit, and nested scarcity subsets are preserved."),
    code("""audit = json.loads((WORK/'track3_preflight.json').read_text())
plan = json.loads((WORK/'group3_run_plan.json').read_text())
print({k: v['labels'] for k, v in audit['splits'].items()})
print(audit['tokenizers'])
sys.path.insert(0, str(WORK))
from collect_results import job_id

# Before full training, mount Drive and update OUTPUT to a folder
# under /content/drive/MyDrive. Colab asks the account owner for access.
OUTPUT = Path('/content/genai_a3_evidence')
MICROBATCH = 8
def invoke(script, *args):
    command = [sys.executable, '-u', str(WORK/script), *map(str, args)]
    with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True) as process:
        for line in process.stdout:
            print(line, end='', flush=True)
        if process.wait() != 0:
            raise RuntimeError(f'{script} failed with exit code {process.returncode}; inspect the output above')
def run_jobs(jobs, smoke=False):
    for job in jobs:
        invoke('train_group3.py', job_id(job), '--output', OUTPUT,
               '--microbatch', MICROBATCH, *(['--smoke'] if smoke else []))
"""),
    markdown("## T4 smoke checks\nOne short optimizer step per encoder and method. These outputs are operational checks and are excluded from the results CSV."),
    code("""smoke_jobs = [j for j in plan['jobs'] if j['seed'] == 3 and j['experiment'] in ('01','03','05','07b')]
run_jobs(smoke_jobs, smoke=True)
"""),
    markdown("## Pilot and full roster\nThe pilot is one real three-epoch run. Inspect its logs and reload checks before the full roster. The full workflow requires a mounted Drive path so a disconnect cannot erase evidence. Do not inspect test predictions before validation selection."),
    code("""RUN_PILOT = False
RUN_FULL = False
if RUN_FULL or RUN_PILOT:
    from google.colab import drive
    drive.mount('/content/drive')
    if not Path('/content/drive/MyDrive').is_dir():
        raise RuntimeError('Mount Drive to keep training evidence across disconnects.')
    OUTPUT = Path('/content/drive/MyDrive/AdvancedGenAI_A3_Group3/run_v1')
if RUN_PILOT:
    run_jobs([next(j for j in plan['jobs'] if job_id(j) == 'xlmr_01_full_ft_3_100')])
if RUN_FULL:
    run_jobs(j for j in plan['jobs'] if j['fraction'] == 1)
    invoke('collect_results.py', OUTPUT, '--select-only')
    run_jobs(j for j in plan['jobs'] if j['experiment'] == '08')
    invoke('collect_results.py', OUTPUT)
elif not RUN_PILOT:
    print('Pilot and full training are disabled. Complete smoke checks before enabling either.')
"""),
    markdown("## Export\nAfter all runs, download the executed notebook using File > Download > Download .ipynb, plus the evidence archive. Raw tweets and model weights are not in this archive."),
    code("""if RUN_FULL or RUN_PILOT:
    import shutil
    path = shutil.make_archive('/content/genai_a3_evidence', 'zip', OUTPUT)
    print(path)
"""),
], metadata={"accelerator": "GPU", "colab": {"gpuType": "T4"},
             "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}})
nb.validate(notebook)
nb.write(notebook, HERE / "Group3_Colab.ipynb")
