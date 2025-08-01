# NLP (Natural Language Processing) With Translator <img height="32" src="https://docs.python.org/3/_static/py.svg" alt="Python">

- Service untuk Sentiment Analysis.
- Analisis menggunakan bahasa inggris.
- Disediakan fungsi translator untuk bahasa yang lain.

## Docker
```bash
# BUILD
docker buildx build --no-cache -t nlp-with-translator . -f dockerfile

# RUN
docker run -d --name nlp-with-translator -p 5001:80 nlp-with-translator
```

## API
Parameter:
* `translate` (_Optional_) flag untuk melakukan penerjemahan atau tidak (default: `false`). Bahasa yang akan diproses adalah bahasa Inggris.
* `from` (_Optional_) kode bahasa input (default: `auto`).
* `to` (_Optional_) kode bahasa output (default: `auto`).
* `text` (_Mandatory_) teks yang akan dianalisa sentimennya. Jika berbahasa inggris parameter `translate` di-_set_ `false`.
> Kode bahasa bisa dilihat di [Google](https://translate.google.com/)

### Translate (/Translate)
```json
# REQUEST
{
    "translate": true,
    "to": "ko",
    "text": "Di tengah gaya hidup modern Indonesia, di mana teknologi menjadi bagian tak terpisahkan dari keseharian, kebutuhan akan kebersihan gigi yang optimal mendorong meningkatnya popularitas sikat gigi elektrik."
}

# RESPONSE
{
    "translate": true,
    "to": "ko",
    "text": "Di tengah gaya hidup modern Indonesia, di mana teknologi menjadi bagian tak terpisahkan dari keseharian, kebutuhan akan kebersihan gigi yang optimal mendorong meningkatnya popularitas sikat gigi elektrik.",
    "result": "기술이 일상 생활에서 떼려야 뗄 수 없는 부분이 된 인도네시아의 현대적인 라이프스타일 속에서 최적의 치아 위생에 대한 요구로 인해 전동 칫솔의 인기가 높아지고 있습니다."
}
```

### VaderStandard (/VaderStandard)
```json
# REQUEST
{
    "translate": true,
    "text": "Di tengah gaya hidup modern Indonesia, di mana teknologi menjadi bagian tak terpisahkan dari keseharian, kebutuhan akan kebersihan gigi yang optimal mendorong meningkatnya popularitas sikat gigi elektrik."
}

# RESPONSE
{
    "translate": true,
    "text": "Di tengah gaya hidup modern Indonesia, di mana teknologi menjadi bagian tak terpisahkan dari keseharian, kebutuhan akan kebersihan gigi yang optimal mendorong meningkatnya popularitas sikat gigi elektrik.",
    "positive": 0.162,
    "negative": 0.0,
    "neutral": 0.838,
    "compound": 0.6808
}
```

### VaderFinancial (/VaderFinancial)
Analisa sentimen untuk bidang ekonomi dan finansial.
```json
# REQUEST
{
    "translate": true,
    "text": "Di tengah gaya hidup modern Indonesia, di mana teknologi menjadi bagian tak terpisahkan dari keseharian, kebutuhan akan kebersihan gigi yang optimal mendorong meningkatnya popularitas sikat gigi elektrik."
}

# RESPONSE
{
    "translate": true,
    "text": "Di tengah gaya hidup modern Indonesia, di mana teknologi menjadi bagian tak terpisahkan dari keseharian, kebutuhan akan kebersihan gigi yang optimal mendorong meningkatnya popularitas sikat gigi elektrik.",
    "positive": 0.204,
    "negative": 0.0,
    "neutral": 0.796,
    "compound": 0.397
}
```

### NaiveBayes (/NaiveBayes)
```json
# REQUEST
{
    "translate": true,
    "text": "Di tengah gaya hidup modern Indonesia, di mana teknologi menjadi bagian tak terpisahkan dari keseharian, kebutuhan akan kebersihan gigi yang optimal mendorong meningkatnya popularitas sikat gigi elektrik."
}

# RESPONSE
{
    "translate": true,
    "text": "Di tengah gaya hidup modern Indonesia, di mana teknologi menjadi bagian tak terpisahkan dari keseharian, kebutuhan akan kebersihan gigi yang optimal mendorong meningkatnya popularitas sikat gigi elektrik.",
    "positive": 0.99787645,
    "negative": 0.00212355
}
```

### TextBlob (/TextBlob)
```json
# REQUEST
{
    "translate": true,
    "text": "Di tengah gaya hidup modern Indonesia, di mana teknologi menjadi bagian tak terpisahkan dari keseharian, kebutuhan akan kebersihan gigi yang optimal mendorong meningkatnya popularitas sikat gigi elektrik."
}

# RESPONSE
{
    "translate": true,
    "text": "Di tengah gaya hidup modern Indonesia, di mana teknologi menjadi bagian tak terpisahkan dari keseharian, kebutuhan akan kebersihan gigi yang optimal mendorong meningkatnya popularitas sikat gigi elektrik.",
    "polarity": 0.0,
    "subjectivity": 0.45
}
```

## Documentation
- [Vader](https://hex.tech/use-cases/sentiment-analysis/vader-sentiment-analysis/)
- [NaiveBayes](https://medium.com/@zubairashfaque/sentiment-analysis-with-naive-bayes-algorithm-a31021764fb4)
- [TextBlob](https://textblob.readthedocs.io/en/dev/)