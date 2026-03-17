# Peasy 5-Language Package Expansion — Design Spec

> **Date**: 2026-03-17
> **Scope**: Expand 8 Peasy functional packages to 5 languages (Python, TypeScript, Rust, Ruby, Go)
> **Reference**: AgentGIF 5-language pattern, CITED Health Phase G, BarcodeFYI Gold Standard
> **Rule**: 절대로 Claude API를 사용하지 않는다

---

## 1. Problem Statement

Peasy has 8 functional packages covering PDF, Image, Text, CSS, Compress, Document, Audio, and Video. Currently:

| Language | Packages | Status |
|----------|----------|--------|
| Python (PyPI) | 8 | ✅ Complete (engine + API client + CLI + MCP) |
| TypeScript (npm) | 8 | ⚠️ Engine-only (no API client) |
| Rust (crates.io) | 8 | 🔴 Minimal stubs (version() + error types) |
| Ruby (rubygems) | 8 | ⚠️ Mixed (some engines, no API client) |
| Go (pkg.go.dev) | 0 | 🔴 Not started |

**Goal**: Bring all 40 packages (8 × 5 languages) to production quality with:
1. **API client** for peasytools.com DRF API (all languages)
2. **Glossary & Guide search** functionality (all languages)
3. **Engine functions** where language ecosystem supports it
4. **SEO-optimized READMEs** with peasytools.com backlinks
5. **PUBLIC GitHub repos** (currently all PRIVATE)

---

## 2. Package Matrix (40 packages)

| Package | Python | TypeScript | Rust | Ruby | Go |
|---------|--------|------------|------|------|----|
| peasy-pdf | `peasy-pdf` | `peasy-pdf-js` | `peasy-pdf-rs` | `peasy-pdf-rb` | `peasy-pdf-go` |
| peasy-image | `peasy-image` | `peasy-image-js` | `peasy-image-rs` | `peasy-image-rb` | `peasy-image-go` |
| peasy-audio | `peasy-audio` | `peasy-audio-js` | `peasy-audio-rs` | `peasy-audio-rb` | `peasy-audio-go` |
| peasy-video | `peasy-video` | `peasy-video-js` | `peasy-video-rs` | `peasy-video-rb` | `peasy-video-go` |
| peasy-css | `peasy-css` | `peasy-css-js` | `peasy-css-rs` | `peasy-css-rb` | `peasy-css-go` |
| peasy-compress | `peasy-compress` | `peasy-compress-js` | `peasy-compress-rs` | `peasy-compress-rb` | `peasy-compress-go` |
| peasy-document | `peasy-document` | `peasy-document-js` | `peasy-document-rs` | `peasy-document-rb` | `peasy-document-go` |
| peasytext | `peasytext` | `peasytext-js` | `peasytext-rs` | `peasytext-rb` | `peasytext-go` |

> **Naming note**: `peasytext` is the only package without a hyphen. It was published before the `peasy-*` naming convention was established. All registries and repos use this form consistently.

**Registry names** (no language suffix on registries):

| Registry | Name Format | Example |
|----------|-------------|---------|
| PyPI | `peasy-pdf` | `pip install peasy-pdf` |
| npm | `peasy-pdf` | `npm install peasy-pdf` |
| crates.io | `peasy-pdf` | `cargo add peasy-pdf` |
| rubygems | `peasy-pdf` | `gem install peasy-pdf` |
| pkg.go.dev | `github.com/peasytools/peasy-pdf-go` | `go get github.com/peasytools/peasy-pdf-go` |

**GitHub org**: `peasytools` (not `fyipedia`)

**Current publication status**:

| Registry | Published | Status |
|----------|-----------|--------|
| PyPI | 8/8 | ✅ All published at v0.1.1 |
| npm | 8/8 | ✅ All published at v0.1.1 (bare names, no org scope) |
| crates.io | 8/8 | ✅ All published at v0.1.1 |
| rubygems | 8/8 | ✅ All published at v0.1.1 |
| Go (pkg.go.dev) | 0/8 | 🔴 Repos don't exist yet |

---

## 3. Architecture Per Language

### 3.1 Dual-Layer Design

