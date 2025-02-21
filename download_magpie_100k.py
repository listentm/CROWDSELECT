from datasets import load_dataset
import pdb
proxies={
    "http":"http://127.0.0.1:7891",
    "https":"http://127.0.0.1:7891"
}
ds = load_dataset("Magpie-Align/Magpie-100K-Generator-Zoo",cache_dir='./magpie_100k')
pdb.set_trace()