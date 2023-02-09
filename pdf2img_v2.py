import pypdfium2 as pdfium
import os
import shutil
from tqdm import trange

def process(in_path, out_path):
    # remove tmp file
    if os.path.exists("in/in.tmp"):
        os.remove("in/in.tmp")
    shutil.copy(in_path, "in/in.tmp")
    print("正在转换 " + in_path)
    with pdfium.PdfDocument("in/in.tmp") as pdf:
        n_pages = len(pdf)
        for page_number in trange(n_pages):
            page = pdf.get_page(page_number)
            pil_image = page.render_topil(scale=300/72)
            pil_image.save(os.path.join(out_path, f"{page_number+1}.png"))
    print("已输出至 " + out_path)

if not os.path.exists("in"):
    os.makedirs("in")
    print("未找到输入文件夹，已创建，请将待转换的PDF一并放入in文件夹中，然后按回车键继续")
    input()
if not os.path.exists("out"):
    os.makedirs("out")

files = []
for file in os.listdir("in"):
    if file.endswith(".pdf"):
        files.append(os.path.join("in", file))

if len(files) == 0:
    print("输入文件夹in为空，退出")
    exit()

out_counter = 0
for file in files:
    while os.path.exists(os.path.join("out", str(out_counter))):
        out_counter += 1
    os.makedirs(os.path.join("out", str(out_counter)))
    process(file, os.path.join("out", str(out_counter)))
print("已完成，按回车键退出")
input()

