To run the whole thing, the most complete command is:


```python
scrapy runspider spider_native.py -o november_2024.jsonl
scrapy runspider spider_zaginieni.py -o november_2024_zag.jsonl 
# Copy them together into first file
python classify_gender_names.py november_2024.jsonl 
```

final file should be: november_2024_gendered.jsonl 