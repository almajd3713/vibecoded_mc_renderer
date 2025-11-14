"""Pytest configuration and fixtures."""

import pytest
import json
import hashlib
from pathlib import Path
from typing import Generator
import urllib.request
import urllib.error

from vibecoded_mc_renderer.core.resource_manager import ResourceManager
from vibecoded_mc_renderer.core.model_loader import ModelLoader
from vibecoded_mc_renderer.core.texture_manager import TextureManager
from vibecoded_mc_renderer.core.renderer import BlockRenderer


# Minecraft 1.12.2 client jar information
MINECRAFT_VERSION = "1.12.2"
MINECRAFT_JAR_URL = "https://launcher.mojang.com/v1/objects/0f275bc1547d01fa5f56ba34bdc87d981ee12daf/client.jar"
MINECRAFT_JAR_SHA1 = "0f275bc1547d01fa5f56ba34bdc87d981ee12daf"


@pytest.fixture(scope="session")
def test_data_dir() -> Path:
    """Get or create the test data directory."""
    data_dir = Path(__file__).parent / "test_data"
    data_dir.mkdir(exist_ok=True)
    return data_dir


@pytest.fixture(scope="session")
def minecraft_jar(test_data_dir: Path) -> Path:
    """
    Download and cache the Minecraft 1.12.2 client jar.
    
    This fixture downloads the jar once per test session and caches it.
    """
    jar_path = test_data_dir / f"minecraft_{MINECRAFT_VERSION}.jar"
    
    # Check if jar already exists and is valid
    if jar_path.exists():
        # Verify SHA1 hash
        with open(jar_path, "rb") as f:
            jar_hash = hashlib.sha1(f.read()).hexdigest()
        
        if jar_hash == MINECRAFT_JAR_SHA1:
            print(f"\n✓ Using cached Minecraft {MINECRAFT_VERSION} jar: {jar_path}")
            return jar_path
        else:
            print(f"\n⚠ Cached jar has incorrect hash, re-downloading...")
            jar_path.unlink()
    
    # Download the jar
    print(f"\n⬇ Downloading Minecraft {MINECRAFT_VERSION} client jar...")
    print(f"  URL: {MINECRAFT_JAR_URL}")
    print(f"  Size: ~10 MB (this may take a moment)")
    
    try:
        urllib.request.urlretrieve(MINECRAFT_JAR_URL, jar_path)
        
        # Verify the download
        with open(jar_path, "rb") as f:
            jar_hash = hashlib.sha1(f.read()).hexdigest()
        
        if jar_hash != MINECRAFT_JAR_SHA1:
            jar_path.unlink()
            raise ValueError(
                f"Downloaded jar has incorrect SHA1 hash.\n"
                f"Expected: {MINECRAFT_JAR_SHA1}\n"
                f"Got: {jar_hash}"
            )
        
        print(f"✓ Successfully downloaded and verified Minecraft {MINECRAFT_VERSION} jar")
        return jar_path
        
    except urllib.error.URLError as e:
        pytest.skip(f"Could not download Minecraft jar: {e}")
    except Exception as e:
        if jar_path.exists():
            jar_path.unlink()
        pytest.skip(f"Error downloading Minecraft jar: {e}")


@pytest.fixture
def resource_manager(minecraft_jar: Path) -> Generator[ResourceManager, None, None]:
    """Create a ResourceManager with the Minecraft jar."""
    manager = ResourceManager([minecraft_jar])
    yield manager
    manager.close()


@pytest.fixture
def model_loader(resource_manager: ResourceManager) -> ModelLoader:
    """Create a ModelLoader with the resource manager."""
    return ModelLoader(resource_manager)


@pytest.fixture
def texture_manager(resource_manager: ResourceManager) -> TextureManager:
    """Create a TextureManager with the resource manager."""
    return TextureManager(resource_manager)


@pytest.fixture
def renderer(texture_manager: TextureManager) -> BlockRenderer:
    """Create a BlockRenderer with the texture manager."""
    return BlockRenderer(texture_manager)
