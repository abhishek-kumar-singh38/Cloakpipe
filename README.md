# CloakPipe

**CloakPipe** is an educational binary-transformation and detection-research pipeline.

It studies how controlled transformations and different compilation settings change the static representation of **benign programs**, and which measurable properties remain useful for defensive analysis.

> This repository intentionally uses benign test data and does not implement shellcode execution, persistence, credential theft, sandbox bypasses, or EDR-disabling behavior.

## Research pipeline

```text
Benign Test Data
      |
      v
Controlled Transformation
      |
      +--> SHA-256 / Entropy
      |
      v
Source Template Generation
      |
      v
Optional Native Compilation
      |
      v
Binary Metadata Analysis
      |
      v
Experiment Report
```

## Features

- Controlled byte transformations for experiments
- SHA-256 comparison
- Shannon entropy measurement
- Jinja2 source-template generation
- Optional local GCC/Clang compilation of benign programs
- Basic PE/ELF identification
- JSON experiment reporting
- Unit tests and GitHub Actions CI

## Installation

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
pip install -e .
```

## Quick start

```bash
python -m cloakpipe.cli analyze examples/benign_sample/sample.bin

python -m cloakpipe.cli transform examples/benign_sample/sample.bin --method xor --output experiments/results/transformed.bin

python -m cloakpipe.cli generate examples/benign_sample/sample.bin --output experiments/results/generated.c

pytest
```

## Research questions

1. How much does a transformation change a file hash?
2. How does transformation affect byte entropy?
3. Which properties remain stable across multiple builds?
4. How do compiler options affect binary structure?
5. Which static features are useful for defensive classification?

## Safety

Only use this project with files and systems you own or are explicitly authorized to test.

## License

MIT
