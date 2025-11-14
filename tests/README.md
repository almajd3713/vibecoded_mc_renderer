# Tests

This directory contains tests for the VibeCoded Minecraft Renderer.

## Automatic Minecraft Jar Download

The tests automatically download Minecraft 1.12.2 client jar when first run. This is handled by the `minecraft_jar` fixture in `conftest.py`.

### What Happens on First Run

1. **Download**: The test suite downloads the Minecraft 1.12.2 client jar (~10 MB) from Mojang's official servers
2. **Verification**: The downloaded jar is verified using SHA1 hash to ensure integrity
3. **Caching**: The jar is cached in `tests/test_data/` for future test runs
4. **Reuse**: Subsequent test runs use the cached jar

### Jar Information

- **Version**: 1.12.2
- **Source**: Official Mojang launcher servers
- **Size**: ~10 MB
- **SHA1**: `0f275bc1547d01fa5f56ba34bdc87d981ee12daf`
- **Cache Location**: `tests/test_data/minecraft_1.12.2.jar`

## Running Tests

### Install Dependencies

First, install the package with dev dependencies:

```bash
pip install -e ".[dev]"
```

Or using requirements files:

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Run All Tests

```bash
pytest
```

On first run, you'll see:

```
⬇ Downloading Minecraft 1.12.2 client jar...
  URL: https://launcher.mojang.com/v1/objects/...
  Size: ~10 MB (this may take a moment)
✓ Successfully downloaded and verified Minecraft 1.12.2 jar
```

Subsequent runs will show:

```
✓ Using cached Minecraft 1.12.2 jar: tests/test_data/minecraft_1.12.2.jar
```

### Run with Coverage

```bash
pytest --cov=vibecoded_mc_renderer
```

### Run Specific Test Files

```bash
# Unit tests only
pytest tests/test_resource_location.py

# Integration tests only
pytest tests/test_integration.py
```

### Run Specific Tests

```bash
pytest tests/test_integration.py::TestBlockRenderer::test_render_stone_block
```

### Verbose Output

```bash
pytest -v
```

## Test Structure

### `conftest.py`
- Pytest configuration and fixtures
- Automatic Minecraft jar download and caching
- Fixture for ResourceManager, ModelLoader, TextureManager, BlockRenderer

### `test_resource_location.py`
- Unit tests for ResourceLocation utility class
- No Minecraft jar required

### `test_integration.py`
- Integration tests using the actual Minecraft jar
- Tests ResourceManager, ModelLoader, TextureManager, BlockRenderer
- End-to-end rendering tests

## Fixtures Available

When writing tests, you can use these fixtures:

```python
def test_something(minecraft_jar, resource_manager, model_loader, texture_manager, renderer):
    """All fixtures are automatically available."""
    # minecraft_jar: Path to the cached Minecraft jar
    # resource_manager: Initialized ResourceManager
    # model_loader: Initialized ModelLoader
    # texture_manager: Initialized TextureManager
    # renderer: Initialized BlockRenderer
```

## Network Requirements

The first test run requires an internet connection to download the Minecraft jar. After that, tests can run offline using the cached jar.

If the download fails, tests will be skipped with a clear message.

## Cleaning Test Data

To force re-download of the Minecraft jar:

```bash
# Windows
Remove-Item -Recurse tests\test_data

# Linux/Mac
rm -rf tests/test_data
```

The jar will be re-downloaded on the next test run.

## Troubleshooting

### Download Fails

If the download fails, you can manually download the jar:

1. Download from: https://launcher.mojang.com/v1/objects/0f275bc1547d01fa5f56ba34bdc87d981ee12daf/client.jar
2. Save as: `tests/test_data/minecraft_1.12.2.jar`
3. Run tests again

### Hash Verification Fails

If the cached jar has an incorrect hash, it will be automatically re-downloaded.

### Tests Skip Due to Network Error

The tests will gracefully skip if the jar cannot be downloaded. Ensure you have:
- Active internet connection (first run only)
- Access to launcher.mojang.com
- No firewall blocking the download

## Writing New Tests

Example test using fixtures:

```python
def test_render_custom_block(model_loader, renderer, tmp_path):
    """Test rendering a custom block."""
    model = model_loader.get_model_for_block("minecraft:diamond_block")
    assert model is not None
    
    image = renderer.render_block(model, "minecraft:diamond_block", output_size=128)
    assert image is not None
    
    # Save to temporary directory
    output_file = tmp_path / "diamond.png"
    image.save(output_file)
    assert output_file.exists()
```

## CI/CD Considerations

For continuous integration:

1. **Caching**: Cache the `tests/test_data/` directory to avoid re-downloading
2. **Timeout**: First run may take 1-2 minutes to download
3. **Disk Space**: Ensure ~15 MB free space for the jar
4. **Network**: CI environment needs internet access

Example GitHub Actions cache:

```yaml
- name: Cache test data
  uses: actions/cache@v3
  with:
    path: tests/test_data
    key: minecraft-jar-1.12.2
```
