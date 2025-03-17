To run the whole thing, the most complete command is:


```python
scrapy runspider spider_zaginieni.py -o data/maart_2025_zag.jsonl 
scrapy runspider spider_native.py -o data/maart_2025.jsonl
scrapy runspider spider_interpol.py -o data/maart_2025_int.jsonl
# Copy them together into first file, like so:
#cat jan29_2025_zag.jsonl >> jan29_full.jsonl
#cat jan29_2025_int.jsonl >> jan29_full.jsonl
#cat jan29_2025.jsonl >> jan29_full.jsonl
python classify_gender_names.py maart_2025.jsonl 
```

final file should be: jan29_2025_gendered.jsonl 