Every package has two independent layers:

```
┌─────────────────────────────────────────┐
│  Layer 1: ENGINE (local operations)     │
│  - Language-native file processing      │
│  - Zero or minimal dependencies         │
│  - Works offline                        │
├─────────────────────────────────────────┤
│  Layer 2: API CLIENT (REST wrapper)     │
│  - Wraps peasytools.com DRF API         │
│  - Browse tools, formats, conversions   │
│  - Search glossary terms & guides       │
│  - Zero-auth, public API                │
└─────────────────────────────────────────┘
```

**Not all languages need full engine implementations.** The API client is the **minimum viable package** — it provides discovery, glossary/guide search, and SEO backlink value. Engine functions are a bonus that depends on language ecosystem maturity.

### 3.2 Language-Specific Implementation

#### Python (Reference Implementation — already complete)

```
src/peasy_pdf/
├── __init__.py          # Exports
├── engine.py            # Local PDF ops (pypdf)
├── api.py               # REST client (httpx)
├── cli.py               # CLI (typer)
├── mcp_server.py        # MCP server (fastmcp)
└── py.typed             # PEP 561
```

**Layers**: Engine ✅ + API ✅ + CLI ✅ + MCP ✅
**Dependencies**: Core: `pypdf`. Optional: `httpx[api]`, `typer[cli]`, `mcp[mcp]`

#### TypeScript (Engine exists, add API client)

```
src/
├── index.ts             # Re-exports (engine + client)
├── engine.ts            # Local PDF ops (pdf-lib) — EXISTS
├── types.ts             # Engine types (PdfInfo, etc.) — EXISTS
├── client.ts            # REST client (native fetch) — NEW
└── api-types.ts         # API response types (PaginatedResponse, etc.) — NEW
```

**Layers**: Engine ✅ + API ⬜ (to add)
**Dependencies**: Engine-specific (e.g., `pdf-lib`). API client: zero deps (native `fetch`)
**Note**: `types.ts` already exists with engine types (`PdfInfo`, `PdfMetadata`, `PageSize`). API client types go in `api-types.ts` to avoid collision. Both are re-exported from `index.ts`.

#### Rust (Rewrite stubs with API client + selective engine)

```
src/
├── lib.rs               # Module declarations
├── client.rs            # REST client (reqwest) — NEW
├── types.rs             # Serde structs — NEW
├── error.rs             # thiserror — NEW
└── engine.rs            # Local ops (lopdf etc.) — SELECTIVE
```

**Layers**: API ⬜ (priority) + Engine ⬜ (selective)
**Dependencies**: `reqwest`, `serde`, `serde_json`, `tokio`. (`thiserror` already present in existing Cargo.toml.)

**Engine scope per package** (Rust has mature crates for some domains):

| Package | Rust Engine? | Crate |
|---------|-------------|-------|
| peasy-pdf | ✅ Yes | `lopdf` |
| peasy-image | ✅ Yes | `image` |
| peasy-css | ✅ Yes | `lightningcss` or `cssparser` |
| peasy-compress | ✅ Yes | `flate2`, `zip`, `tar` |
| peasytext | ✅ Yes | Pure Rust string ops |
| peasy-document | ⚠️ Partial | `pulldown-cmark` (Markdown only) |
| peasy-audio | ❌ Skip | No mature pure-Rust audio processing |
| peasy-video | ❌ Skip | No mature pure-Rust video processing |

#### Ruby (Enhance stubs with API client + keep system wrappers)

```
lib/peasy_pdf/
├── version.rb           # VERSION constant
├── client.rb            # REST client (Net::HTTP) — NEW
├── types.rb             # Response structs — NEW
└── engine.rb            # System wrapper (qpdf) — EXISTS for some
```

**Layers**: API ⬜ (priority) + Engine ✅ (system wrappers where applicable)
**Dependencies**: Zero (stdlib only: `net/http`, `json`, `uri`)

#### Go (Create from scratch — API client only)

```
peasy-pdf-go/
├── go.mod               # Module declaration
├── client.go            # REST client (net/http)
├── types.go             # Response structs
├── client_test.go       # Tests
├── README.md
└── LICENSE
```

