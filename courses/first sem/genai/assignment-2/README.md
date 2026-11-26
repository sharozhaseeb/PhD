# CS5004 Assignment 2 — Sharoz Haseeb, 26L-9005 (d = 5)

Diffusion models (Part A), ViT vs Swin (Part B) and Swin by hand (Part C).

| Part | My settings |
|---|---|
| A | classes **5 Sandal, 8 Bag, 1 Trouser** (18,000 images) |
| C | image **448 × 448 × 3**, **C = 128** |

## Files

| File | What it is |
|---|---|
| `26L-9005_A2.ipynb` | The notebook. Run it in Colab, top to bottom. |
| `make_report.py` | Builds the PDF report from the notebook's outputs (numbers and figures). |
| `CS5004_GenAI_Assignment_2.pdf` | The handout. |
| `prep/` | My study notes and grading checklist. **Do not submit this folder.** |

## Step by step

### 1. Photos (Part B): done, in `photos/`
Your 94 phone photos are sorted into `photos/glasses_case`, `photos/perfume`, `photos/shoe` and `photos/switch_board`, 25 each:
- **Removed:** 2 accidental blurry shots that show no object.
- **Topped up:** short classes were filled with 8 augmented copies (flip + small rotation + crop + brightness/colour), named `*_aug.jpg`.
- **Split:** the notebook puts augmented copies in the training split only, so the test set is always real photos.
- **Traceability:** `photos/file_map.csv` maps every file to its original phone file name.

**Upload:** drag the whole `photos` folder into `MyDrive/CS5004_A2/` on Google Drive, giving `MyDrive/CS5004_A2/photos/shoe/...`.

The original advice for taking photos is kept below for reference.
- Pick **4 classes** of everyday objects that you have **several different examples of**, e.g. mugs/cups, shoes, books, bottles.
  Using 3–6 different objects per class is better than 25 shots of one object.
- Take **25 photos per class** with your phone (100 in total, about 15 minutes). Keep the originals on your phone for the viva.
- For each class, a quick shot list that covers "vary background, angle and lighting":
  - 8 photos on your desk: front, side, top-down, 45°, close and a bit further away
  - 8 photos somewhere else (floor, bed, shelf, kitchen counter, outside) with different backgrounds
  - 9 photos in different light: daylight by a window, room light at night, lamp from the side, one with the flash
- Keep the object **centred and filling most of the frame**, because the 224 × 224 centre crop cuts off the edges.
  Hold the phone the same way you normally do; portrait or landscape both work (EXIF rotation is handled).
- Make a Drive folder `MyDrive/CS5004_A2/photos/` with one sub-folder per class:
  ```
  MyDrive/CS5004_A2/photos/mug/IMG_0001.jpg ... (25 files)
  MyDrive/CS5004_A2/photos/shoe/...
  MyDrive/CS5004_A2/photos/book/...
  MyDrive/CS5004_A2/photos/plant/...
  ```
  JPG, PNG and HEIC all work. The folder names become the class names in the report.

### 2. Run the notebook in Colab
1. Upload `26L-9005_A2.ipynb` to Colab and pick **Runtime → Change runtime type → T4 GPU**.
2. (Optional) To check that everything works first, set `QUICK_TEST = True` in the settings cell and run all cells. It takes
   a few minutes and uses tiny settings, and writes to a separate `outputs_quicktest/` folder that the real run never reads.
   Then set `QUICK_TEST = False` and restart the runtime.
3. Run the cells **one at a time** and read the markdown above each one. The two training cells take about 15 minutes each.
   Total run time is roughly 35–40 minutes.
4. If Colab disconnects, run the cells again. Finished checkpoints are reloaded from Drive and not retrained
   (`REUSE_CHECKPOINTS = True`), and the settings they were trained with are printed.
5. For the run you **submit**, start with an empty `outputs/ckpt/` folder, so the two training cells show their
   epoch-by-epoch logs. The marker should see the training actually happen in the notebook.

