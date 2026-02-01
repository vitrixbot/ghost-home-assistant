# Ghost Integration Submission to Home Assistant Core

You are helping submit the Ghost integration to the Home Assistant Core repository. The integration is fully developed and tested in a separate repository. Your job is to copy it into the correct location in the HA core repo, run the required scripts, verify everything works, and prepare for PR submission.

## Source Repository

The Ghost integration source is at: `~/clawd/ghost-home-assistant/custom_components/ghost/`

## Target Repository

The Home Assistant Core fork should be cloned locally. The integration goes into: `homeassistant/components/ghost/`

---

## Step 1: Copy Integration Files

Copy these files from the source to the target:

```
SOURCE: ~/clawd/ghost-home-assistant/custom_components/ghost/
TARGET: homeassistant/components/ghost/

Files to copy:
├── __init__.py
├── config_flow.py
├── const.py
├── coordinator.py
├── diagnostics.py
├── manifest.json
├── quality_scale.yaml
├── sensor.py
├── strings.json
├── webhook.py
├── icons.json
└── translations/
    └── en.json
```

**DO NOT copy:**
- `icon.png` and `icon@2x.png` (these go to home-assistant/brands repo separately)
- `__pycache__/` directories
- Any `.pyc` files

---

## Step 2: Copy Test Files

Copy tests to the HA core test directory:

```
SOURCE: ~/clawd/ghost-home-assistant/tests/
TARGET: tests/components/ghost/

Files to copy:
├── __init__.py
├── conftest.py
├── test_config_flow.py
├── test_coordinator.py
├── test_diagnostics.py
├── test_init.py
├── test_sensor.py
└── test_webhook.py
```

---

## Step 3: Run Required Scripts

From the HA core repository root, run these scripts:

### 3.1 Generate requirements_all.txt
```bash
python3 -m script.gen_requirements_all
```
This adds `aioghost==0.3.0` to `requirements_all.txt`.

### 3.2 Run hassfest
```bash
python3 -m script.hassfest
```
This validates the manifest and generates derived files like CODEOWNERS entries.

### 3.3 Verify with hassfest (strict mode)
```bash
python3 -m script.hassfest --integration-path homeassistant/components/ghost
```

---

## Step 4: Run Tests

### 4.1 Run integration tests
```bash
pytest tests/components/ghost/ -v
```

### 4.2 Run with coverage
```bash
pytest tests/components/ghost/ --cov=homeassistant.components.ghost --cov-report=term-missing
```

Coverage should be >95% (we have ~99%).

### 4.3 Run linting
```bash
ruff check homeassistant/components/ghost/
ruff format --check homeassistant/components/ghost/
```

### 4.4 Run mypy (optional but recommended)
```bash
mypy homeassistant/components/ghost/
```

Note: Some "cannot subclass Any" errors are expected until HA stubs are applied during CI.

---

## Step 5: Verify Manifest

Check `homeassistant/components/ghost/manifest.json` contains:

```json
{
  "codeowners": ["@johnonolan"],
  "config_flow": true,
  "documentation": "https://www.home-assistant.io/integrations/ghost",
  "domain": "ghost",
  "integration_type": "service",
  "iot_class": "cloud_polling",
  "loggers": ["aioghost"],
  "name": "Ghost",
  "quality_scale": "platinum",
  "requirements": ["aioghost==0.3.0"]
}
```

**Critical checks:**
- NO `version` field (core integrations don't use this)
- `quality_scale` is set to `platinum`
- `codeowners` is `@johnonolan` (personal GitHub, not org)
- Keys are in alphabetical order

---

## Step 6: Verify quality_scale.yaml

Ensure `homeassistant/components/ghost/quality_scale.yaml` exists and has all rules marked as either `done` or `exempt` with comments.

---

## Step 7: Check CODEOWNERS

After running hassfest, verify that `CODEOWNERS` file in repo root contains:
```
homeassistant/components/ghost/* @johnonolan
```

---

## Step 8: Verify Generated Files

After running scripts, check these files were updated:
- `requirements_all.txt` — should contain `aioghost==0.3.0`
- `CODEOWNERS` — should have ghost entry
- `.coveragerc` — may be updated

---

## Step 9: Pre-commit Checks

Run the full pre-commit suite:
```bash
pre-commit run --all-files
```

Or at minimum:
```bash
ruff check .
ruff format .
```

---

## Step 10: Final Verification Checklist

Before committing, verify:

- [ ] All files copied to correct locations
- [ ] `python3 -m script.gen_requirements_all` ran successfully
- [ ] `python3 -m script.hassfest` ran successfully
- [ ] `pytest tests/components/ghost/ -v` — all tests pass
- [ ] `ruff check homeassistant/components/ghost/` — no errors
- [ ] No `version` in manifest.json
- [ ] `quality_scale: platinum` in manifest.json
- [ ] `quality_scale.yaml` exists with all rules addressed
- [ ] CODEOWNERS updated with @johnonolan

---

## Step 11: Commit

Create a single commit with message:
```
Add Ghost integration
```

Do NOT use prefixes like `[ghost]` or `feat:`. Keep it simple.

---

## Step 12: Documentation PR (Separate)

A separate PR is needed for `home-assistant/home-assistant.io`:
- Copy `~/clawd/ghost-home-assistant/docs/ghost.md` to `source/_integrations/ghost.markdown`
- Note: File extension changes from `.md` to `.markdown`

---

## Step 13: Brand Assets PR (Separate)

A separate PR is needed for `home-assistant/brands`:
- Copy `icon.png` to `custom_integrations/ghost/icon.png`
- Copy `icon@2x.png` to `custom_integrations/ghost/icon@2x.png`
- After core PR is merged, these move to `core_integrations/ghost/`

---

## Reference Documentation

- Development Checklist: https://developers.home-assistant.io/docs/development_checklist/
- Integration Manifest: https://developers.home-assistant.io/docs/creating_integration_manifest/
- Quality Scale: https://developers.home-assistant.io/docs/core/integration-quality-scale/
- Quality Scale Checklist: https://developers.home-assistant.io/docs/core/integration-quality-scale/checklist/
- Style Guidelines: https://developers.home-assistant.io/docs/development_guidelines/
- Submitting Work: https://developers.home-assistant.io/docs/development_submitting/

---

## About the Integration

**Ghost** is an open-source publishing platform. This integration provides:
- Member count sensors (total, paid, free, comped)
- Revenue sensors (MRR, ARR)
- Content sensors (posts, comments)
- Email newsletter metrics
- ActivityPub/SocialWeb metrics
- Webhook events for real-time updates
- Full config flow with reauth and reconfigure support
- Diagnostics support

**Library:** `aioghost` (https://pypi.org/project/aioghost/) — async Python client for Ghost Admin API

**Quality Scale:** Platinum tier (all Bronze, Silver, Gold, and Platinum requirements met)
