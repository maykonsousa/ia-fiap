"""Monta o dataset da Fase 6 (vaca x laranja) com imagens do COCO 2017.

Uso:
    python scripts/baixar_imagens.py <pasta_com_instances_*.json>

As 80 imagens (IDs abaixo) foram pré-filtradas no COCO (1 a 3 objetos da classe, objeto principal
ocupando de 8% a 70% da foto, sem a outra classe na cena) e escolhidas visualmente pelo grupo.
Cada classe é embaralhada com seed fixa e dividida 32/4/4 em dataset/images/{train,val,test};
a origem e a licença de cada foto vão para dataset/fontes.csv.
"""
import csv
import json
import random
import sys
import urllib.request
from pathlib import Path

IDS = {
    "vaca": [3321, 11169, 24480, 35242, 43371, 67680, 77408, 88987, 108920, 111945, 118594, 124636, 151757,
             191947, 193707, 223005, 224182, 287062, 292998, 296030, 303127, 347445, 357860, 358741, 375869,
             393686, 440097, 447113, 457100, 471278, 484341, 493407, 514387, 529645, 537695, 554691, 560789,
             568654, 576075, 578493],
    "laranja": [16161, 20882, 36255, 69535, 87018, 87620, 97883, 102811, 108862, 120491, 130088, 134288, 136881,
                138115, 144430, 150324, 166557, 170238, 198195, 221911, 235532, 253890, 255194, 305832, 358624,
                377611, 402170, 408543, 411750, 414108, 457703, 468623, 494550, 497335, 500228, 510596, 521352,
                533261, 563730, 574796],
}
SPLITS = [("train", 32), ("val", 4), ("test", 4)]

ann_dir = Path(sys.argv[1])
out = Path(__file__).resolve().parent.parent / "dataset"

# Metadados (arquivo, licença) das imagens escolhidas
images = {}
for split in ("val2017", "train2017"):
    data = json.loads((ann_dir / f"instances_{split}.json").read_text())
    lic = {l["id"]: l["name"] for l in data["licenses"]}
    for img in data["images"]:
        images[img["id"]] = {**img, "split": split, "license_name": lic[img["license"]]}

rows = []
for nome, ids in IDS.items():
    ids = sorted(ids)
    random.Random(42).shuffle(ids)
    n = 0
    for split, qtd in SPLITS:
        dest = out / "images" / split
        dest.mkdir(parents=True, exist_ok=True)
        for img_id in ids[n:n + qtd]:
            img = images[img_id]
            n += 1
            arquivo = f"{nome}_{n:02d}.jpg"
            url = f"http://images.cocodataset.org/{img['split']}/{img['file_name']}"
            urllib.request.urlretrieve(url, dest / arquivo)
            rows.append([arquivo, split, nome, img_id, url, img["flickr_url"], img["license_name"]])

with open(out / "fontes.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["arquivo", "split", "classe", "coco_id", "url_coco", "url_flickr", "licenca"])
    w.writerows(rows)
print(f"{len(rows)} imagens em {out}")
