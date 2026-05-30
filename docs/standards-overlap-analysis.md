# T3.11 — Standards Overlap Analysis

This document compares the five metadata standards used in this project:
**RO-Crate**, **CodeMeta**, **FAIR4ML**, **Croissant**, and **Model Card**.
For each pair we look at what they share, what is unique to each, and where
they conflict. At the end we list the concrete inconsistencies in our own
files.

## 1. The five standards at a glance

| Standard       | Describes                                     | Format   | Audience                         | File in this repo                                         |
| -------------- | --------------------------------------------- | -------- | -------------------------------- | --------------------------------------------------------- |
| **RO-Crate**   | A research package (everything in one bundle) | JSON-LD  | Repositories, archivists         | `ro-crate-metadata.json`                                  |
| **CodeMeta**   | Software (source code, dependencies, version) | JSON-LD  | Software registries, devs        | `codemeta.json`                                           |
| **FAIR4ML**    | A trained ML model (algorithm, metrics)       | JSON-LD  | Model registries, ML researchers | `docs/fair4ml/gradient_boosting_severity_2026-05-25.json` |
| **Croissant**  | A dataset for ML (schema, fields, splits)     | JSON-LD  | ML frameworks, data tools        | `croissant.json`                                          |
| **Model Card** | A model for humans (use cases, ethics)        | Markdown | End users, decision-makers       | `docs/model-card.md`                                      |

Four of the five are JSON-LD and share schema.org as a base vocabulary, which
is why so many of the fields look the same. Only Model Card is plain Markdown.

## 2. Field overlap across all five standards

The table below shows which standard typically carries each kind of metadata.
"✓" means the field is normally there, "—" means it's not part of that
standard's core scope.

| Field / Concept              | RO-Crate | CodeMeta | FAIR4ML | Croissant | Model Card |
| ---------------------------- | :------: | :------: | :-----: | :-------: | :--------: |
| Name / title                 |    ✓     |    ✓     |    ✓    |     ✓     |     ✓      |
| Description / abstract       |    ✓     |    ✓     |    ✓    |     ✓     |     ✓      |
| Authors (with ORCIDs)        |    ✓     |    ✓     |    ✓    |     ✓     |     ✓      |
| License                      |    ✓     |    ✓     |    ✓    |     ✓     |     ✓      |
| Version                      |    ✓     |    ✓     |    ✓    |     ✓     |     —      |
| Date created / published     |    ✓     |    ✓     |    ✓    |     ✓     |     —      |
| Identifier (DOI / URL)       |    ✓     |    ✓     |    ✓    |     ✓     |     —      |
| Keywords                     |    ✓     |    ✓     |    —    |     ✓     |     —      |
| File listing / parts         |    ✓     |    —     |    —    |     ✓     |     —      |
| Source code repository       |    ✓     |    ✓     |    ✓    |     —     |     —      |
| Dependencies (with versions) |    —     |    ✓     |    —    |     —     |     —      |
| Programming language         |    —     |    ✓     |    —    |     —     |     —      |
| Training algorithm + version |    —     |    —     |    ✓    |     —     |     ✓      |
| Hyperparameters              |    —     |    —     |    ✓    |     —     |     —      |
| Evaluation metrics (values)  |    —     |    —     |    ✓    |     —     |     ✓      |
| Training dataset reference   |    —     |    —     |    ✓    |     —     |     ✓      |
| Model selection / candidates |    —     |    —     |    ✓    |     —     |     ✓      |
| Data schema (fields + types) |    —     |    —     |    —    |     ✓     |     —      |
| Units of measurement         |    —     |    —     |    —    |     ✓     |     —      |
| Data splits (train/val/test) |    —     |    —     |    ✓    |     ✓     |     —      |
| Intended use                 |    —     |    —     |    ✓    |     —     |     ✓      |
| Out-of-scope use             |    —     |    —     |    —    |     —     |     ✓      |
| Limitations                  |    —     |    —     |    ✓    |     —     |     ✓      |
| Ethical considerations       |    —     |    —     |    —    |     —     |     ✓      |
| Provenance / lineage         |    ✓     |    —     |    ✓    |     ✓     |     —      |

The pattern is pretty clear: **RO-Crate** is the outer container that lists
all the files; **CodeMeta** does software and dependencies; **FAIR4ML** and
**Model Card** cover the model from two angles (machine vs. human);
**Croissant** owns the dataset schema in detail.

## 3. Pairwise comparison

Ten pairs total. For each one: what overlaps, what's unique, where things
tend to clash.

### 3.1 RO-Crate ↔ CodeMeta

- **Overlap:** name, description, authors, license, version, code repo URL,
  date.
- **Unique to RO-Crate:** the file-by-file listing of everything in the package
  (`hasPart`), file relationships, validation profile.
