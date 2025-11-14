"""Example script for rendering a stone block."""

from pathlib import Path
from vibecoded_mc_renderer.core.resource_manager import ResourceManager
from vibecoded_mc_renderer.core.model_loader import ModelLoader
from vibecoded_mc_renderer.core.texture_manager import TextureManager
from vibecoded_mc_renderer.core.renderer import BlockRenderer


def main():
    """Render a stone block from a Minecraft jar."""
    # Path to your Minecraft jar file
    jar_path = Path("path/to/minecraft.jar")

    if not jar_path.exists():
        print(f"Error: Jar file not found at {jar_path}")
        print("Please update the jar_path in this script to point to your Minecraft jar.")
        return

    # Create resource manager
    with ResourceManager([jar_path]) as resource_manager:
        # Create model loader and texture manager
        model_loader = ModelLoader(resource_manager)
        texture_manager = TextureManager(resource_manager)
        renderer = BlockRenderer(texture_manager)

        # Load and render stone block
        print("Loading stone block model...")
        model = model_loader.get_model_for_block("minecraft:stone")

        if model:
            print("Rendering stone block...")
            image = renderer.render_block(model, "minecraft:stone", output_size=256)
            image.save("stone_block.png")
            print("✓ Saved to stone_block.png")
        else:
            print("Error: Could not load stone block model")


if __name__ == "__main__":
    main()
