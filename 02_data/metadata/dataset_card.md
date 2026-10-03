# 📊 Dataset Card: Phishing Email Dataset

| Field | Value |
|-------|-------|
| **Name** | Phishing Email Dataset |
| **Source** | [Cần bổ sung: Kaggle URL hoặc nguồn gốc] |
| **Size** | ~52 MB |
| **Format** | CSV |
| **Rows** | [Cần bổ sung: số dòng] |
| **Columns** | `Email Text`, `Email Type` (0=Safe, 1=Phishing) |
| **Class Balance** | [Cần bổ sung: tỷ lệ phishing/safe] |
| **Language** | English |
| **License** | [Cần bổ sung] |

## Preprocessing Notes

- Tokenized using `distilbert-base-uncased` tokenizer
- Max sequence length: 512 tokens
- Partitioned using Dirichlet distribution (α configurable)
- Non-IID partitioning across 4 FL clients

## Known Issues

- [Cần bổ sung: missing values, encoding issues, etc.]