**Layers**: API ⬜ (create) + Engine ❌ (Go PDF ecosystem too immature)
**Dependencies**: Zero (stdlib only: `net/http`, `encoding/json`, `net/url`)

---

## 4. API Client Contract

All languages implement the **same 14 methods** wrapping the peasytools.com DRF API:

### 4.1 Method Signatures

| # | Method | HTTP | Path | Query Params |
|---|--------|------|------|-------------|
| 1 | `list_tools` | GET | `/api/v1/tools/` | `page`, `limit`, `category`, `search` |
| 2 | `get_tool` | GET | `/api/v1/tools/{slug}/` | — |
| 3 | `list_categories` | GET | `/api/v1/categories/` | `page`, `limit` |
| 4 | `list_formats` | GET | `/api/v1/formats/` | `page`, `limit`, `category`, `search` |
| 5 | `get_format` | GET | `/api/v1/formats/{slug}/` | — |
| 6 | `list_conversions` | GET | `/api/v1/conversions/` | `page`, `limit`, `source`, `target` |
| 7 | `list_glossary` | GET | `/api/v1/glossary/` | `page`, `limit`, `category`, `search` |
| 8 | `get_glossary_term` | GET | `/api/v1/glossary/{slug}/` | — |
| 9 | `list_guides` | GET | `/api/v1/guides/` | `page`, `limit`, `category`, `audience_level`, `search` |
| 10 | `get_guide` | GET | `/api/v1/guides/{slug}/` | — |
| 11 | `list_use_cases` | GET | `/api/v1/use-cases/` | `page`, `limit`, `industry`, `search` |
| 12 | `search` | GET | `/api/v1/search/` | `q`, `limit` |
| 13 | `list_sites` | GET | `/api/v1/sites/` | — |
| 14 | `openapi_spec` | GET | `/api/openapi.json` | — |

### 4.2 Base URL Per Package

Each package defaults to its **category site** (not the hub):

| Package | Default Base URL |
|---------|-----------------|
| peasy-pdf | `https://peasypdf.com` |
| peasy-image | `https://peasyimage.com` |
| peasy-audio | `https://peasyaudio.com` |
| peasy-video | `https://peasyvideo.com` |
| peasy-css | `https://peasycss.com` |
| peasy-compress | `https://peasytools.com` |
| peasy-document | `https://peasyformats.com` |
| peasytext | `https://peasytext.com` |

All sites serve the same unified multi-tenant API. Note: `peasy-compress` uses the hub domain (`peasytools.com`) because no dedicated `peasycompress.com` domain exists. Compression tools are listed under the hub's tool categories. README backlink URLs for `peasy-compress` use hub paths like `https://peasytools.com/tools/zip-compress/`.

### 4.3 Response Types

**Paginated list response**:
```json
{
  "count": 255,
  "next": "https://peasypdf.com/api/v1/tools/?page=2",
  "previous": null,
  "results": [...]
}
```

**Detail response**: Single object (no pagination wrapper).

**Search response**: `{"query": "...", "results": {"tools": [...], "formats": [...], "glossary": [...]}}`

**Error responses** (DRF standard):
```json
// 404 Not Found
{"detail": "Not found."}

// 400 Bad Request
{"detail": "Invalid page."}
```

All language clients should raise/return an error with the HTTP status code and the `detail` message when available.

### 4.4 Glossary & Guide Search (Key Feature)

The `search` method returns cross-model results including glossary terms and guides. Additionally, dedicated `list_glossary` and `list_guides` endpoints support `?search=` for filtered searches.

**Usage examples across languages**:

```python
# Python
from peasy_pdf import PeasyPdfAPI
api = PeasyPdfAPI()
results = api.search("lossless compression", limit=10)
tools = api.list_tools(search="merge")
guides = api.list_guides(search="how to compress pdf", category="how-to")
term = api.get_glossary_term("lossless-compression")
```

```typescript
// TypeScript
import { PeasyPdf } from "peasy-pdf";
const client = new PeasyPdf();
const results = await client.search("lossless compression", 10);
const tools = await client.listTools({ search: "merge" });
const guides = await client.listGuides({ search: "how to compress pdf", audienceLevel: "beginner" });
```

