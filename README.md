# Smart-Vertigo-Dataset

Video dataset of normal and pathological eye movements and oculomotor findings recorded using smartphones in an emergency department setting.

## Repository structure and availability

The SMART-VERTIGO Dataset resources are distributed across Zenodo and GitHub. The dataset and associated documentation are deposited in Zenodo under restricted access, while the supporting video-processing code and its documentation are openly available through GitHub.

The structure below provides a unified overview of the resources available across both repositories. `ZENODO` and `GITHUB` indicate the repository in which each resource is hosted and are not themselves directories within the deposited resources.

```text
SMART-VERTIGO Dataset resources
│
├── ZENODO
│   ├── README.md
│   ├── 01_Cropped_Videos_No_Audio/
│   ├── 02_Smart_Vertigo_Dataset.xlsx
│   ├── 03_Binary_Segmentation_Masks/
│   └── Data_Use_Agreement_SMART_VERTIGO.docx
│
└── GITHUB
    └── Smart-Vertigo-Dataset/
        ├── README.md
        └── CODE/
            └── video_processing/
                ├── README.md
                ├── audit_and_remove_video_audio.py
                ├── extract_video_frames.py
                ├── spatial_crop_320x320.py
                └── requirements.txt
```

### Repository locations

**Zenodo dataset:**  
https://doi.org/10.5281/zenodo.23104512

**Data Use Agreement (DUA):**  
https://doi.org/10.5281/zenodo.23104943

**GitHub repository:**  
https://github.com/elvira-cortese/Smart-Vertigo-Dataset

**Video-processing code:**  
https://github.com/elvira-cortese/Smart-Vertigo-Dataset/tree/main/CODE/video_processing

## Zenodo resources

- **`README.md`** — Dataset-level documentation, repository structure, access information, and guidance for reuse.
- **`01_Cropped_Videos_No_Audio/`** — Cropped smartphone eye-movement videos with audio removed.
- **`02_Smart_Vertigo_Dataset.xlsx`** — Structured video-level dataset and accompanying data dictionary, controlled vocabularies, filename grammar, and clinical-label catalogues.
- **`03_Binary_Segmentation_Masks/`** — A small representative subset of binary semantic segmentation masks delineating the iris and sclera (PNG format), provided to illustrate segmentation outputs.
- **`Data_Use_Agreement_SMART_VERTIGO.docx`** — Data Use Agreement (DUA) governing access to and use of the restricted dataset.

## Dataset access

The SMART-VERTIGO Dataset is available on Zenodo under restricted access, subject to completion and approval of the Data Use Agreement (DUA).

The dataset is managed in accordance with GDPR requirements for scientific research conducted in the public interest.

## Dataset scope, structure and usage considerations

