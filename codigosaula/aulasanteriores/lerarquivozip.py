import zipfile

zip_file_path = "./agoravai.zip"
with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
    for file_name in zip_ref.namelist():
        with zip_ref.open(file_name) as file:
            for line in file:
                print(line.decode("utf-8", "replace").strip())