```go
// Go
client := peasypdf.NewClient()
results, _ := client.Search(ctx, "lossless compression", nil)
guides, _ := client.ListGuides(ctx, &peasypdf.ListGuidesOptions{Search: "compress"})
tools, _ := client.ListTools(ctx, &peasypdf.ListOptions{Search: "merge"})
```

```rust
// Rust
let client = peasy_pdf::Client::new();
let results = client.search("lossless compression", None).await?;
let guides = client.list_guides(&ListGuidesOptions { search: Some("compress"), ..Default::default() }).await?;
```

```ruby
# Ruby
client = PeasyPDF::Client.new
results = client.search("lossless compression", limit: 10)
guides = client.list_guides(search: "how to compress pdf", audience_level: "beginner")
```

---

## 5. Per-Language Implementation Details

### 5.1 Python — Update API Client (Minor)

**Current state**: Complete (engine + api + cli + mcp). v0.1.1 published.

**Changes needed**:
- Add `list_categories` method to `api.py` (missing in some packages)
- Add `search` parameter to `list_tools`, `list_glossary`, `list_guides`, and `list_use_cases` (all four are currently missing `search` support in the Python reference implementation)
- Update README with "Also Available" 5-language table
- Add guide/glossary search examples to README
- Bump to v0.2.0

### 5.2 TypeScript — Add API Client Layer

**Current state**: Engine functions only. v0.1.1 published.

**New files**:
```typescript
// src/api-types.ts — NEW (separate from existing engine types.ts)
export interface ListOptions {
  page?: number;
  limit?: number;
  search?: string;
  category?: string;
}

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export class PeasyPdf {
  private baseUrl: string;

  constructor(baseUrl = "https://peasypdf.com") {
    this.baseUrl = baseUrl.replace(/\/+$/, "");
  }

  private async get<T>(path: string, params?: Record<string, string>): Promise<T> {
    const url = new URL(path, this.baseUrl);
    if (params) {
      Object.entries(params).forEach(([k, v]) => {
        if (v !== undefined) url.searchParams.set(k, v);
      });
    }
    const res = await fetch(url.toString());
    if (!res.ok) throw new Error(`PeasyPdf API: HTTP ${res.status}`);
    return res.json() as Promise<T>;
  }

  async listTools(opts?: ListOptions) { ... }
  async getTool(slug: string) { ... }
  async listFormats(opts?: ListOptions) { ... }
  async getFormat(slug: string) { ... }
  async listGlossary(opts?: ListOptions) { ... }
  async getGlossaryTerm(slug: string) { ... }
  async listGuides(opts?: ListOptions & { audienceLevel?: string }) { ... }
  async getGuide(slug: string) { ... }
  async listConversions(opts?: ListOptions & { source?: string; target?: string }) { ... }
  async listUseCases(opts?: ListOptions & { industry?: string }) { ... }
  async search(query: string, limit?: number) { ... }
  async listSites() { ... }
  async listCategories(opts?: ListOptions) { ... }
  async openapiSpec() { ... }
}
```

**Dependencies**: Zero runtime (native `fetch`). Dev: `tsup`, `typescript`, `vitest`.
**Build**: ESM only via tsup.

### 5.3 Rust — Full Rewrite (API Client + Selective Engine)

**Current state**: Minimal stubs (version() + error types, `thiserror` already in Cargo.toml).

**New implementation**:

