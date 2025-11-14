"""Example script for batch rendering blocks."""

from pathlib import Path
from vibecoded_mc_renderer.core.resource_manager import ResourceManager
from vibecoded_mc_renderer.core.model_loader import ModelLoader
from vibecoded_mc_renderer.core.texture_manager import TextureManager
from vibecoded_mc_renderer.core.renderer import BlockRenderer


def main():
    """Render multiple Minecraft blocks."""
    # Path to your Minecraft jar file
    jar_path = Path("path/to/minecraft.jar")

    if not jar_path.exists():
        print(f"Error: Jar file not found at {jar_path}")
        print("Please update the jar_path in this script to point to your Minecraft jar.")
        return

    # Blocks to render
    blocks_to_render = [
        "minecraft:stone",
        "minecraft:dirt",
        "minecraft:grass_block",
        "minecraft:cobblestone",
        "minecraft:oak_planks",
        "minecraft:glass",
    ]

    # Create output directory
    output_dir = Path("rendered_blocks")
    output_dir.mkdir(exist_ok=True)

    # Create resource manager and renderer
    with ResourceManager([jar_path]) as resource_manager:
        model_loader = ModelLoader(resource_manager)
        texture_manager = TextureManager(resource_manager)
        renderer = BlockRenderer(texture_manager)

        print(f"Rendering {len(blocks_to_render)} blocks...")

        for block_id in blocks_to_render:
            print(f"  Rendering {block_id}...", end=" ")

            try:
                model = model_loader.get_model_for_block(block_id)
                if model:
                    image = renderer.render_block(model, block_id, output_size=128)
                    filename = block_id.replace(":", "_") + ".png"
                    image.save(output_dir / filename)
                    print("✓")
                else:
                    print("✗ (model not found)")
            except Exception as e:
                print(f"✗ ({e})")

        print(f"\nRendered blocks saved to {output_dir}/")


if __name__ == "__main__":
    main()