### 3. Look at your results and check the "opinion" answers
The code measures every number for you. A few sentences depend on what **you see**, so check them after the run:
- **A3 comparison** (markdown cell after the trajectory plots). It was written from a full test run of this notebook; the
  figures from that run are in `prep/reference_run_partA/`. In that run the **linear** samples looked better for Sandal/Bag/Trouser:
  a good mix of classes with sharp sandal straps. The cosine grid was mostly bags, with blurry sandals, even though its trajectory
  found the outline earlier. Your Colab run will give similar but not identical images. If your cosine grid looks better, edit
  that paragraph and set `BETTER_SCHEDULE = "cosine"` in `make_report.py`. Either way, make `SAMPLE_OBSERVATION` describe what
  *your* samples look like.
- **If you re-run after changing classes or settings, delete `outputs/ckpt/` first.** The notebook refuses to reuse a checkpoint
  trained on other classes.
- **B2 discussion**: the notebook cell and the report both pick the better backbone from your measured number of errors,
  using the same rule. If there are misclassified photos, look at them and write one sentence about them in `B2_ERROR_NOTE` in
  `make_report.py`, e.g. which classes were confused and why.

### Things worth understanding before the viva
- **Why x̂₀ is clipped during sampling.** The cosine schedule's last β is 0.999, so 1/√α₉₉₉ ≈ 31.6. Without clipping, small
  ε-errors at t = 999 blow up and the cosine samples come out black. The notebook shows this in an extra cell. Clamping x̂₀ to
  [−1, 1] and using the matching ε in the *same* update formula fixes it. The original DDPM code does the same (`clip_denoised`).
- **Why float32 (no mixed precision).** It is simpler. Some GPUs also give NaN losses in float16 with this U-Net.
- `prep/TA_CHECKLIST.md` lists likely viva questions with short answers. `prep/TA_REVIEW.md` lists what was checked.

### 4. Build the report
1. In `make_report.py`, fill in `STUDENT_NAME` and `DRIVE_LINK` (share the `CS5004_A2` Drive folder as "anyone with the link
   can view"), and check `BETTER_SCHEDULE` / `SAMPLE_OBSERVATION`.
2. In a new Colab cell:
   ```
   !pip install -q reportlab
   !python make_report.py --outputs /content/drive/MyDrive/CS5004_A2/outputs
   ```
   (upload `make_report.py` to Colab first). This writes `26L-9005_A2_report.pdf` into the outputs folder and warns
   you if it is longer than 8 pages.

### 5. Submit
- `26L-9005_A2.ipynb` with **all cells executed**. In Colab use File → Download → .ipynb, after the full run.
- `26L-9005_A2_report.pdf`.
- The Drive folder link (already in the report) with `outputs/ckpt/ddpm_linear.pt`, `outputs/ckpt/ddpm_cosine.pt` and `photos/`.

## Requirements checklist

| Handout item | Where it is |
|---|---|
| A1 linear + cosine schedules, ᾱ plot, 2 × 6 grid, explanation | A1 cells; `A1_alpha_bar.png`, `A1_forward_grid.png` |
| A2 random-init U-Net (32, 64, 128), own training step, 2 models with identical settings, loss curves, checkpoints, time / batch / lr / epochs | A2 cells; `A2_loss_curves.png`, `ckpt/*.pt`, `results.json → A2` |
| A3 own 1000-step sampler with σ² = β, 4 × 4 grids, sampling time, 8-step trajectory with x̂₀, comparison + 1000-vs-1 answer | A3 cells; `A3_samples_*.png`, `A3_trajectory_*.png` |
| B dataset collage, exif_transpose, timm transforms | Part B cells; `B_dataset_collage.png` |
| B1 hooks, shape table (tokens, channels, downsampling), param counts, FPN answer | B1 cells; tables in `results.json → B1` |
| B2 frozen features ([CLS] / GAP), one stratified 70/30 split, logistic regression, accuracy + macro-F1, confusion matrices, 3 misclassified per model, discussion | B2 cells; `B2_confusion_matrices.png`, `B2_misclassified.png` |
| C sizes, windows, Ω(MSA), Ω(W-MSA), ratio | Part C markdown (hand working) + checking code cell |
| Report ≤ 8 pages with Drive link | `make_report.py` |