```rust
// src/client.rs
pub struct Client {
    http: reqwest::Client,
    base_url: String,
}

impl Client {
    pub fn new() -> Self { ... }
    pub fn with_base_url(base_url: &str) -> Self { ... }

    pub async fn list_tools(&self, opts: &ListOptions) -> Result<Paginated<Tool>> { ... }
    pub async fn get_tool(&self, slug: &str) -> Result<ToolDetail> { ... }
    pub async fn list_glossary(&self, opts: &ListOptions) -> Result<Paginated<GlossaryTerm>> { ... }
    pub async fn get_glossary_term(&self, slug: &str) -> Result<GlossaryTermDetail> { ... }
    pub async fn list_guides(&self, opts: &ListGuidesOptions) -> Result<Paginated<Guide>> { ... }
    pub async fn get_guide(&self, slug: &str) -> Result<GuideDetail> { ... }
    pub async fn search(&self, query: &str, limit: Option<u32>) -> Result<SearchResult> { ... }
    // ... all 14 methods
}

// ListGuidesOptions includes audience_level field matching the DRF API.
#[derive(Default)]
pub struct ListGuidesOptions {
    pub page: Option<u32>,
    pub limit: Option<u32>,
    pub category: Option<String>,
    pub audience_level: Option<String>,
    pub search: Option<String>,
}
```

**Dependencies**: `reqwest = { version = "0.12", features = ["json"] }`, `serde`, `serde_json`, `thiserror`, `tokio`

**Engine**: Only for packages with mature Rust crates (pdf, image, css, compress, text). Audio/Video skip engine.

### 5.4 Ruby — Add API Client, Keep System Wrappers

**Current state**: Some have system wrapper engines (e.g., peasy-pdf-rb wraps qpdf). No API client.

**New files**:

```ruby
# lib/peasy_pdf/client.rb
require "net/http"
require "json"
require "uri"

module PeasyPDF  # Matches existing convention (all-caps acronym)
  class Client
    DEFAULT_BASE_URL = "https://peasypdf.com"

    def initialize(base_url: DEFAULT_BASE_URL)
      @base_url = base_url
    end

    def list_tools(page: 1, limit: 50, category: nil, search: nil) ... end
    def get_tool(slug) ... end
    def list_glossary(page: 1, limit: 50, category: nil, search: nil) ... end
    def get_glossary_term(slug) ... end
    def list_guides(page: 1, limit: 50, category: nil, audience_level: nil, search: nil) ... end
    def get_guide(slug) ... end
    def search(query, limit: 20) ... end
    # ... all 14 methods

    private

    def get(path, **params)
      uri = URI("#{@base_url}#{path}")
      params.reject! { |_, v| v.nil? }
      uri.query = URI.encode_www_form(params) unless params.empty?
      response = Net::HTTP.get_response(uri)
      raise PeasyPDF::Error, "HTTP #{response.code}: #{JSON.parse(response.body).fetch('detail', 'Unknown error')}" unless response.is_a?(Net::HTTPSuccess)
      JSON.parse(response.body)
    end
  end
end
```

**Module naming**: All Ruby packages use all-caps acronyms matching the existing convention: `PeasyPDF`, `PeasyCSS`, `PeasyImage`, etc.

**Dependencies**: Zero (stdlib only).

### 5.5 Go — Create From Scratch (API Client Only)

**New packages**: 8 new repos (`peasy-pdf-go` through `peasytext-go`).

```go
// client.go
package peasypdf

import (
    "context"
    "encoding/json"
    "fmt"
    "net/http"
    "net/url"
)

const DefaultBaseURL = "https://peasypdf.com"

type Client struct {
    BaseURL    string
    HTTPClient *http.Client
}

func NewClient(opts ...Option) *Client {
    c := &Client{BaseURL: DefaultBaseURL, HTTPClient: &http.Client{}}
    for _, opt := range opts {
        opt(c)
    }
    return c
}

type Option func(*Client)

func WithBaseURL(url string) Option {
    return func(c *Client) { c.BaseURL = url }
}

// All 14 methods with context.Context
func (c *Client) ListTools(ctx context.Context, opts *ListOptions) (*PaginatedResponse[Tool], error) { ... }
func (c *Client) GetTool(ctx context.Context, slug string) (*ToolDetail, error) { ... }
func (c *Client) ListGlossary(ctx context.Context, opts *ListOptions) (*PaginatedResponse[GlossaryTerm], error) { ... }
func (c *Client) ListGuides(ctx context.Context, opts *ListGuidesOptions) (*PaginatedResponse[Guide], error) { ... }
func (c *Client) Search(ctx context.Context, query string, opts *SearchOptions) (*SearchResult, error) { ... }
// ...

// ListGuidesOptions includes AudienceLevel matching the DRF API's audience_level param.
// SearchOptions includes Limit (optional, server default 20).
// ListOptions includes Page, Limit, Category, Search fields.
```

