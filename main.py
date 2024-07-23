import os
import json
import zipfile
import uuid
from PIL import Image, ImageOps

class TotemCreator:

    @staticmethod
    def head(skin, uol):
        head = Image.new("RGBA", (8, 8))
        head.paste(skin.crop((9, 8, 15, 9)), (1, 0))
        head.paste(skin.crop((8, 9, 16, 16)), (0, 1))
        if uol:
            l21 = skin.crop((40, 8, 48, 9))
            l22 = skin.crop((40, 9, 48, 16))
            head.paste(l21, (0, 0), l21)
            head.paste(l22, (0, 1), l22)
        return head

    @staticmethod
    def body(skin, uol):
        body = Image.new("RGBA", (8, 4))
        body.paste(skin.crop((20, 21, 28, 22)), (0, 0))
        body.paste(skin.crop((20, 23, 28, 24)), (0, 1))
        body.paste(skin.crop((20, 29, 28, 30)), (0, 2))
        body.paste(skin.crop((20, 31, 28, 32)), (0, 3))
        if uol:
            l21 = skin.crop((20, 37, 28, 38))
            l22 = skin.crop((20, 39, 28, 40))
            l23 = skin.crop((20, 45, 28, 46))
            l24 = skin.crop((20, 47, 28, 48))
            body.paste(l21, (0, 0), l21)
            body.paste(l22, (0, 1), l22)
            body.paste(l23, (0, 2), l23)
            body.paste(l24, (0, 3), l24)
        return body

    @staticmethod
    def legs(skin, uol):
        legs = Image.new("RGBA", (6, 3))
        legs.paste(skin.crop((4, 20, 5, 22)), (0, 0))
        legs.paste(skin.crop((6, 20, 8, 22)), (1, 0))
        legs.paste(skin.crop((20, 52, 22, 54)), (3, 0))
        legs.paste(skin.crop((23, 52, 24, 54)), (5, 0))

        legs.paste(skin.crop((4, 31, 5, 32)), (1, 2))
        legs.paste(skin.crop((7, 31, 8, 32)), (2, 2))
        legs.paste(skin.crop((20, 63, 21, 64)), (3, 2))
        legs.paste(skin.crop((23, 63, 24, 64)), (4, 2))
        if uol:
            l21 = skin.crop((4, 36, 5, 38))
            l22 = skin.crop((6, 36, 8, 38))
            l23 = skin.crop((4, 52, 6, 54))
            l24 = skin.crop((7, 52, 8, 54))
            legs.paste(l21, (0, 0), l21)
            legs.paste(l22, (1, 0), l22)
            legs.paste(l23, (3, 0), l23)
            legs.paste(l24, (5, 0), l24)

            l25 = skin.crop((4, 47, 5, 48))
            l26 = skin.crop((7, 47, 8, 48))
            l27 = skin.crop((4, 63, 5, 64))
            l28 = skin.crop((7, 63, 8, 64))
            legs.paste(l25, (1, 2), l25)
            legs.paste(l26, (2, 2), l26)
            legs.paste(l27, (3, 2), l27)
            legs.paste(l28, (4, 2), l28)
        return legs

    @staticmethod
    def arms(skin, uol):
        arms = Image.new("RGBA", (14, 3))
        arms.paste(skin.crop((37, 52, 40, 54)).rotate(90, expand=True), (11, 0))
        arms.paste(skin.crop((44, 20, 47, 22)).rotate(-90, expand=True), (1, 0))
        arms.paste(skin.crop((39, 63, 40, 64)), (13, 0))
        arms.paste(skin.crop((36, 63, 37, 64)), (13, 1))
        arms.paste(skin.crop((44, 31, 45, 32)), (0, 0))
        arms.paste(skin.crop((47, 31, 48, 32)), (0, 1))
        if uol:
            l21 = skin.crop((53, 52, 56, 54)).rotate(90, expand=True)
            l22 = skin.crop((44, 36, 47, 38)).rotate(-90, expand=True)
            l23 = skin.crop((55, 63, 56, 64))
            l24 = skin.crop((52, 63, 53, 64))
            l25 = skin.crop((44, 47, 45, 48))
            l26 = skin.crop((47, 47, 48, 48))

            arms.paste(l21, (11, 0), l21)
            arms.paste(l22, (1, 0), l22)
            arms.paste(l23, (13, 0), l23)
            arms.paste(l24, (13, 1), l24)
            arms.paste(l25, (0, 0), l25)
            arms.paste(l26, (0, 1), l26)

        return arms

    def make_totem(self, user, uol=True):
        # Load the skin image
        skin = Image.open(user).convert("RGBA")

        # Create the individual parts
        torso = self.body(skin, uol)
        head = self.head(skin, uol)
        legs = self.legs(skin, uol)
        arms = self.arms(skin, uol)

        # Create the totem canvas
        canvas = Image.new("RGBA", (16, 16))

        # Paste the parts onto the canvas
        canvas.paste(arms, (1, 8))
        canvas.paste(legs, (5, 13))
        if skin.size[1] == 32:
            canvas.paste(ImageOps.mirror(canvas.crop((0, 0, 8, 16))), (8, 0))

        canvas.paste(torso, (4, 9))
        canvas.paste(head, (4, 1))

        return canvas