| Section | Content |
| --- | --- |
| **Dataset scope and intended use** | This dataset was designed as a video-based dataset focused on normal and pathological eye movements and oculomotor findings. It is not a case-based, patient-based, or diagnosis-based dataset. Medical diagnoses were intentionally excluded from the dataset design *a priori*. |
| **Unit of observation** | Each row represents a single video file and constitutes one observation in the dataset. Multiple videos originate from the same participant and typically correspond to different clinical tests. In a small number of cases, multiple videos may represent separate recordings or versions of the same test for the same participant; each is retained as an independent video-level observation. |
| **Video editing and cropping** | Videos were edited and cropped primarily to maintain image stability and, where possible, retain portions in which nystagmus or other relevant oculomotor movements could be observed. Cropping was not intended to preserve the complete examination, diagnostic context, or full temporal context. |
| **Interpretation limitation** | This is a video-based dataset, in which each video represents an individual observation and should be interpreted independently. All annotations and derived variables describe the findings visible or applicable to that specific video and should not be assumed to represent the participant's complete clinical examination or diagnosis. Accordingly, the absence of a feature from an individual cropped video does not necessarily indicate its absence at the participant level. |
| **Medical diagnosis variables** | Medical diagnoses were intentionally excluded from the analytical design and intended scope. |
| **Machine-learning scope** | Models developed from this dataset should primarily address video-level eye-movement or oculomotor characteristics. The dataset should not be treated as a participant-level diagnostic dataset, and video-level labels should not be automatically converted into medical diagnosis targets. |
| **Participant-level data structure** | Multiple videos may originate from the same participant and are not statistically independent. Training, validation, and test partitions should consider participant identity to prevent data leakage. Closely related alternative video versions should remain in the same partition. |
| **Original-data preservation** | Source variables are retained with their original names and values. Derived standardised variables never silently overwrite source values. |
| **Explicit source corrections applied** | Two explicitly validated source corrections were applied: `p27av` pursuit_hor result `pursuit` → `smooth`; `p71av` GEN record with missing `nyst_dir` → `horizontal_bilateral`. |
| **Validated p100av gaze exception** | The `apraxic` result recorded for the `gaze_down`, `gaze_left`, and `gaze_right` videos from participant `p100av` has been explicitly validated. These values are preserved and are not treated as source-data errors solely because they differ from the usual gaze result categories. |
| **Derived-variable missingness** | `not_applicable` indicates that a derived variable does not conceptually apply. `unknown` indicates that the variable applies but the required information is missing, unavailable, or cannot be determined reliably. |
| **result2 missingness** | When no secondary result is recorded in `result2`, `result2_standardized` is assigned `not_applicable`. Absence of a secondary result is not interpreted as unknown information. |
| **Conservative standardisation** | Standardisation corrects only unequivocal spelling, abbreviation, formatting, or predefined categorical variants and must not introduce a new clinical interpretation. |
| **Traceability** | Every derived value is traceable to one or more source variables through a documented derivation rule. |
| **Interpretation of test results and additional findings** | The `result` field and its corresponding standardised/derived variable describe the primary result directly associated with the clinical test represented in that video. Additional relevant findings, when present, are recorded separately in `result2` and/or `nyst_type`, together with their corresponding standardised variables. These additional fields provide complementary information and should not be interpreted as replacing or redefining the primary test-specific result for that particular test. |
| **Secondary-finding preservation** | A normal, negative, or otherwise non-abnormal primary result refers specifically to the test being assessed and does not imply the absence of other relevant oculomotor findings. Additional findings explicitly recorded in `result2` and/or `nystagmus_type` should therefore be interpreted as complementary findings associated with that video. |
| **Alternate-cover preservation** | For `alternate_cover`, secondary findings recorded in `result2` are preserved as complete labels and are not decomposed into `abnormality` or `abnormality_direction`. No additional clinical interpretation is derived from these labels. |
| **GEN direction-preservation rule** | When `nyst_type = gen`, the directional information recorded in `nyst_dir` is preserved in `nystagmus_direction` without clinical reinterpretation or simplification. |
| **Video-version suffix rule** | Validated numerical suffixes such as `_2` and `_3` may identify alternative versions of a video. These suffixes do not represent characteristics of the nystagmus and are excluded from `nystagmus_direction`, while the source `nyst_dir` remains available. |
| **Lighting conditions** | `good`, `regular`, and `bad` describe lighting conditions affecting the visual quality of the video. Recordings classified as `regular` or `bad` were affected by insufficient lighting and/or shadowing. |
| **Quality-control variables** | `review_required` in `DATA` is provided for data-quality assessment and manual review. It is not a clinical label and does not represent participant characteristics, clinical findings, or diagnostic outcomes. |
| **Identifiers** | `internal` and `participant_number` (the pseudonymous Participant ID provided for each video) are identifiers or traceability variables and should not be used as predictive clinical features. |
| **Filename ontology and controlled vocabulary** | The complete source-label vocabulary used in filenames is provided in `LABEL_VOCABULARY`. Filename construction rules and test-specific patterns are provided in `FILENAME_GRAMMAR`. These machine-readable sheets should be used together with the `DATA` table and standardised catalogue sheets. |
| **Filename interpretation** | Original filenames are retained for traceability and include a small number of legacy spelling variants, suffixes, and free-text qualifiers. Because underscores may occur within individual labels, filenames should not be parsed by splitting every underscore. For computational use, refer to the structured `DATA` columns and standardised variables. |
| **Direction terminology** | Two distinct direction concepts are used. Test direction/plane is derived from the bedside test label and stored in `condition/direction` (e.g., `hor` = horizontal left–right testing; `vert` = vertical up–down testing where applicable; `gaze_left/right/up/down` = instructed gaze direction). Nystagmus direction is stored separately in `nystagmus_direction`; `left/right/up/down` there refer to the fast-phase beating direction of the observed nystagmus. These variables must not be interpreted interchangeably. |
| **Operational definitions of clinical labels** | Clinical meanings of the controlled labels are documented in the catalogue sheets: `RESULT_VALUES` defines primary test results; `RESULT_DETAILS` defines secondary findings and qualifiers; `NYST_TYPES` defines nystagmus types; and `NYST_DIRECTIONS` defines nystagmus beating-direction/morphology labels. `DATA_DICTIONARY` defines the corresponding columns and links users to these catalogues. |