**Dependencies**: Zero (stdlib only). Go 1.21+.
**Module path**: `github.com/peasytools/peasy-pdf-go`
**Publishing**: Git tag `v0.2.0` → auto-indexed on pkg.go.dev.

---

## 6. README Backlink Strategy

### 6.1 URL Placement Per README

Each README includes **10-15 peasytools.com URLs** across these sections:

| Section | URLs | Example |
|---------|------|---------|
| Header tagline | 1 | `[PeasyPDF](https://peasypdf.com)` |
| Description | 2-3 | Tools page, API docs |
| Quick Start | 1-2 | Guide URLs in code comments |
| API Reference | 2-3 | Endpoint URLs with examples |
| Glossary/Guide examples | 3-4 | Specific guide/term URLs |
| Learn More | 5-6 | Tools, guides, glossary, API docs |
| Also Available | 5 | Cross-language links |

### 6.2 URL Categories

```markdown
## Learn More

- **Tools**: [PDF Merge](https://peasypdf.com/pdf/pdf-merge/) · [PDF Split](https://peasypdf.com/pdf/pdf-split/) · [All PDF Tools](https://peasypdf.com/pdf/)
- **Guides**: [How to Compress PDFs](https://peasypdf.com/guides/how-to-compress-pdf/) · [PDF vs DOCX](https://peasypdf.com/guides/pdf-vs-docx/) · [All Guides](https://peasypdf.com/guides/)
- **Glossary**: [What is PDF/A?](https://peasypdf.com/glossary/pdfa/) · [Lossless Compression](https://peasypdf.com/glossary/lossless-compression/) · [All Terms](https://peasypdf.com/glossary/)
- **Formats**: [PDF Format](https://peasypdf.com/formats/pdf/) · [All Formats](https://peasypdf.com/formats/)
- **API**: [REST API Docs](https://peasypdf.com/api/docs/) · [OpenAPI Spec](https://peasypdf.com/api/openapi.json)
```

### 6.3 Guide Document Samples in README

Each README includes a **real API response sample** showing guide content:

```markdown
### Fetching a Guide

\```python
guide = api.get_guide("how-to-compress-pdf")
print(guide["title"])       # "How to Compress PDF Files Without Losing Quality"
print(guide["word_count"])  # 1542
print(guide["content"][:200])  # First 200 chars of Markdown content
# Full guide: https://peasypdf.com/guides/how-to-compress-pdf/
\```
```

### 6.4 Also Available Table (All READMEs)

```markdown
## Also Available

| Language | Package | Install |
|----------|---------|---------|
| **Python** | [peasy-pdf](https://pypi.org/project/peasy-pdf/) | `pip install "peasy-pdf[api]"` |
| **TypeScript** | [peasy-pdf](https://www.npmjs.com/package/peasy-pdf) | `npm install peasy-pdf` |
| **Go** | [peasy-pdf-go](https://pkg.go.dev/github.com/peasytools/peasy-pdf-go) | `go get github.com/peasytools/peasy-pdf-go` |
| **Rust** | [peasy-pdf](https://crates.io/crates/peasy-pdf) | `cargo add peasy-pdf` |
| **Ruby** | [peasy-pdf](https://rubygems.org/gems/peasy-pdf) | `gem install peasy-pdf` |
```

### 6.5 Peasy Tools Ecosystem Table