def create_mcpack(skin_path):
    # Create an instance of the TotemCreator class
    creator = TotemCreator()

    # Create the totem
    totem = creator.make_totem(skin_path)

    # Save the result
    totem_path = 'totem.png'
    totem.save(totem_path)
    totem.show()

    # Generate unique UUIDs for the texture pack
    texture_pack_uuid = str(uuid.uuid4())
    resource_pack_uuid = str(uuid.uuid4())

    # Create the directory structure for the texture pack
    pack_name = "TotemPack"
    os.makedirs(f"{pack_name}/textures/items", exist_ok=True)
    os.makedirs(f"{pack_name}/textures/icon", exist_ok=True)

    # Move the totem image to the textures folder
    os.rename(totem_path, f"{pack_name}/textures/items/totem.png")

    # Create the icon for the texture pack
    icon = totem.resize((256, 256), Image.NEAREST)
    icon.save(f"{pack_name}/pack_icon.png")

    # Create manifest.json
    manifest = {
        "format_version": 2,
        "header": {
            "description": "Custom Totem Texture Pack",
            "name": "Custom Totem By Luqidniy",
            "uuid": texture_pack_uuid,  # Unique UUID for the texture pack
            "version": [1, 0, 0],
            "min_engine_version": [1, 13, 0]  # Minimum Minecraft version
        },
        "modules": [
            {
                "description": "Custom Totem",
                "type": "resources",
                "uuid": resource_pack_uuid,  # Unique UUID for the resource module
                "version": [1, 0, 0]
            }
        ]
    }

    with open(f"{pack_name}/manifest.json", 'w') as f:
        json.dump(manifest, f, indent=4)

    # Create textures.json
    textures = {
        "texture_data": {
            "totem": {
                "textures": "textures/items/totem"
            }
        }
    }

    with open(f"{pack_name}/textures/textures.json", 'w') as f:
        json.dump(textures, f, indent=4)

    # Zip the pack
    zip_path = f"{pack_name}.mcpack"
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for root, dirs, files in os.walk(pack_name):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, pack_name))

    # Clean up
    for root, dirs, files in os.walk(pack_name, topdown=False):
        for file in files:
            os.remove(os.path.join(root, file))
        for dir in dirs:
            os.rmdir(os.path.join(root, dir))
    os.rmdir(pack_name)

    print(f"{zip_path} created successfully.")

# Path to the skin image
skin_path = 'skin.png'

# Create the .mcpack file
create_mcpack(skin_path)
