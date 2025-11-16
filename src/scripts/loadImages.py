import subprocess

# Define "vial" as a variable
lista = ["vial", "hidrico", "electrico"]
base_path = "./resources/ejemplo"


def main():
    print("Starting image generation...")

    # Execute the command 3 times
    for el in lista:
        subprocess.run(
            [
                "dot",
                "-Tpng",
                f"{base_path}/{el}.dot",
                "-o",
                f"{base_path}/imgs/{el}.png",
            ]
        )

    print("Success!")


if __name__ == "__main__":
    main()