```markdown
## Peasy Tools

Part of the [Peasy Tools](https://peasytools.com) open-source developer ecosystem.

| Package | PyPI | npm | Description |
|---------|------|-----|-------------|
| **peasy-pdf** | [PyPI](https://pypi.org/project/peasy-pdf/) | [npm](https://npmjs.com/package/peasy-pdf) | PDF merge, split, rotate, metadata — [peasypdf.com](https://peasypdf.com) |
| peasy-image | [PyPI](https://pypi.org/project/peasy-image/) | [npm](https://npmjs.com/package/peasy-image) | Image resize, crop, convert, compress — [peasyimage.com](https://peasyimage.com) |
| peasytext | [PyPI](https://pypi.org/project/peasytext/) | [npm](https://npmjs.com/package/peasytext) | Text case conversion, slugify, word count — [peasytext.com](https://peasytext.com) |
| peasy-css | [PyPI](https://pypi.org/project/peasy-css/) | [npm](https://npmjs.com/package/peasy-css) | CSS minify, format, analyze — [peasycss.com](https://peasycss.com) |
| peasy-compress | [PyPI](https://pypi.org/project/peasy-compress/) | [npm](https://npmjs.com/package/peasy-compress) | ZIP, TAR, gzip compression — [peasytools.com](https://peasytools.com) |
| peasy-document | [PyPI](https://pypi.org/project/peasy-document/) | [npm](https://npmjs.com/package/peasy-document) | Markdown, HTML, CSV, JSON conversion — [peasyformats.com](https://peasyformats.com) |
| peasy-audio | [PyPI](https://pypi.org/project/peasy-audio/) | [npm](https://npmjs.com/package/peasy-audio) | Audio trim, merge, convert, normalize — [peasyaudio.com](https://peasyaudio.com) |
| peasy-video | [PyPI](https://pypi.org/project/peasy-video/) | [npm](https://npmjs.com/package/peasy-video) | Video trim, resize, thumbnails, GIF — [peasyvideo.com](https://peasyvideo.com) |
```

---

## 7. Implementation Priority

### Phase 1: Go Packages (8 new repos) — Highest Impact

Go packages don't exist yet. Creating them:
- Fills the 5th language slot (completing the AgentGIF pattern)
- 8 new PUBLIC repos = 8 new backlink sources
- Simplest implementation (API client only, zero deps)

**Order**: peasy-pdf-go → peasytext-go → peasy-image-go → peasy-css-go → peasy-compress-go → peasy-document-go → peasy-audio-go → peasy-video-go

### Phase 2: TypeScript API Client (8 updates)

Add `client.ts` + `api-types.ts` to all 8 existing JS packages:
- Packages already published, just need API client layer
- Zero new dependencies (native `fetch`)
- Bump to v0.2.0 and republish

### Phase 3: Rust Rewrite (8 updates)

Replace stubs with real API client + selective engine:
- API client for all 8 packages
- Engine functions for 6/8 packages (skip audio/video)
- Bump to v0.2.0 and republish

### Phase 4: Ruby API Client (8 updates)

Add API client to all 8 Ruby packages:
- Zero dependencies (stdlib Net::HTTP)
- Keep existing system wrapper engines where they exist
- Bump to v0.2.0 and republish

### Phase 5: Python Updates + README Overhaul (8 updates)

- Ensure API client parity (add missing methods)
- Update all 40 READMEs with backlinks and "Also Available" tables
- Bump to v0.2.0

### Phase 6: Make Existing Repos PUBLIC + Final Publish

- Flip the existing 32 PRIVATE repos → PUBLIC (Go repos are already created PUBLIC in Phase 1)
- Publish all updated packages to registries
- Verify all backlinks resolve
- Run `gh repo list peasytools --visibility public` to confirm all 40 repos are visible

---

## 8. Version Strategy

All packages bump from v0.1.1 → **v0.2.0** with this expansion:

| What's New in v0.2.0 |
|----------------------|
| API client for peasytools.com REST API |
| Glossary search (`list_glossary`, `get_glossary_term`) |
| Guide search (`list_guides`, `get_guide`) |
| Unified search across tools, formats, and glossary |
| Format conversion discovery (`list_conversions`) |
| "Also Available" cross-language table in README |
| PUBLIC GitHub repository |

---

## 9. File Templates Per Language

### Go Template (peasy-pdf-go)

```
peasy-pdf-go/
├── go.mod                    # module github.com/peasytools/peasy-pdf-go
├── README.md                 # Gold Standard with backlinks
├── LICENSE                   # MIT
├── client.go                 # Client struct + 14 methods
├── types.go                  # Response structs (Tool, Format, GlossaryTerm, Guide, etc.)
├── options.go                # ListOptions, ListGuideOptions, etc.
├── client_test.go            # Tests
└── .gitignore
```

