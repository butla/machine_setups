from pathlib import Path

telefon_on_pc = Path("/data/zdjęcia_i_filmiki/telefon/")
phone_photos = Path("/home/butla/note_10_camera/")

telefon_on_pc_files = set(p.name for p in telefon_on_pc.iterdir())
phone_photos_files = set(p.name for p in phone_photos.iterdir())

print(len(telefon_on_pc_files))
print(len(phone_photos_files))

print(telefon_on_pc_files - phone_photos_files)
