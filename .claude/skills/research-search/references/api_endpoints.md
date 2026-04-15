# API Endpoints Reference

This file contains the URL templates, parameter formats, and response parsing guidance for each academic database API used by `research-search`. Read this before making your first API call.

## Table of Contents

1. [Semantic Scholar](#semantic-scholar)
2. [OpenAlex](#openalex)
3. [PubMed E-utilities](#pubmed-e-utilities)
4. [arXiv](#arxiv)

---

## Semantic Scholar

**Base URL:** `https://api.semanticscholar.org/graph/v1`

### Paper Search

```
GET /paper/search?query={query}&fields={fields}&limit=30&year={start}-{end}
```

**Parameters:**
- `query`: URL-encoded search string
- `fields`: Comma-separated list of fields to return
- `limit`: Max results (up to 100, use 30)
- `year`: Year range filter, format `YYYY-YYYY` (e.g., `2019-2026`)
- `offset`: For pagination (default 0)

**Recommended fields:**
```
title,authors,year,abstract,externalIds,citationCount,journal,url,references,citations
```

**Example:**
```
https://api.semanticscholar.org/graph/v1/paper/search?query=EEG+neurofeedback+cognitive+training&fields=title,authors,year,abstract,externalIds,citationCount,journal,url&limit=30&year=2019-2026
```

**Response structure:**
```json
{
  "total": 1234,
  "offset": 0,
  "data": [
    {
      "paperId": "abc123def456",
      "title": "Paper Title",
      "authors": [{"authorId": "123", "name": "Author Name"}],
      "year": 2024,
      "abstract": "...",
      "externalIds": {
        "DOI": "10.1234/example",
        "ArXiv": "2401.12345",
        "PubMed": "12345678",
        "CorpusId": 987654
      },
      "citationCount": 42,
      "journal": {"name": "Journal Name"},
      "url": "https://www.semanticscholar.org/paper/abc123"
    }
  ]
}
```

**Field mapping:**
- `paperId` → `semantic_scholar_id`
- `externalIds.DOI` → `doi`
- `externalIds.ArXiv` → `arxiv_id`
- `externalIds.PubMed` → `pubmed_id`
- `authors[].name` → `authors[]`
- `journal.name` → `journal`

### Paper References (for snowball)

```
GET /paper/{paper_id}/references?fields=title,authors,year,abstract,externalIds,citationCount&limit=50
```

Where `{paper_id}` can be the Semantic Scholar paperId, DOI (prefixed with `DOI:`), or arXiv ID (prefixed with `ARXIV:`).

**Response structure:**
```json
{
  "data": [
    {
      "citedPaper": {
        "paperId": "...",
        "title": "...",
        "authors": [...],
        "year": 2023,
        "abstract": "...",
        "externalIds": {...},
        "citationCount": 15
      }
    }
  ]
}
```

### Paper Citations (for citation network)

```
GET /paper/{paper_id}/citations?fields=title,authors,year,externalIds&limit=50
```

Same structure as references but with `citingPaper` instead of `citedPaper`.

### Rate Limits

- Without API key: ~100 requests per 5 minutes
- With API key: 1 request/second sustained
- If you get 429 (Too Many Requests), wait 30 seconds before retrying

---

## OpenAlex

**Base URL:** `https://api.openalex.org`

### Works Search

```
GET /works?search={query}&filter=from_publication_date:{start}&per_page=30&mailto={email}
```

**Parameters:**
- `search`: URL-encoded search string
- `filter`: Comma-separated filters
  - `from_publication_date:YYYY-MM-DD` — papers published after this date
  - `to_publication_date:YYYY-MM-DD` — papers published before this date
  - `type:journal-article` — filter to journal articles only (optional)
- `per_page`: Results per page (max 200, use 30)
- `sort`: Sort order, e.g., `cited_by_count:desc`
- `mailto`: Your email (gets you into the polite pool with higher rate limits)

**Example:**
```
https://api.openalex.org/works?search=EEG+neurofeedback+cognitive+training+elderly&filter=from_publication_date:2019-01-01&per_page=30&sort=cited_by_count:desc
```

**Response structure:**
```json
{
  "meta": {"count": 456, "per_page": 30, "page": 1},
  "results": [
    {
      "id": "https://openalex.org/W1234567890",
      "doi": "https://doi.org/10.1234/example",
      "title": "Paper Title",
      "publication_year": 2024,
      "authorships": [
        {
          "author": {"display_name": "Author Name", "id": "..."},
          "institutions": [...]
        }
      ],
      "primary_location": {
        "source": {"display_name": "Journal Name"}
      },
      "abstract_inverted_index": {...},
      "cited_by_count": 42,
      "referenced_works": ["https://openalex.org/W111", "https://openalex.org/W222"],
      "ids": {
        "openalex": "https://openalex.org/W1234567890",
        "doi": "https://doi.org/10.1234/example",
        "pmid": "https://pubmed.ncbi.nlm.nih.gov/12345678"
      }
    }
  ]
}
```

**Field mapping:**
- `id` → `openalex_id` (extract the W-number, e.g., "W1234567890")
- `doi` → `doi` (strip `https://doi.org/` prefix)
- `publication_year` → `year`
- `authorships[].author.display_name` → `authors[]`
- `primary_location.source.display_name` → `journal`
- `cited_by_count` → `citation_count`
- `referenced_works` → useful for citation network (cross-reference with other OpenAlex IDs in collection)

**Abstract reconstruction:** OpenAlex stores abstracts as an inverted index. To reconstruct:
```python
# The inverted index maps words to their positions
# {"This": [0], "is": [1], "an": [2], "abstract": [3]}
# Reconstruct by sorting positions and joining words
```
When using WebFetch, the abstract may need reconstruction. If the inverted index is too complex to reconstruct inline, note it and rely on Semantic Scholar for the abstract.

### Rate Limits

- Without `mailto`: 10 requests/second
- With `mailto` parameter: 100 requests/second (polite pool)
- Very generous — unlikely to hit limits

---

## PubMed E-utilities

**Base URL:** `https://eutils.ncbi.nlm.nih.gov/entrez/eutils`

PubMed uses a two-step process: search (get IDs) then fetch (get details).

### Step 1: ESearch (get PMIDs)

```
GET /esearch.fcgi?db=pubmed&term={query}&retmax=30&retmode=json&mindate={YYYY}&maxdate={YYYY}&datetype=pdat
```

**Parameters:**
- `db`: Always `pubmed`
- `term`: URL-encoded search string (supports MeSH terms and Boolean operators)
- `retmax`: Max results (use 30)
- `retmode`: `json` for JSON response
- `mindate` / `maxdate`: Publication date range (YYYY format)
- `datetype`: `pdat` for publication date

**Example:**
```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=neurofeedback+EEG+elderly+cognitive&retmax=30&retmode=json&mindate=2019&maxdate=2026&datetype=pdat
```

**Response:**
```json
{
  "esearchresult": {
    "count": "156",
    "retmax": "30",
    "idlist": ["39123456", "39012345", "38901234", ...]
  }
}
```

### Step 2: EFetch (get paper details)

```
GET /efetch.fcgi?db=pubmed&id={id1},{id2},{id3}&retmode=xml
```

Fetch up to 200 IDs at once (comma-separated). Use `retmode=xml` — PubMed's XML has the richest metadata.

**Example:**
```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=39123456,39012345,38901234&retmode=xml
```

**Response (XML) — key fields:**
```xml
<PubmedArticle>
  <MedlineCitation>
    <PMID>39123456</PMID>
    <Article>
      <ArticleTitle>Paper Title</ArticleTitle>
      <Abstract><AbstractText>Full abstract...</AbstractText></Abstract>
      <AuthorList>
        <Author><LastName>Smith</LastName><ForeName>John</ForeName></Author>
      </AuthorList>
      <Journal>
        <Title>Journal of Neuroscience</Title>
      </Journal>
      <ArticleDate><Year>2024</Year></ArticleDate>
    </Article>
  </MedlineCitation>
  <PubmedData>
    <ArticleIdList>
      <ArticleId IdType="doi">10.1234/example</ArticleId>
      <ArticleId IdType="pmc">PMC1234567</ArticleId>
    </ArticleIdList>
  </PubmedData>
</PubmedArticle>
```

**Field mapping:**
- `PMID` → `pubmed_id`
- `ArticleTitle` → `title`
- `AuthorList/Author` → `authors[]` (format: "FirstName LastName")
- `ArticleDate/Year` → `year`
- `Journal/Title` → `journal`
- `ArticleId[IdType=doi]` → `doi`
- `AbstractText` → `abstract`
- PubMed does not provide citation counts — rely on Semantic Scholar or OpenAlex for that

### Rate Limits

- Without API key: 3 requests/second
- With API key (NCBI_API_KEY): 10 requests/second
- Batch your EFetch calls (up to 200 IDs per request) to minimize calls

---

## arXiv

**Base URL:** `https://export.arxiv.org/api`

### Query Search

```
GET /query?search_query={query}&start=0&max_results=30&sortBy=relevance&sortOrder=descending
```

**Parameters:**
- `search_query`: Search expression using arXiv query syntax
  - `all:{terms}` — search all fields
  - `ti:{terms}` — title only
  - `abs:{terms}` — abstract only
  - `cat:{category}` — category filter (e.g., `cs.AI`, `q-bio.NC`)
  - Combine with `AND`, `OR`, `ANDNOT`
- `start`: Offset for pagination
- `max_results`: Max results (up to 30000, use 30)
- `sortBy`: `relevance`, `lastUpdatedDate`, or `submittedDate`

**Example:**
```
https://export.arxiv.org/api/query?search_query=all:EEG+AND+all:neurofeedback+AND+all:cognitive+training&start=0&max_results=30&sortBy=relevance
```

**Response (Atom XML):**
```xml
<feed>
  <entry>
    <id>http://arxiv.org/abs/2401.12345v1</id>
    <title>Paper Title</title>
    <summary>Abstract text...</summary>
    <published>2024-01-15T00:00:00Z</published>
    <author><name>Author Name</name></author>
    <arxiv:doi>10.1234/example</arxiv:doi>
    <link href="http://arxiv.org/abs/2401.12345v1" rel="alternate"/>
    <link href="http://arxiv.org/pdf/2401.12345v1" rel="related" title="pdf"/>
    <arxiv:primary_category term="cs.AI"/>
  </entry>
</feed>
```

**Field mapping:**
- Extract arXiv ID from `<id>` tag: `http://arxiv.org/abs/2401.12345v1` → `2401.12345`
- `<title>` → `title` (strip newlines)
- `<summary>` → `abstract` (strip newlines)
- `<published>` → `year` (extract year)
- `<author><name>` → `authors[]`
- `<arxiv:doi>` → `doi` (if present)
- `<arxiv:primary_category term>` → useful for field classification
- arXiv does not provide citation counts — use Semantic Scholar for that

### Rate Limits

- arXiv API is slow and rate-limited: ~1 request every 3 seconds
- You'll typically make only 5 calls (one per query), so this is manageable

### Year Filtering

arXiv API doesn't have a built-in year filter parameter. To filter by date, add a date range to the query:
```
search_query=all:EEG+AND+all:neurofeedback+AND+submittedDate:[202001010000+TO+202612310000]
```

Or simply filter results by year after fetching.