### TypeScript Addition (peasy-pdf-js)

```
src/
├── index.ts                  # UPDATE: re-export engine + client + all types
├── engine.ts                 # EXISTING: local PDF ops
├── types.ts                  # EXISTING: engine types (PdfInfo, PageSize, etc.)
├── client.ts                 # NEW: REST API client
└── api-types.ts              # NEW: API response interfaces (PaginatedResponse, etc.)
```

### Rust Rewrite (peasy-pdf-rs)

```
src/
├── lib.rs                    # REWRITE: mod declarations + re-exports
├── client.rs                 # NEW: async Client struct
├── types.rs                  # NEW: Serde types
├── error.rs                  # NEW: thiserror Error enum
└── engine.rs                 # REWRITE: real PDF ops with lopdf (selective)
```

### Ruby Addition (peasy-pdf-rb)

```
lib/peasy_pdf/
├── version.rb                # EXISTING: bump version
├── client.rb                 # NEW: Net::HTTP API client
├── types.rb                  # NEW: response types (OpenStruct or plain Hash)
└── engine.rb                 # EXISTING: system wrappers (keep)
```

---

## 10. Testing Strategy

| Language | Framework | What to Test |
|----------|-----------|-------------|
| Python | pytest | API client methods with mocked httpx |
| TypeScript | vitest | Client methods with mocked fetch |
| Go | go test | Client methods with httptest.Server |
| Rust | cargo test | Client methods with mockito or wiremock |
| Ruby | minitest | Client methods with webmock |

**Minimum test coverage**: Every API client method has at least one test verifying:
1. Correct URL construction
2. Query parameter serialization
3. Response deserialization
4. Error handling (non-200 status)

---

## 11. Publication Pipeline

### Per-Language Publishing

| Language | Command | Auth |
|----------|---------|------|
| Python | `uv build && uv publish` | `service-pypi` token |
| TypeScript | `npm run build && npm publish` | `service-npm` token |
| Go | `git tag v0.2.0 && git push --tags` | Auto-indexed |
| Rust | `cargo publish` | `service-crates-io` token |
| Ruby | `gem build && gem push` | `service-rubygems` token (MFA required) |

### Repo Visibility Change

```bash
# Batch flip all repos to PUBLIC
gh repo list peasytools --limit 100 --json name --jq '.[].name' | while read repo; do
  gh repo edit "peasytools/$repo" --visibility public
done
```

---

## 12. Success Metrics

| Metric | Target |
|--------|--------|
| Total packages published | 40 (8 × 5 languages) |
| GitHub repos PUBLIC | 40+ |
| Backlinks per README | 10-15 peasytools.com URLs |
| Total backlink sources | 40 repos × 3 registries = ~120 indexed pages |
| API client methods per package | 14 (unified contract) |
| Glossary/Guide search | All 40 packages |
| Version alignment | All at v0.2.0 |

---

## 13. Excluded from Scope

| Item | Reason |
|------|--------|
| peasy-mcp (unified MCP hub) | Already complete, separate concern |
| peasy-convert (unified CLI) | Already complete, wraps individual packages |
| peasy-vscode | VS Code extension, different distribution |
| peasy-gpts | ChatGPT integration, different platform |
| peasy-docker | Container images, different distribution |
| peasy-actions | GitHub Actions, different distribution |
| peasy-chrome | Browser extension, different platform |
| homebrew-peasy | Homebrew tap, depends on CLI packages |

---

## 14. Risk & Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| Ruby MFA blocker | Can't push gems without OTP | Use `gem push --otp` with authenticator app |
| crates.io name conflicts | `peasy-pdf` may be taken | Check availability first; fallback: `peasytools-pdf` |
| npm name conflicts | `peasy-pdf` may be taken | Already published 8/8 under bare names (no @org scope) ✅ |
| Go module path change | peasytools org vs fyipedia | Use `peasytools` consistently |
| API rate limiting | High traffic from packages | peasytools.com has no rate limits (public API) |
| README content duplication | 40 READMEs with similar structure | Template-driven generation per package |