- **Unique to CodeMeta:** programming language and runtime, full dependency list
  with pinned versions, dev status (active / inactive).
- **Conflicts:** basically none — they answer different questions. RO-Crate
  says "here's the package and what's in it"; CodeMeta says "here's what
  software runs it." Different layers.

### 3.2 RO-Crate ↔ FAIR4ML

- **Overlap:** name, description, authors, license, identifier, training-data
  reference (RO-Crate via `hasPart`, FAIR4ML via `trainedOn`).
- **Unique to RO-Crate:** the full file inventory of the research package.
- **Unique to FAIR4ML:** all the model-specific stuff — algorithm,
  hyperparameters, metrics, model selection, intended use, limitations.
- **Conflicts:** usually the **identifier** field. RO-Crate identifies the
  _whole package_; FAIR4ML identifies the _training dataset_. If they get
  filled in inconsistently, they point at different DOIs. (Exactly what
  happens in our repo — see Section 5.)

### 3.3 RO-Crate ↔ Croissant

- **Overlap:** dataset-level metadata (name, description, license, creator,
  keywords, file references).
- **Unique to RO-Crate:** non-data files (notebooks, code, models, figures)
  alongside the dataset.
- **Unique to Croissant:** field-level schema, data types, units of
  measurement, value enums, references between fields.
- **Conflicts:** none in spec, but **scope confusion** is easy. Dataset
  metadata ends up in RO-Crate at the package level and again in Croissant at
  the dataset level — they should match but can easily drift.

### 3.4 RO-Crate ↔ Model Card

- **Overlap:** name, description, license. Not much else.
- **Unique to RO-Crate:** package structure, file listing, provenance graph.
- **Unique to Model Card:** intended use, out-of-scope use, ethical
  considerations, human-readable evaluation.
- **Conflicts:** none — they barely overlap. RO-Crate is the wrapper, Model
  Card is documentation for one specific artifact inside the wrapper.

### 3.5 CodeMeta ↔ FAIR4ML

- **Overlap:** name, description, authors, license, version, identifier,
  source repo.
- **Unique to CodeMeta:** programming language, dependencies, software status.
- **Unique to FAIR4ML:** everything model-specific (algorithm,
  hyperparameters, metrics, training data reference).
- **Conflicts:** the **version** field. CodeMeta versions are about the
  _software pipeline_; FAIR4ML versions are about the _trained model_. These
  can diverge — software v1.2.0 might produce model v2.0.0. People often
  copy one into the other and lose that distinction.

### 3.6 CodeMeta ↔ Croissant

- **Overlap:** name, description, authors, license, keywords, identifier.
- **Unique to CodeMeta:** software-only fields.
- **Unique to Croissant:** all the data-specific fields (schema, types, units,
  splits, references).
- **Conflicts:** basically none — they describe different artifacts (code vs.
  data). Only mild overlap is when both list authors, which should match.

### 3.7 CodeMeta ↔ Model Card

- **Overlap:** name, license, authors (loosely).
- **Unique to CodeMeta:** software and dependencies.
- **Unique to Model Card:** intended use, limitations, ethics, evaluation
  narrative.
- **Conflicts:** basically none. CodeMeta describes the software that
  produces the model; Model Card describes the model. Adjacent, not
  overlapping.

### 3.8 FAIR4ML ↔ Croissant

- **Overlap:** training dataset reference, data splits, license, authors.
- **Unique to FAIR4ML:** everything about the model.
- **Unique to Croissant:** field-level schema and units of the dataset.
- **Conflicts:** the **dataset description**. FAIR4ML names the training set
  in one or two fields (`trainedOn.name`, `trainedOn.identifier`); Croissant
  describes it in full. If they reference different revisions or DOIs of the
  same dataset, reproducibility breaks.

### 3.9 FAIR4ML ↔ Model Card

- **Overlap:** intended use, limitations, evaluation metrics, training data
  reference, algorithm name, license, authors. **This is the biggest overlap
  of any pair in the project.**
- **Unique to FAIR4ML:** machine-readable structure, full hyperparameter list,
  model selection record, exact numeric metrics, model artifact location.
- **Unique to Model Card:** out-of-scope use, ethical considerations,
  human-readable narrative around the same numbers.
- **Conflicts:** **the metric values themselves**, if they're entered by hand
  in both files. Easy to round one and not the other, or update one when the
  model is retrained but not the other. Fix: generate the Model Card text
  _from_ the FAIR4ML JSON, or just be clear about which file is the source
  of truth.

### 3.10 Croissant ↔ Model Card

- **Overlap:** training data reference, license.
- **Unique to Croissant:** field-level schema and data types.
- **Unique to Model Card:** all the narrative/ethics/use-case stuff.
- **Conflicts:** none in spec. The two describe opposite ends of the
  pipeline (input data schema vs. trained model documentation).
