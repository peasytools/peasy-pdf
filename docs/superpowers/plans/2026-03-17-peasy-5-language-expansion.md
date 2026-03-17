# Peasy 5-Language Package Expansion — Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Expand 8 Peasy functional packages to 5 languages (Python, TypeScript, Rust, Ruby, Go) with unified API client, glossary/guide search, SEO-optimized READMEs with peasytools.com backlinks, and PUBLIC GitHub repos.

**Architecture:** Each package has two layers: Engine (local file operations) and API Client (REST wrapper for peasytools.com DRF API with 14 unified methods). API client is the minimum viable package — engine is a bonus per language ecosystem maturity.

**Tech Stack:** Python/httpx, TypeScript/native fetch, Go/stdlib net/http, Rust/reqwest+serde+tokio, Ruby/stdlib Net::HTTP. All zero-auth, public API.

**Spec:** `docs/superpowers/specs/2026-03-17-peasy-5-language-expansion-design.md`

**Critical Rule:** 절대로 Claude API를 사용하지 않는다 (NEVER use Claude API)

---

## File Structure Overview

### New files to CREATE (per Go package — 8 packages × 6 files = 48 files):
```
packages/peasy-{name}-go/
├── go.mod              # module github.com/peasytools/peasy-{name}-go
├── client.go           # Client struct + 14 methods
├── types.go            # Response structs (Tool, Format, GlossaryTerm, Guide, etc.)
├── errors.go           # PeasyError, NotFoundError, APIError
├── client_test.go      # httptest.NewServer-based tests
├── README.md           # Gold Standard with peasytools.com backlinks
└── LICENSE             # MIT
```

### New files to CREATE (per TypeScript package — 8 packages × 2 files = 16 files):
```
packages/peasy-{name}-js/src/
├── client.ts           # PeasyPdf class with 14 async methods
└── api-types.ts        # PaginatedResponse, ListOptions, etc.
```

### New files to CREATE (per Rust package — 8 packages × 3 files = 24 files):
```
packages/peasy-{name}-rs/src/
├── client.rs           # async Client struct with 14 methods
├── types.rs            # Serde structs for API responses
└── error.rs            # thiserror PeasyError enum
```

### New files to CREATE (per Ruby package — 8 packages × 2 files = 16 files):
```
packages/peasy-{name}-rb/lib/peasy_{name}/
├── client.rb           # Client class with 14 methods
└── types.rb            # Response wrapper (optional — Ruby uses Hash)
```

### Existing files to MODIFY:
- `packages/peasy-{name}-js/src/index.ts` — re-export client + api-types
- `packages/peasy-{name}-js/package.json` — bump version to 0.2.0
- `packages/peasy-{name}-rs/Cargo.toml` — add reqwest/serde/tokio deps, bump version
- `packages/peasy-{name}-rs/src/lib.rs` — add mod client/types/error declarations
- `packages/peasy-{name}-rb/lib/peasy_{name}.rb` — require client.rb
- `packages/peasy-{name}-rb/peasy-{name}.gemspec` — bump version
- `packages/peasy-{name}-rb/lib/peasy_{name}/version.rb` — bump version
- `packages/peasy-{name}/src/peasy_{name}/api.py` — add search param to list methods
- `packages/peasy-{name}/pyproject.toml` — bump version
- All 40 `README.md` files — add backlinks, Also Available table, ecosystem table

### Package ↔ Name mapping (8 packages):
| Package | Python module | TS class | Go package | Rust crate | Ruby module | Default base URL |
|---------|--------------|----------|------------|------------|-------------|-----------------|
| peasy-pdf | `peasy_pdf` | `PeasyPdf` | `peasypdf` | `peasy_pdf` | `PeasyPDF` | `https://peasypdf.com` |
| peasy-image | `peasy_image` | `PeasyImage` | `peasyimage` | `peasy_image` | `PeasyImage` | `https://peasyimage.com` |
| peasy-audio | `peasy_audio` | `PeasyAudio` | `peasyaudio` | `peasy_audio` | `PeasyAudio` | `https://peasyaudio.com` |
| peasy-video | `peasy_video` | `PeasyVideo` | `peasyvideo` | `peasy_video` | `PeasyVideo` | `https://peasyvideo.com` |
| peasy-css | `peasy_css` | `PeasyCss` | `peasycss` | `peasy_css` | `PeasyCSS` | `https://peasycss.com` |
| peasy-compress | `peasy_compress` | `PeasyCompress` | `peasycompress` | `peasy_compress` | `PeasyCompress` | `https://peasytools.com` |
| peasy-document | `peasy_document` | `PeasyDocument` | `peasydocument` | `peasy_document` | `PeasyDocument` | `https://peasyformats.com` |
| peasytext | `peasytext` | `PeasyText` | `peasytext` | `peasytext` | `PeasyText` | `https://peasytext.com` |

---

## Chunk 1: Phase 1 — Go Packages (8 new repos)

Go packages are created from scratch. This is the highest-impact phase: 8 new PUBLIC repos = 8 new backlink sources, and it completes the 5th language slot.

**Gold Standard Reference:** `packages/citedhealth-go/` (241-line client.go, 62-line types.go, 32-line errors.go, 408-line test file)

**Order:** peasy-pdf-go first (template), then replicate for remaining 7 packages.

### Task 1: Create peasy-pdf-go repository

**Files:**
- Create: `packages/peasy-pdf-go/go.mod`
- Create: `packages/peasy-pdf-go/errors.go`
- Create: `packages/peasy-pdf-go/types.go`
- Create: `packages/peasy-pdf-go/client.go`
- Create: `packages/peasy-pdf-go/client_test.go`
- Create: `packages/peasy-pdf-go/LICENSE`
- Create: `packages/peasy-pdf-go/README.md`

- [ ] **Step 1: Create the GitHub repo**

```bash
cd ~/dev/packages
gh repo create peasytools/peasy-pdf-go --public --description "Go client for PeasyPDF — PDF tools, glossary, and guides API" --license MIT --clone
cd peasy-pdf-go
```

- [ ] **Step 2: Create go.mod**

Create `go.mod`:
```
module github.com/peasytools/peasy-pdf-go

go 1.21
```

- [ ] **Step 3: Write errors.go**

Create `errors.go`:
```go
package peasypdf

import "fmt"

// PeasyError is the base error type for Peasy API errors.
type PeasyError struct {
	StatusCode int
	Message    string
}

func (e *PeasyError) Error() string {
	return fmt.Sprintf("peasypdf: HTTP %d: %s", e.StatusCode, e.Message)
}

// NotFoundError is returned when a resource is not found (404).
type NotFoundError struct {
	Resource   string
	Identifier string
}

func (e *NotFoundError) Error() string {
	return fmt.Sprintf("peasypdf: %s not found: %s", e.Resource, e.Identifier)
}
```

- [ ] **Step 4: Write types.go with all 14 response types**

Create `types.go`:
```go
package peasypdf

import "encoding/json"

// PaginatedResponse represents a DRF paginated API response.
type PaginatedResponse struct {
	Count    int             `json:"count"`
	Next     *string         `json:"next"`
	Previous *string         `json:"previous"`
	Results  json.RawMessage `json:"results"`
}

// Tool represents a Peasy tool.
type Tool struct {
	Slug        string `json:"slug"`
	Name        string `json:"name"`
	Description string `json:"description"`
	Category    string `json:"category"`
	URL         string `json:"url"`
}

// Category represents a tool category.
type Category struct {
	Slug        string `json:"slug"`
	Name        string `json:"name"`
	Description string `json:"description"`
	ToolCount   int    `json:"tool_count"`
}

// Format represents a file format.
type Format struct {
	Slug        string   `json:"slug"`
	Name        string   `json:"name"`
	Extension   string   `json:"extension"`
	MimeType    string   `json:"mime_type"`
	Category    string   `json:"category"`
	Description string   `json:"description"`
}

// Conversion represents a format conversion.
type Conversion struct {
	Source      string `json:"source"`
	Target      string `json:"target"`
	Description string `json:"description"`
	ToolSlug    string `json:"tool_slug"`
}

// GlossaryTerm represents a glossary term.
type GlossaryTerm struct {
	Slug       string `json:"slug"`
	Term       string `json:"term"`
	Definition string `json:"definition"`
	Category   string `json:"category"`
}

// Guide represents a how-to guide.
type Guide struct {
	Slug          string `json:"slug"`
	Title         string `json:"title"`
	Description   string `json:"description"`
	Category      string `json:"category"`
	AudienceLevel string `json:"audience_level"`
	WordCount     int    `json:"word_count"`
}

// UseCase represents an industry use case.
type UseCase struct {
	Slug     string `json:"slug"`
	Title    string `json:"title"`
	Industry string `json:"industry"`
}

// Site represents a Peasy site.
type Site struct {
	Name   string `json:"name"`
	Domain string `json:"domain"`
	URL    string `json:"url"`
}

// SearchResult represents a cross-model search response.
type SearchResult struct {
	Query   string           `json:"query"`
	Results SearchCategories `json:"results"`
}

// SearchCategories holds categorized search results.
type SearchCategories struct {
	Tools    []Tool        `json:"tools"`
	Formats  []Format      `json:"formats"`
	Glossary []GlossaryTerm `json:"glossary"`
}

// ListOptions configures paginated list requests.
type ListOptions struct {
	Page     int
	Limit    int
	Category string
	Search   string
}

// ListGuidesOptions extends ListOptions with audience level.
type ListGuidesOptions struct {
	Page          int
	Limit         int
	Category      string
	AudienceLevel string
	Search        string
}

// ListConversionsOptions configures conversion list requests.
type ListConversionsOptions struct {
	Page   int
	Limit  int
	Source string
	Target string
}

// SearchOptions configures search requests.
type SearchOptions struct {
	Limit int
}
```

- [ ] **Step 5: Write client.go with all 14 methods**

Create `client.go`:
```go
// Package peasypdf provides a Go client for the PeasyPDF API.
//
// PeasyPDF offers PDF tools (merge, split, rotate, compress), glossary terms,
// how-to guides, and format conversion discovery. This client requires no
// authentication and has zero external dependencies.
//
// Usage:
//
//	client := peasypdf.New()
//	tools, err := client.ListTools(ctx, nil)
//	term, err := client.GetGlossaryTerm(ctx, "lossy-compression")
//	results, err := client.Search(ctx, "merge pdf", nil)
package peasypdf

import (
	"context"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"net/url"
	"strconv"
	"strings"
	"time"
)

// DefaultBaseURL is the default base URL for the PeasyPDF API.
const DefaultBaseURL = "https://peasypdf.com"

// DefaultTimeout is the default HTTP timeout.
const DefaultTimeout = 30 * time.Second

// Client is a PeasyPDF API client.
type Client struct {
	baseURL    string
	httpClient *http.Client
}

// Option configures the Client.
type Option func(*Client)

// WithBaseURL sets a custom base URL.
func WithBaseURL(u string) Option {
	return func(c *Client) {
		c.baseURL = strings.TrimRight(u, "/")
	}
}

// WithTimeout sets a custom HTTP timeout.
func WithTimeout(d time.Duration) Option {
	return func(c *Client) {
		c.httpClient.Timeout = d
	}
}

// WithHTTPClient sets a custom HTTP client.
func WithHTTPClient(hc *http.Client) Option {
	return func(c *Client) {
		c.httpClient = hc
	}
}

// New creates a new PeasyPDF API client.
func New(opts ...Option) *Client {
	c := &Client{
		baseURL:    DefaultBaseURL,
		httpClient: &http.Client{Timeout: DefaultTimeout},
	}
	for _, opt := range opts {
		opt(c)
	}
	return c
}

func (c *Client) doRequest(ctx context.Context, path string) ([]byte, error) {
	req, err := http.NewRequestWithContext(ctx, http.MethodGet, c.baseURL+path, nil)
	if err != nil {
		return nil, fmt.Errorf("peasypdf: create request: %w", err)
	}

	resp, err := c.httpClient.Do(req)
	if err != nil {
		return nil, fmt.Errorf("peasypdf: request failed: %w", err)
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, fmt.Errorf("peasypdf: read body: %w", err)
	}

	if resp.StatusCode == http.StatusOK {
		return body, nil
	}
	if resp.StatusCode == http.StatusNotFound {
		return nil, &NotFoundError{Resource: "resource", Identifier: path}
	}
	return nil, &PeasyError{
		StatusCode: resp.StatusCode,
		Message:    string(body),
	}
}

func buildListParams(page, limit int, category, search string) url.Values {
	params := url.Values{}
	if page > 0 {
		params.Set("page", strconv.Itoa(page))
	}
	if limit > 0 {
		params.Set("limit", strconv.Itoa(limit))
	}
	if category != "" {
		params.Set("category", category)
	}
	if search != "" {
		params.Set("search", search)
	}
	return params
}

func buildPath(base string, params url.Values) string {
	if encoded := params.Encode(); encoded != "" {
		return base + "?" + encoded
	}
	return base
}

// ListTools returns a paginated list of tools.
func (c *Client) ListTools(ctx context.Context, opts *ListOptions) ([]Tool, error) {
	o := applyListOpts(opts)
	path := buildPath("/api/v1/tools/", buildListParams(o.Page, o.Limit, o.Category, o.Search))

	body, err := c.doRequest(ctx, path)
	if err != nil {
		return nil, fmt.Errorf("peasypdf: list tools: %w", err)
	}
	return decodePaginated[Tool](body)
}

// GetTool returns a single tool by slug.
func (c *Client) GetTool(ctx context.Context, slug string) (*Tool, error) {
	body, err := c.doRequest(ctx, "/api/v1/tools/"+url.PathEscape(slug)+"/")
	if err != nil {
		return nil, fmt.Errorf("peasypdf: get tool: %w", err)
	}
	var tool Tool
	if err := json.Unmarshal(body, &tool); err != nil {
		return nil, fmt.Errorf("peasypdf: decode tool: %w", err)
	}
	return &tool, nil
}

// ListCategories returns a paginated list of categories.
func (c *Client) ListCategories(ctx context.Context, opts *ListOptions) ([]Category, error) {
	o := applyListOpts(opts)
	path := buildPath("/api/v1/categories/", buildListParams(o.Page, o.Limit, "", ""))

	body, err := c.doRequest(ctx, path)
	if err != nil {
		return nil, fmt.Errorf("peasypdf: list categories: %w", err)
	}
	return decodePaginated[Category](body)
}

// ListFormats returns a paginated list of file formats.
func (c *Client) ListFormats(ctx context.Context, opts *ListOptions) ([]Format, error) {
	o := applyListOpts(opts)
	path := buildPath("/api/v1/formats/", buildListParams(o.Page, o.Limit, o.Category, o.Search))

	body, err := c.doRequest(ctx, path)
	if err != nil {
		return nil, fmt.Errorf("peasypdf: list formats: %w", err)
	}
	return decodePaginated[Format](body)
}

// GetFormat returns a single format by slug.
func (c *Client) GetFormat(ctx context.Context, slug string) (*Format, error) {
	body, err := c.doRequest(ctx, "/api/v1/formats/"+url.PathEscape(slug)+"/")
	if err != nil {
		return nil, fmt.Errorf("peasypdf: get format: %w", err)
	}
	var f Format
	if err := json.Unmarshal(body, &f); err != nil {
		return nil, fmt.Errorf("peasypdf: decode format: %w", err)
	}
	return &f, nil
}

// ListConversions returns a paginated list of format conversions.
func (c *Client) ListConversions(ctx context.Context, opts *ListConversionsOptions) ([]Conversion, error) {
	params := url.Values{}
	if opts != nil {
		if opts.Page > 0 {
			params.Set("page", strconv.Itoa(opts.Page))
		}
		if opts.Limit > 0 {
			params.Set("limit", strconv.Itoa(opts.Limit))
		}
		if opts.Source != "" {
			params.Set("source", opts.Source)
		}
		if opts.Target != "" {
			params.Set("target", opts.Target)
		}
	}
	path := buildPath("/api/v1/conversions/", params)

	body, err := c.doRequest(ctx, path)
	if err != nil {
		return nil, fmt.Errorf("peasypdf: list conversions: %w", err)
	}
	return decodePaginated[Conversion](body)
}

// ListGlossary returns a paginated list of glossary terms.
func (c *Client) ListGlossary(ctx context.Context, opts *ListOptions) ([]GlossaryTerm, error) {
	o := applyListOpts(opts)
	path := buildPath("/api/v1/glossary/", buildListParams(o.Page, o.Limit, o.Category, o.Search))

	body, err := c.doRequest(ctx, path)
	if err != nil {
		return nil, fmt.Errorf("peasypdf: list glossary: %w", err)
	}
	return decodePaginated[GlossaryTerm](body)
}

// GetGlossaryTerm returns a single glossary term by slug.
func (c *Client) GetGlossaryTerm(ctx context.Context, slug string) (*GlossaryTerm, error) {
	body, err := c.doRequest(ctx, "/api/v1/glossary/"+url.PathEscape(slug)+"/")
	if err != nil {
		return nil, fmt.Errorf("peasypdf: get glossary term: %w", err)
	}
	var term GlossaryTerm
	if err := json.Unmarshal(body, &term); err != nil {
		return nil, fmt.Errorf("peasypdf: decode glossary term: %w", err)
	}
	return &term, nil
}

// ListGuides returns a paginated list of guides.
func (c *Client) ListGuides(ctx context.Context, opts *ListGuidesOptions) ([]Guide, error) {
	params := url.Values{}
	if opts != nil {
		if opts.Page > 0 {
			params.Set("page", strconv.Itoa(opts.Page))
		}
		if opts.Limit > 0 {
			params.Set("limit", strconv.Itoa(opts.Limit))
		}
		if opts.Category != "" {
			params.Set("category", opts.Category)
		}
		if opts.AudienceLevel != "" {
			params.Set("audience_level", opts.AudienceLevel)
		}
		if opts.Search != "" {
			params.Set("search", opts.Search)
		}
	}
	path := buildPath("/api/v1/guides/", params)

	body, err := c.doRequest(ctx, path)
	if err != nil {
		return nil, fmt.Errorf("peasypdf: list guides: %w", err)
	}
	return decodePaginated[Guide](body)
}

// GetGuide returns a single guide by slug.
func (c *Client) GetGuide(ctx context.Context, slug string) (*Guide, error) {
	body, err := c.doRequest(ctx, "/api/v1/guides/"+url.PathEscape(slug)+"/")
	if err != nil {
		return nil, fmt.Errorf("peasypdf: get guide: %w", err)
	}
	var g Guide
	if err := json.Unmarshal(body, &g); err != nil {
		return nil, fmt.Errorf("peasypdf: decode guide: %w", err)
	}
	return &g, nil
}

// ListUseCases returns a paginated list of use cases.
func (c *Client) ListUseCases(ctx context.Context, opts *ListOptions) ([]UseCase, error) {
	o := applyListOpts(opts)
	params := buildListParams(o.Page, o.Limit, "", o.Search)
	if o.Category != "" {
		params.Set("industry", o.Category)
	}
	path := buildPath("/api/v1/use-cases/", params)

	body, err := c.doRequest(ctx, path)
	if err != nil {
		return nil, fmt.Errorf("peasypdf: list use cases: %w", err)
	}
	return decodePaginated[UseCase](body)
}

// Search searches across tools, formats, and glossary.
func (c *Client) Search(ctx context.Context, query string, opts *SearchOptions) (*SearchResult, error) {
	params := url.Values{"q": {query}}
	if opts != nil && opts.Limit > 0 {
		params.Set("limit", strconv.Itoa(opts.Limit))
	}
	path := buildPath("/api/v1/search/", params)

	body, err := c.doRequest(ctx, path)
	if err != nil {
		return nil, fmt.Errorf("peasypdf: search: %w", err)
	}
	var result SearchResult
	if err := json.Unmarshal(body, &result); err != nil {
		return nil, fmt.Errorf("peasypdf: decode search result: %w", err)
	}
	return &result, nil
}

// ListSites returns all Peasy sites.
func (c *Client) ListSites(ctx context.Context) ([]Site, error) {
	body, err := c.doRequest(ctx, "/api/v1/sites/")
	if err != nil {
		return nil, fmt.Errorf("peasypdf: list sites: %w", err)
	}
	return decodePaginated[Site](body)
}

// OpenAPISpec returns the OpenAPI 3.0.3 specification.
func (c *Client) OpenAPISpec(ctx context.Context) (map[string]interface{}, error) {
	body, err := c.doRequest(ctx, "/api/openapi.json")
	if err != nil {
		return nil, fmt.Errorf("peasypdf: openapi spec: %w", err)
	}
	var spec map[string]interface{}
	if err := json.Unmarshal(body, &spec); err != nil {
		return nil, fmt.Errorf("peasypdf: decode openapi spec: %w", err)
	}
	return spec, nil
}

// --- helpers ---

func applyListOpts(opts *ListOptions) ListOptions {
	if opts == nil {
		return ListOptions{}
	}
	return *opts
}

func decodePaginated[T any](body []byte) ([]T, error) {
	var page PaginatedResponse
	if err := json.Unmarshal(body, &page); err != nil {
		return nil, fmt.Errorf("decode paginated response: %w", err)
	}
	var items []T
	if err := json.Unmarshal(page.Results, &items); err != nil {
		return nil, fmt.Errorf("decode results: %w", err)
	}
	return items, nil
}
```

- [ ] **Step 6: Write client_test.go**

Create `client_test.go`:
```go
package peasypdf_test

import (
	"context"
	"encoding/json"
	"errors"
	"net/http"
	"net/http/httptest"
	"testing"

	peasypdf "github.com/peasytools/peasy-pdf-go"
)

func paginatedJSON(t *testing.T, results interface{}) []byte {
	t.Helper()
	raw, err := json.Marshal(results)
	if err != nil {
		t.Fatalf("marshal results: %v", err)
	}
	body := map[string]interface{}{
		"count":    1,
		"next":     nil,
		"previous": nil,
		"results":  json.RawMessage(raw),
	}
	b, err := json.Marshal(body)
	if err != nil {
		t.Fatalf("marshal paginated: %v", err)
	}
	return b
}

func TestNew(t *testing.T) {
	c := peasypdf.New()
	if c == nil {
		t.Fatal("expected non-nil client")
	}
}

func TestListTools(t *testing.T) {
	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path != "/api/v1/tools/" {
			t.Errorf("unexpected path: %s", r.URL.Path)
		}
		w.Header().Set("Content-Type", "application/json")
		w.Write(paginatedJSON(t, []map[string]interface{}{
			{"slug": "pdf-merge", "name": "PDF Merge", "category": "pdf"},
		}))
	}))
	defer srv.Close()

	c := peasypdf.New(peasypdf.WithBaseURL(srv.URL))
	tools, err := c.ListTools(context.Background(), nil)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if len(tools) != 1 {
		t.Fatalf("expected 1 tool, got %d", len(tools))
	}
	if tools[0].Slug != "pdf-merge" {
		t.Errorf("expected slug pdf-merge, got %s", tools[0].Slug)
	}
}

func TestListToolsWithSearch(t *testing.T) {
	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if s := r.URL.Query().Get("search"); s != "merge" {
			t.Errorf("expected search=merge, got search=%s", s)
		}
		w.Header().Set("Content-Type", "application/json")
		w.Write(paginatedJSON(t, []map[string]interface{}{
			{"slug": "pdf-merge", "name": "PDF Merge"},
		}))
	}))
	defer srv.Close()

	c := peasypdf.New(peasypdf.WithBaseURL(srv.URL))
	tools, err := c.ListTools(context.Background(), &peasypdf.ListOptions{Search: "merge"})
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if len(tools) != 1 {
		t.Fatalf("expected 1 tool, got %d", len(tools))
	}
}

func TestGetTool(t *testing.T) {
	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path != "/api/v1/tools/pdf-merge/" {
			t.Errorf("unexpected path: %s", r.URL.Path)
		}
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(map[string]interface{}{
			"slug": "pdf-merge", "name": "PDF Merge", "description": "Merge PDFs",
		})
	}))
	defer srv.Close()

	c := peasypdf.New(peasypdf.WithBaseURL(srv.URL))
	tool, err := c.GetTool(context.Background(), "pdf-merge")
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if tool.Name != "PDF Merge" {
		t.Errorf("expected PDF Merge, got %s", tool.Name)
	}
}

func TestListGlossary(t *testing.T) {
	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path != "/api/v1/glossary/" {
			t.Errorf("unexpected path: %s", r.URL.Path)
		}
		w.Header().Set("Content-Type", "application/json")
		w.Write(paginatedJSON(t, []map[string]interface{}{
			{"slug": "lossy-compression", "term": "Lossy Compression", "category": "compression"},
		}))
	}))
	defer srv.Close()

	c := peasypdf.New(peasypdf.WithBaseURL(srv.URL))
	terms, err := c.ListGlossary(context.Background(), &peasypdf.ListOptions{Search: "lossy"})
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if len(terms) != 1 {
		t.Fatalf("expected 1 term, got %d", len(terms))
	}
}

func TestGetGlossaryTerm(t *testing.T) {
	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path != "/api/v1/glossary/lossy-compression/" {
			t.Errorf("unexpected path: %s", r.URL.Path)
		}
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(map[string]interface{}{
			"slug": "lossy-compression", "term": "Lossy Compression",
			"definition": "A compression method that reduces file size by discarding some data.",
			"category":   "compression",
		})
	}))
	defer srv.Close()

	c := peasypdf.New(peasypdf.WithBaseURL(srv.URL))
	term, err := c.GetGlossaryTerm(context.Background(), "lossy-compression")
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if term.Term != "Lossy Compression" {
		t.Errorf("expected Lossy Compression, got %s", term.Term)
	}
}

func TestListGuides(t *testing.T) {
	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if al := r.URL.Query().Get("audience_level"); al != "beginner" {
			t.Errorf("expected audience_level=beginner, got %s", al)
		}
		w.Header().Set("Content-Type", "application/json")
		w.Write(paginatedJSON(t, []map[string]interface{}{
			{"slug": "how-to-merge-pdfs", "title": "How to Merge PDFs", "audience_level": "beginner"},
		}))
	}))
	defer srv.Close()

	c := peasypdf.New(peasypdf.WithBaseURL(srv.URL))
	guides, err := c.ListGuides(context.Background(), &peasypdf.ListGuidesOptions{AudienceLevel: "beginner"})
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if len(guides) != 1 {
		t.Fatalf("expected 1 guide, got %d", len(guides))
	}
}

func TestSearch(t *testing.T) {
	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if q := r.URL.Query().Get("q"); q != "merge pdf" {
			t.Errorf("expected q=merge pdf, got q=%s", q)
		}
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(map[string]interface{}{
			"query": "merge pdf",
			"results": map[string]interface{}{
				"tools":    []map[string]interface{}{{"slug": "pdf-merge", "name": "PDF Merge"}},
				"formats":  []interface{}{},
				"glossary": []interface{}{},
			},
		})
	}))
	defer srv.Close()

	c := peasypdf.New(peasypdf.WithBaseURL(srv.URL))
	result, err := c.Search(context.Background(), "merge pdf", nil)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if result.Query != "merge pdf" {
		t.Errorf("expected query 'merge pdf', got '%s'", result.Query)
	}
	if len(result.Results.Tools) != 1 {
		t.Errorf("expected 1 tool result, got %d", len(result.Results.Tools))
	}
}

func TestNotFoundError(t *testing.T) {
	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusNotFound)
		w.Write([]byte(`{"detail":"Not found."}`))
	}))
	defer srv.Close()

	c := peasypdf.New(peasypdf.WithBaseURL(srv.URL))
	_, err := c.GetTool(context.Background(), "nonexistent")
	if err == nil {
		t.Fatal("expected error, got nil")
	}
	var notFound *peasypdf.NotFoundError
	if !errors.As(err, &notFound) {
		t.Fatalf("expected NotFoundError, got %T: %v", err, err)
	}
}

func TestServerError(t *testing.T) {
	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusInternalServerError)
		w.Write([]byte(`{"detail":"Internal server error."}`))
	}))
	defer srv.Close()

	c := peasypdf.New(peasypdf.WithBaseURL(srv.URL))
	_, err := c.ListTools(context.Background(), nil)
	if err == nil {
		t.Fatal("expected error, got nil")
	}
	var peasyErr *peasypdf.PeasyError
	if !errors.As(err, &peasyErr) {
		t.Fatalf("expected PeasyError, got %T: %v", err, err)
	}
	if peasyErr.StatusCode != 500 {
		t.Errorf("expected status 500, got %d", peasyErr.StatusCode)
	}
}
```

- [ ] **Step 7: Run tests to verify**

Run: `cd ~/dev/packages/peasy-pdf-go && go test -v ./...`
Expected: All tests PASS

- [ ] **Step 8: Write README.md with backlinks**

Create `README.md` following the Peasy README gold standard. Must include:
- Title + badges (Go Reference, License, Zero Dependencies)
- One-paragraph description with peasypdf.com link
- Quick Start code example
- API Client section with all 14 methods table
- Glossary & Guide search examples
- Learn More section with 10+ peasypdf.com URLs
- Also Available 5-language table
- Peasy Tools ecosystem table

Key URLs to include:
- `https://peasypdf.com` (main site)
- `https://peasypdf.com/pdf/` (tools index)
- `https://peasypdf.com/pdf/pdf-merge/` (specific tool)
- `https://peasypdf.com/guides/` (guides index)
- `https://peasypdf.com/glossary/` (glossary index)
- `https://peasypdf.com/formats/` (formats index)
- `https://peasypdf.com/api/docs/` (API docs)
- `https://peasypdf.com/api/openapi.json` (OpenAPI spec)

- [ ] **Step 9: Create LICENSE file**

```
MIT License

Copyright (c) 2026 Peasy Tools

Permission is hereby granted, free of charge, to any person obtaining a copy
...
```

- [ ] **Step 10: Commit and tag**

```bash
cd ~/dev/packages/peasy-pdf-go
git add -A
git commit -m "feat: Go client for PeasyPDF API — 14 methods, glossary/guide search, zero deps"
git tag v0.2.0
git push origin main --tags
```

### Task 2: Create remaining 7 Go packages

For each of the remaining 7 packages, replicate the peasy-pdf-go pattern with these substitutions:

| Package | Go package name | Default base URL | Repo name |
|---------|----------------|------------------|-----------|
| peasytext-go | `peasytext` | `https://peasytext.com` | `peasytools/peasytext-go` |
| peasy-image-go | `peasyimage` | `https://peasyimage.com` | `peasytools/peasy-image-go` |
| peasy-css-go | `peasycss` | `https://peasycss.com` | `peasytools/peasy-css-go` |
| peasy-compress-go | `peasycompress` | `https://peasytools.com` | `peasytools/peasy-compress-go` |
| peasy-document-go | `peasydocument` | `https://peasyformats.com` | `peasytools/peasy-document-go` |
| peasy-audio-go | `peasyaudio` | `https://peasyaudio.com` | `peasytools/peasy-audio-go` |
| peasy-video-go | `peasyvideo` | `https://peasyvideo.com` | `peasytools/peasy-video-go` |

Each package follows the **exact same file structure** as peasy-pdf-go. The only differences are:

1. **Package name** (e.g., `package peasyimage` instead of `package peasypdf`)
2. **DefaultBaseURL** constant
3. **Error prefix** in fmt.Errorf messages (e.g., `"peasyimage:"` instead of `"peasypdf:"`)
4. **go.mod module path** (e.g., `github.com/peasytools/peasy-image-go`)
5. **README backlinks** — each package links to its own category site
6. **Test import path** — matches the module path

The types.go, errors.go, and all 14 client methods are **identical in structure** across all 8 Go packages. The API endpoints are the same (`/api/v1/tools/`, etc.) because all Peasy sites serve the same unified multi-tenant API.

**Per package steps:**

- [ ] **Step 1: Create repo** — `gh repo create peasytools/{name} --public --description "..." --license MIT --clone`
- [ ] **Step 2: Create go.mod, errors.go, types.go, client.go, client_test.go**
  - Copy from peasy-pdf-go, find-replace package name, base URL, error prefix
- [ ] **Step 3: Write README.md** with package-specific backlinks
- [ ] **Step 4: Run tests** — `go test -v ./...`
- [ ] **Step 5: Commit and tag** — `git tag v0.2.0 && git push origin main --tags`

**Total: 7 packages × 5 steps = 35 steps. Run in batch.**

---

## Chunk 2: Phase 2 — TypeScript API Client (8 updates)

Add `client.ts` + `api-types.ts` to all 8 existing TypeScript packages. Zero new runtime dependencies (native `fetch`).

**Key constraint:** `types.ts` already exists with engine types. API types go in `api-types.ts` to avoid collision.

### Task 3: Add API client to peasy-pdf-js (template)

**Files:**
- Create: `packages/peasy-pdf-js/src/api-types.ts`
- Create: `packages/peasy-pdf-js/src/client.ts`
- Modify: `packages/peasy-pdf-js/src/index.ts`
- Modify: `packages/peasy-pdf-js/package.json`

- [ ] **Step 1: Create api-types.ts**

Create `packages/peasy-pdf-js/src/api-types.ts`:
```typescript
/** Options for paginated list requests. */
export interface ListOptions {
  page?: number;
  limit?: number;
  category?: string;
  search?: string;
}

/** Options for list_guides with audience_level. */
export interface ListGuidesOptions extends ListOptions {
  audienceLevel?: string;
}

/** Options for list_conversions with source/target. */
export interface ListConversionsOptions extends Omit<ListOptions, "category" | "search"> {
  source?: string;
  target?: string;
}

/** DRF paginated response. */
export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

/** A Peasy tool. */
export interface Tool {
  slug: string;
  name: string;
  description: string;
  category: string;
  url: string;
}

/** A tool category. */
export interface Category {
  slug: string;
  name: string;
  description: string;
  tool_count: number;
}

/** A file format. */
export interface Format {
  slug: string;
  name: string;
  extension: string;
  mime_type: string;
  category: string;
  description: string;
}

/** A format conversion. */
export interface Conversion {
  source: string;
  target: string;
  description: string;
  tool_slug: string;
}

/** A glossary term. */
export interface GlossaryTerm {
  slug: string;
  term: string;
  definition: string;
  category: string;
}

/** A how-to guide. */
export interface Guide {
  slug: string;
  title: string;
  description: string;
  category: string;
  audience_level: string;
  word_count: number;
}

/** An industry use case. */
export interface UseCase {
  slug: string;
  title: string;
  industry: string;
}

/** A Peasy site. */
export interface Site {
  name: string;
  domain: string;
  url: string;
}

/** Cross-model search result. */
export interface SearchResult {
  query: string;
  results: {
    tools: Tool[];
    formats: Format[];
    glossary: GlossaryTerm[];
  };
}
```

- [ ] **Step 2: Create client.ts**

Create `packages/peasy-pdf-js/src/client.ts`:
```typescript
import type {
  Category,
  Conversion,
  Format,
  GlossaryTerm,
  Guide,
  ListConversionsOptions,
  ListGuidesOptions,
  ListOptions,
  PaginatedResponse,
  SearchResult,
  Site,
  Tool,
  UseCase,
} from "./api-types.js";

/** PeasyPDF API client. Zero dependencies — uses native fetch. */
export class PeasyPdf {
  private baseUrl: string;

  constructor(baseUrl = "https://peasypdf.com") {
    this.baseUrl = baseUrl.replace(/\/+$/, "");
  }

  private async get<T>(path: string, params?: Record<string, string | number | undefined>): Promise<T> {
    const url = new URL(path, this.baseUrl);
    if (params) {
      for (const [k, v] of Object.entries(params)) {
        if (v !== undefined && v !== null) url.searchParams.set(k, String(v));
      }
    }
    const res = await fetch(url.toString());
    if (!res.ok) {
      const body = await res.text();
      throw new Error(`PeasyPdf API error: HTTP ${res.status} — ${body}`);
    }
    return res.json() as Promise<T>;
  }

  /** List tools (paginated). Filter by category or search query. */
  async listTools(opts?: ListOptions): Promise<PaginatedResponse<Tool>> {
    return this.get("/api/v1/tools/", opts);
  }

  /** Get a single tool by slug. */
  async getTool(slug: string): Promise<Tool> {
    return this.get(`/api/v1/tools/${encodeURIComponent(slug)}/`);
  }

  /** List tool categories (paginated). */
  async listCategories(opts?: Pick<ListOptions, "page" | "limit">): Promise<PaginatedResponse<Category>> {
    return this.get("/api/v1/categories/", opts);
  }

  /** List file formats (paginated). */
  async listFormats(opts?: ListOptions): Promise<PaginatedResponse<Format>> {
    return this.get("/api/v1/formats/", opts);
  }

  /** Get a single format by slug. */
  async getFormat(slug: string): Promise<Format> {
    return this.get(`/api/v1/formats/${encodeURIComponent(slug)}/`);
  }

  /** List format conversions (paginated). */
  async listConversions(opts?: ListConversionsOptions): Promise<PaginatedResponse<Conversion>> {
    return this.get("/api/v1/conversions/", opts);
  }

  /** List glossary terms (paginated). Search with opts.search. */
  async listGlossary(opts?: ListOptions): Promise<PaginatedResponse<GlossaryTerm>> {
    return this.get("/api/v1/glossary/", opts);
  }

  /** Get a single glossary term by slug. */
  async getGlossaryTerm(slug: string): Promise<GlossaryTerm> {
    return this.get(`/api/v1/glossary/${encodeURIComponent(slug)}/`);
  }

  /** List guides (paginated). Filter by category, audience level, or search. */
  async listGuides(opts?: ListGuidesOptions): Promise<PaginatedResponse<Guide>> {
    const params: Record<string, string | number | undefined> = { ...opts };
    if (opts?.audienceLevel) {
      params.audience_level = opts.audienceLevel;
      delete params.audienceLevel;
    }
    return this.get("/api/v1/guides/", params);
  }

  /** Get a single guide by slug. */
  async getGuide(slug: string): Promise<Guide> {
    return this.get(`/api/v1/guides/${encodeURIComponent(slug)}/`);
  }

  /** List industry use cases (paginated). */
  async listUseCases(opts?: ListOptions & { industry?: string }): Promise<PaginatedResponse<UseCase>> {
    return this.get("/api/v1/use-cases/", opts);
  }

  /** Search across tools, formats, and glossary. */
  async search(query: string, limit?: number): Promise<SearchResult> {
    return this.get("/api/v1/search/", { q: query, limit });
  }

  /** List all Peasy sites. */
  async listSites(): Promise<PaginatedResponse<Site>> {
    return this.get("/api/v1/sites/");
  }

  /** Get the OpenAPI 3.0.3 specification. */
  async openapiSpec(): Promise<Record<string, unknown>> {
    return this.get("/api/openapi.json");
  }
}
```

- [ ] **Step 3: Update index.ts to re-export client + api-types**

Modify `packages/peasy-pdf-js/src/index.ts` to add:
```typescript
// Engine exports (existing)
export type { PdfInfo, PdfMetadata, PageSize, OddEvenMode } from "./types.js";
export { parsePages, merge, split, rotate, reverse, deletePages, extractPages, oddEven, insertBlank, duplicatePages, info, getMetadata, setMetadata, stripMetadata } from "./engine.js";

// API Client (new)
export { PeasyPdf } from "./client.js";
export type {
  ListOptions,
  ListGuidesOptions,
  ListConversionsOptions,
  PaginatedResponse,
  Tool,
  Category,
  Format,
  Conversion,
  GlossaryTerm,
  Guide,
  UseCase,
  Site,
  SearchResult,
} from "./api-types.js";
```

- [ ] **Step 4: Bump version in package.json**

In `packages/peasy-pdf-js/package.json`, change `"version": "0.1.1"` → `"version": "0.2.0"`.

- [ ] **Step 5: Build and verify**

```bash
cd ~/dev/packages/peasy-pdf-js
npm run build
```
Expected: Build succeeds, `dist/` contains client.js, api-types.js, and their .d.ts files.

- [ ] **Step 6: Commit**

```bash
cd ~/dev/packages/peasy-pdf-js
git add src/client.ts src/api-types.ts src/index.ts package.json
git commit -m "feat: add API client with 14 methods, glossary/guide search — v0.2.0"
```

### Task 4: Add API client to remaining 7 TypeScript packages

For each of the remaining 7 packages, replicate the peasy-pdf-js pattern:

| Package repo | TS class name | Default base URL |
|-------------|---------------|------------------|
| peasytext-js | `PeasyText` | `https://peasytext.com` |
| peasy-image-js | `PeasyImage` | `https://peasyimage.com` |
| peasy-css-js | `PeasyCss` | `https://peasycss.com` |
| peasy-compress-js | `PeasyCompress` | `https://peasytools.com` |
| peasy-document-js | `PeasyDocument` | `https://peasyformats.com` |
| peasy-audio-js | `PeasyAudio` | `https://peasyaudio.com` |
| peasy-video-js | `PeasyVideo` | `https://peasyvideo.com` |

**Differences per package:**
1. Class name in `client.ts`
2. Default base URL
3. Existing engine exports in `index.ts` (preserve, add client exports)
4. `package.json` version bump

**Per package steps:**
- [ ] **Step 1:** Create `api-types.ts` (identical across all 8 — same API contract)
- [ ] **Step 2:** Create `client.ts` (change class name + base URL)
- [ ] **Step 3:** Update `index.ts` (preserve existing engine exports, add client + api-types)
- [ ] **Step 4:** Bump version in `package.json` to `0.2.0`
- [ ] **Step 5:** `npm run build` — verify success
- [ ] **Step 6:** Commit

**Note for peasytext-js:** The repo name is `peasytext-js` (no hyphen in "peasytext"). Class name: `PeasyText`. Check existing exports in `index.ts` before modifying.

---

## Chunk 3: Phase 3 — Rust Rewrite (8 updates)

Replace minimal stubs with real API client. Current state: only `version()` function + PeasyError enum.

**Dependencies to add:** `reqwest = { version = "0.12", features = ["json"] }`, `serde = { version = "1", features = ["derive"] }`, `serde_json = "1"`, `tokio = { version = "1", features = ["full"] }` (dev-dependency for tests).

### Task 5: Rewrite peasy-pdf-rs (template)

**Files:**
- Create: `packages/peasy-pdf-rs/src/client.rs`
- Create: `packages/peasy-pdf-rs/src/types.rs`
- Create: `packages/peasy-pdf-rs/src/error.rs`
- Modify: `packages/peasy-pdf-rs/src/lib.rs`
- Modify: `packages/peasy-pdf-rs/Cargo.toml`

- [ ] **Step 1: Update Cargo.toml**

In `packages/peasy-pdf-rs/Cargo.toml`, update:
```toml
[package]
name = "peasy-pdf"
version = "0.2.0"
edition = "2021"
description = "Rust client for PeasyPDF — PDF tools, glossary, and guides API"
license = "MIT"
repository = "https://github.com/peasytools/peasy-pdf-rs"
keywords = ["pdf", "peasy", "api-client", "tools"]
categories = ["api-bindings"]

[dependencies]
reqwest = { version = "0.12", features = ["json"] }
serde = { version = "1", features = ["derive"] }
serde_json = "1"
thiserror = "2"

[dev-dependencies]
tokio = { version = "1", features = ["full"] }
wiremock = "0.6"
```

- [ ] **Step 2: Create error.rs**

Create `packages/peasy-pdf-rs/src/error.rs`:
```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum PeasyError {
    #[error("HTTP request failed: {0}")]
    Http(#[from] reqwest::Error),

    #[error("Not found: {resource} '{identifier}'")]
    NotFound { resource: String, identifier: String },

    #[error("API error (HTTP {status}): {body}")]
    Api { status: u16, body: String },

    #[error("JSON decode error: {0}")]
    Decode(#[from] serde_json::Error),
}

pub type Result<T> = std::result::Result<T, PeasyError>;
```

- [ ] **Step 3: Create types.rs**

Create `packages/peasy-pdf-rs/src/types.rs`:
```rust
use serde::Deserialize;

#[derive(Debug, Deserialize)]
pub struct PaginatedResponse<T> {
    pub count: u32,
    pub next: Option<String>,
    pub previous: Option<String>,
    pub results: Vec<T>,
}

#[derive(Debug, Deserialize)]
pub struct Tool {
    pub slug: String,
    pub name: String,
    pub description: String,
    pub category: String,
    #[serde(default)]
    pub url: String,
}

#[derive(Debug, Deserialize)]
pub struct Category {
    pub slug: String,
    pub name: String,
    pub description: String,
    pub tool_count: u32,
}

#[derive(Debug, Deserialize)]
pub struct Format {
    pub slug: String,
    pub name: String,
    pub extension: String,
    pub mime_type: String,
    pub category: String,
    pub description: String,
}

#[derive(Debug, Deserialize)]
pub struct Conversion {
    pub source: String,
    pub target: String,
    pub description: String,
    pub tool_slug: String,
}

#[derive(Debug, Deserialize)]
pub struct GlossaryTerm {
    pub slug: String,
    pub term: String,
    pub definition: String,
    pub category: String,
}

#[derive(Debug, Deserialize)]
pub struct Guide {
    pub slug: String,
    pub title: String,
    pub description: String,
    pub category: String,
    pub audience_level: String,
    pub word_count: u32,
}

#[derive(Debug, Deserialize)]
pub struct UseCase {
    pub slug: String,
    pub title: String,
    pub industry: String,
}

#[derive(Debug, Deserialize)]
pub struct Site {
    pub name: String,
    pub domain: String,
    pub url: String,
}

#[derive(Debug, Deserialize)]
pub struct SearchResult {
    pub query: String,
    pub results: SearchCategories,
}

#[derive(Debug, Deserialize)]
pub struct SearchCategories {
    pub tools: Vec<Tool>,
    pub formats: Vec<Format>,
    pub glossary: Vec<GlossaryTerm>,
}

/// Options for paginated list requests.
#[derive(Default)]
pub struct ListOptions {
    pub page: Option<u32>,
    pub limit: Option<u32>,
    pub category: Option<String>,
    pub search: Option<String>,
}

/// Options for list_guides with audience level.
#[derive(Default)]
pub struct ListGuidesOptions {
    pub page: Option<u32>,
    pub limit: Option<u32>,
    pub category: Option<String>,
    pub audience_level: Option<String>,
    pub search: Option<String>,
}

/// Options for list_conversions with source/target.
#[derive(Default)]
pub struct ListConversionsOptions {
    pub page: Option<u32>,
    pub limit: Option<u32>,
    pub source: Option<String>,
    pub target: Option<String>,
}
```

- [ ] **Step 4: Create client.rs with all 14 methods**

Create `packages/peasy-pdf-rs/src/client.rs`:
```rust
use crate::error::{PeasyError, Result};
use crate::types::*;

const DEFAULT_BASE_URL: &str = "https://peasypdf.com";

pub struct Client {
    http: reqwest::Client,
    base_url: String,
}

impl Client {
    pub fn new() -> Self {
        Self {
            http: reqwest::Client::new(),
            base_url: DEFAULT_BASE_URL.to_string(),
        }
    }

    pub fn with_base_url(base_url: &str) -> Self {
        Self {
            http: reqwest::Client::new(),
            base_url: base_url.trim_end_matches('/').to_string(),
        }
    }

    async fn get(&self, path: &str, params: &[(&str, String)]) -> Result<bytes::Bytes> {
        let url = format!("{}{}", self.base_url, path);
        let filtered: Vec<(&str, &str)> = params
            .iter()
            .filter(|(_, v)| !v.is_empty())
            .map(|(k, v)| (*k, v.as_str()))
            .collect();

        let resp = self.http.get(&url).query(&filtered).send().await?;
        let status = resp.status().as_u16();

        if status == 404 {
            return Err(PeasyError::NotFound {
                resource: "resource".into(),
                identifier: path.into(),
            });
        }
        if status != 200 {
            let body = resp.text().await.unwrap_or_default();
            return Err(PeasyError::Api { status, body });
        }
        Ok(resp.bytes().await?)
    }

    fn list_params(opts: &ListOptions) -> Vec<(&'static str, String)> {
        let mut p = Vec::new();
        if let Some(v) = opts.page { p.push(("page", v.to_string())); }
        if let Some(v) = opts.limit { p.push(("limit", v.to_string())); }
        if let Some(ref v) = opts.category { p.push(("category", v.clone())); }
        if let Some(ref v) = opts.search { p.push(("search", v.clone())); }
        p
    }

    pub async fn list_tools(&self, opts: &ListOptions) -> Result<PaginatedResponse<Tool>> {
        let body = self.get("/api/v1/tools/", &Self::list_params(opts)).await?;
        Ok(serde_json::from_slice(&body)?)
    }

    pub async fn get_tool(&self, slug: &str) -> Result<Tool> {
        let body = self.get(&format!("/api/v1/tools/{}/", slug), &[]).await?;
        Ok(serde_json::from_slice(&body)?)
    }

    pub async fn list_categories(&self, opts: &ListOptions) -> Result<PaginatedResponse<Category>> {
        let mut params = Vec::new();
        if let Some(v) = opts.page { params.push(("page", v.to_string())); }
        if let Some(v) = opts.limit { params.push(("limit", v.to_string())); }
        let body = self.get("/api/v1/categories/", &params).await?;
        Ok(serde_json::from_slice(&body)?)
    }

    pub async fn list_formats(&self, opts: &ListOptions) -> Result<PaginatedResponse<Format>> {
        let body = self.get("/api/v1/formats/", &Self::list_params(opts)).await?;
        Ok(serde_json::from_slice(&body)?)
    }

    pub async fn get_format(&self, slug: &str) -> Result<Format> {
        let body = self.get(&format!("/api/v1/formats/{}/", slug), &[]).await?;
        Ok(serde_json::from_slice(&body)?)
    }

    pub async fn list_conversions(&self, opts: &ListConversionsOptions) -> Result<PaginatedResponse<Conversion>> {
        let mut params = Vec::new();
        if let Some(v) = opts.page { params.push(("page", v.to_string())); }
        if let Some(v) = opts.limit { params.push(("limit", v.to_string())); }
        if let Some(ref v) = opts.source { params.push(("source", v.clone())); }
        if let Some(ref v) = opts.target { params.push(("target", v.clone())); }
        let body = self.get("/api/v1/conversions/", &params).await?;
        Ok(serde_json::from_slice(&body)?)
    }

    pub async fn list_glossary(&self, opts: &ListOptions) -> Result<PaginatedResponse<GlossaryTerm>> {
        let body = self.get("/api/v1/glossary/", &Self::list_params(opts)).await?;
        Ok(serde_json::from_slice(&body)?)
    }

    pub async fn get_glossary_term(&self, slug: &str) -> Result<GlossaryTerm> {
        let body = self.get(&format!("/api/v1/glossary/{}/", slug), &[]).await?;
        Ok(serde_json::from_slice(&body)?)
    }

    pub async fn list_guides(&self, opts: &ListGuidesOptions) -> Result<PaginatedResponse<Guide>> {
        let mut params = Vec::new();
        if let Some(v) = opts.page { params.push(("page", v.to_string())); }
        if let Some(v) = opts.limit { params.push(("limit", v.to_string())); }
        if let Some(ref v) = opts.category { params.push(("category", v.clone())); }
        if let Some(ref v) = opts.audience_level { params.push(("audience_level", v.clone())); }
        if let Some(ref v) = opts.search { params.push(("search", v.clone())); }
        let body = self.get("/api/v1/guides/", &params).await?;
        Ok(serde_json::from_slice(&body)?)
    }

    pub async fn get_guide(&self, slug: &str) -> Result<Guide> {
        let body = self.get(&format!("/api/v1/guides/{}/", slug), &[]).await?;
        Ok(serde_json::from_slice(&body)?)
    }

    pub async fn list_use_cases(&self, opts: &ListOptions) -> Result<PaginatedResponse<UseCase>> {
        let mut params = Vec::new();
        if let Some(v) = opts.page { params.push(("page", v.to_string())); }
        if let Some(v) = opts.limit { params.push(("limit", v.to_string())); }
        if let Some(ref v) = opts.category { params.push(("industry", v.clone())); }
        if let Some(ref v) = opts.search { params.push(("search", v.clone())); }
        let body = self.get("/api/v1/use-cases/", &params).await?;
        Ok(serde_json::from_slice(&body)?)
    }

    pub async fn search(&self, query: &str, limit: Option<u32>) -> Result<SearchResult> {
        let mut params = vec![("q", query.to_string())];
        if let Some(v) = limit { params.push(("limit", v.to_string())); }
        let body = self.get("/api/v1/search/", &params).await?;
        Ok(serde_json::from_slice(&body)?)
    }

    pub async fn list_sites(&self) -> Result<PaginatedResponse<Site>> {
        let body = self.get("/api/v1/sites/", &[]).await?;
        Ok(serde_json::from_slice(&body)?)
    }

    pub async fn openapi_spec(&self) -> Result<serde_json::Value> {
        let body = self.get("/api/openapi.json", &[]).await?;
        Ok(serde_json::from_slice(&body)?)
    }
}

impl Default for Client {
    fn default() -> Self {
        Self::new()
    }
}
```

- [ ] **Step 5: Rewrite lib.rs**

Replace `packages/peasy-pdf-rs/src/lib.rs`:
```rust
pub mod client;
pub mod error;
pub mod types;

pub use client::Client;
pub use error::{PeasyError, Result};
pub use types::*;
```

- [ ] **Step 6: Remove old engine.rs (or keep if lopdf engine is desired)**

For peasy-pdf-rs, keep `engine.rs` as-is (it only has `version()`). The engine rewrite is out of scope — API client is the priority.

- [ ] **Step 7: Verify it compiles**

```bash
cd ~/dev/packages/peasy-pdf-rs
cargo check
```
Expected: Compiles without errors.

- [ ] **Step 8: Commit**

```bash
git add -A
git commit -m "feat: async API client with 14 methods, glossary/guide search — v0.2.0"
```

### Task 6: Rewrite remaining 7 Rust packages

Same pattern as peasy-pdf-rs. Per package:
- [ ] Update `Cargo.toml` (name, description, base URL in client.rs)
- [ ] Create `error.rs`, `types.rs`, `client.rs` (same structure, different error prefix)
- [ ] Rewrite `lib.rs`
- [ ] `cargo check`
- [ ] Commit

---

## Chunk 4: Phase 4 — Ruby API Client (8 updates)

Add `client.rb` to all 8 Ruby packages. Zero dependencies (stdlib Net::HTTP).

### Task 7: Add API client to peasy-pdf-rb (template)

**Files:**
- Create: `packages/peasy-pdf-rb/lib/peasy_pdf/client.rb`
- Modify: `packages/peasy-pdf-rb/lib/peasy_pdf.rb`
- Modify: `packages/peasy-pdf-rb/lib/peasy_pdf/version.rb`

- [ ] **Step 1: Create client.rb**

Create `packages/peasy-pdf-rb/lib/peasy_pdf/client.rb`:
```ruby
# frozen_string_literal: true

require "net/http"
require "json"
require "uri"

module PeasyPDF
  # REST API client for peasypdf.com.
  # Zero dependencies — uses Ruby stdlib only.
  class Client
    DEFAULT_BASE_URL = "https://peasypdf.com"

    def initialize(base_url: DEFAULT_BASE_URL)
      @base_url = base_url.chomp("/")
    end

    # --- Tools ---

    def list_tools(page: 1, limit: 50, category: nil, search: nil)
      get("/api/v1/tools/", page: page, limit: limit, category: category, search: search)
    end

    def get_tool(slug)
      get("/api/v1/tools/#{slug}/")
    end

    # --- Categories ---

    def list_categories(page: 1, limit: 50)
      get("/api/v1/categories/", page: page, limit: limit)
    end

    # --- Formats ---

    def list_formats(page: 1, limit: 50, category: nil, search: nil)
      get("/api/v1/formats/", page: page, limit: limit, category: category, search: search)
    end

    def get_format(slug)
      get("/api/v1/formats/#{slug}/")
    end

    # --- Conversions ---

    def list_conversions(page: 1, limit: 50, source: nil, target: nil)
      get("/api/v1/conversions/", page: page, limit: limit, source: source, target: target)
    end

    # --- Glossary ---

    def list_glossary(page: 1, limit: 50, category: nil, search: nil)
      get("/api/v1/glossary/", page: page, limit: limit, category: category, search: search)
    end

    def get_glossary_term(slug)
      get("/api/v1/glossary/#{slug}/")
    end

    # --- Guides ---

    def list_guides(page: 1, limit: 50, category: nil, audience_level: nil, search: nil)
      get("/api/v1/guides/", page: page, limit: limit, category: category,
                              audience_level: audience_level, search: search)
    end

    def get_guide(slug)
      get("/api/v1/guides/#{slug}/")
    end

    # --- Use Cases ---

    def list_use_cases(page: 1, limit: 50, industry: nil, search: nil)
      get("/api/v1/use-cases/", page: page, limit: limit, industry: industry, search: search)
    end

    # --- Search ---

    def search(query, limit: 20)
      get("/api/v1/search/", q: query, limit: limit)
    end

    # --- Sites ---

    def list_sites
      get("/api/v1/sites/")
    end

    # --- OpenAPI ---

    def openapi_spec
      get("/api/openapi.json")
    end

    private

    def get(path, **params)
      uri = URI("#{@base_url}#{path}")
      params.reject! { |_, v| v.nil? }
      uri.query = URI.encode_www_form(params) unless params.empty?
      response = Net::HTTP.get_response(uri)
      body = JSON.parse(response.body)
      unless response.is_a?(Net::HTTPSuccess)
        detail = body.is_a?(Hash) ? body.fetch("detail", "Unknown error") : response.body
        raise PeasyPDF::Error, "HTTP #{response.code}: #{detail}"
      end
      body
    end
  end
end
```

- [ ] **Step 2: Update lib/peasy_pdf.rb to require client**

Modify `packages/peasy-pdf-rb/lib/peasy_pdf.rb`:
```ruby
# frozen_string_literal: true

require_relative "peasy_pdf/version"
require_relative "peasy_pdf/engine"
require_relative "peasy_pdf/client"
```

- [ ] **Step 3: Bump version**

In `packages/peasy-pdf-rb/lib/peasy_pdf/version.rb`:
```ruby
module PeasyPDF
  VERSION = "0.2.0"
end
```

- [ ] **Step 4: Verify**

```bash
cd ~/dev/packages/peasy-pdf-rb
ruby -e "require_relative 'lib/peasy_pdf'; puts PeasyPDF::VERSION"
```
Expected: `0.2.0`

- [ ] **Step 5: Commit**

```bash
git add lib/peasy_pdf/client.rb lib/peasy_pdf.rb lib/peasy_pdf/version.rb
git commit -m "feat: add API client with 14 methods, glossary/guide search — v0.2.0"
```

### Task 8: Add API client to remaining 7 Ruby packages

Same pattern. Per package:

| Package repo | Ruby module | Default base URL |
|-------------|-------------|------------------|
| peasytext-rb | `PeasyText` | `https://peasytext.com` |
| peasy-image-rb | `PeasyImage` | `https://peasyimage.com` |
| peasy-css-rb | `PeasyCSS` | `https://peasycss.com` |
| peasy-compress-rb | `PeasyCompress` | `https://peasytools.com` |
| peasy-document-rb | `PeasyDocument` | `https://peasyformats.com` |
| peasy-audio-rb | `PeasyAudio` | `https://peasyaudio.com` |
| peasy-video-rb | `PeasyVideo` | `https://peasyvideo.com` |

- [ ] Create `client.rb` (change module name + base URL)
- [ ] Update entry file to require client
- [ ] Bump version to 0.2.0
- [ ] Verify
- [ ] Commit

---

## Chunk 5: Phase 5 — Python Updates + README Overhaul (40 READMEs)

### Task 9: Update Python API clients (8 packages)

Add missing `search` parameter to 4 list methods in each Python package.

**Files to modify per package:** `packages/peasy-{name}/src/peasy_{name}/api.py`

- [ ] **Step 1: Add `search` parameter to list_tools**

In each `api.py`, update `list_tools`:
```python
def list_tools(
    self, *, page: int = 1, limit: int = 50, category: str | None = None, search: str | None = None
) -> dict[str, Any]:
    """List tools (paginated). Filter by category slug or search query."""
    params: dict[str, Any] = {"page": page, "limit": limit}
    if category:
        params["category"] = category
    if search:
        params["search"] = search
    return self._get("/api/v1/tools/", params=params)
```

- [ ] **Step 2: Add `search` parameter to list_glossary**

```python
def list_glossary(
    self, *, page: int = 1, limit: int = 50, category: str | None = None, search: str | None = None
) -> dict[str, Any]:
    """List glossary terms (paginated). Filter by category or search query."""
    params: dict[str, Any] = {"page": page, "limit": limit}
    if category:
        params["category"] = category
    if search:
        params["search"] = search
    return self._get("/api/v1/glossary/", params=params)
```

- [ ] **Step 3: Add `search` + `audience_level` to list_guides**

```python
def list_guides(
    self, *, page: int = 1, limit: int = 50, category: str | None = None,
    audience_level: str | None = None, search: str | None = None
) -> dict[str, Any]:
    """List guides (paginated). Filter by category, audience level, or search query."""
    params: dict[str, Any] = {"page": page, "limit": limit}
    if category:
        params["category"] = category
    if audience_level:
        params["audience_level"] = audience_level
    if search:
        params["search"] = search
    return self._get("/api/v1/guides/", params=params)
```

- [ ] **Step 4: Add `search` parameter to list_use_cases**

```python
def list_use_cases(
    self, *, page: int = 1, limit: int = 50, industry: str | None = None, search: str | None = None
) -> dict[str, Any]:
    """List use cases (paginated). Filter by industry or search query."""
    params: dict[str, Any] = {"page": page, "limit": limit}
    if industry:
        params["industry"] = industry
    if search:
        params["search"] = search
    return self._get("/api/v1/use-cases/", params=params)
```

- [ ] **Step 5: Add `search` parameter to list_formats**

```python
def list_formats(
    self, *, page: int = 1, limit: int = 50, category: str | None = None, search: str | None = None
) -> dict[str, Any]:
    """List file formats (paginated). Filter by category or search query."""
    params: dict[str, Any] = {"page": page, "limit": limit}
    if category:
        params["category"] = category
    if search:
        params["search"] = search
    return self._get("/api/v1/formats/", params=params)
```

- [ ] **Step 6: Bump version to 0.2.0**

In each `pyproject.toml`, change `version = "0.1.1"` → `version = "0.2.0"`.

- [ ] **Step 7: Run ruff check + format**

```bash
cd ~/dev/packages/peasy-pdf
ruff check --fix src/ && ruff format src/
```

- [ ] **Step 8: Commit per package**

```bash
git add src/peasy_pdf/api.py pyproject.toml
git commit -m "feat: add search param to list methods, bump to v0.2.0"
```

### Task 10: Overhaul all 40 READMEs

Every README across all 5 languages × 8 packages gets updated with:

1. **Also Available** table (5 languages with registry links)
2. **Peasy Tools** ecosystem table (8 packages)
3. **Learn More** section with peasytools.com backlinks (10-15 URLs per README)
4. **Glossary & Guide search** code examples
5. **API Client** documentation section

**Template sections to add** (adapt language-specific code examples per language):

```markdown
## Also Available

| Language | Package | Install |
|----------|---------|---------|
| **Python** | [peasy-pdf](https://pypi.org/project/peasy-pdf/) | `pip install "peasy-pdf[api]"` |
| **TypeScript** | [peasy-pdf](https://www.npmjs.com/package/peasy-pdf) | `npm install peasy-pdf` |
| **Go** | [peasy-pdf-go](https://pkg.go.dev/github.com/peasytools/peasy-pdf-go) | `go get github.com/peasytools/peasy-pdf-go` |
| **Rust** | [peasy-pdf](https://crates.io/crates/peasy-pdf) | `cargo add peasy-pdf` |
| **Ruby** | [peasy-pdf](https://rubygems.org/gems/peasy-pdf) | `gem install peasy-pdf` |

## Learn More

- **Tools**: [PDF Merge](https://peasypdf.com/pdf/pdf-merge/) · [PDF Split](https://peasypdf.com/pdf/pdf-split/) · [All PDF Tools](https://peasypdf.com/pdf/)
- **Guides**: [How to Compress PDFs](https://peasypdf.com/guides/how-to-compress-pdf/) · [All Guides](https://peasypdf.com/guides/)
- **Glossary**: [What is PDF/A?](https://peasypdf.com/glossary/pdfa/) · [All Terms](https://peasypdf.com/glossary/)
- **Formats**: [PDF Format](https://peasypdf.com/formats/pdf/) · [All Formats](https://peasypdf.com/formats/)
- **API**: [REST API Docs](https://peasypdf.com/api/docs/) · [OpenAPI Spec](https://peasypdf.com/api/openapi.json)

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

**Per README steps:**
- [ ] Read current README to identify existing sections to preserve
- [ ] Add/update "API Client" section with language-appropriate examples
- [ ] Add "Also Available" table
- [ ] Add "Learn More" section with package-specific URLs
- [ ] Add "Peasy Tools" ecosystem table (bold current package)
- [ ] Commit

**Batch order:** Process by language (8 Python → 8 TypeScript → 8 Go → 8 Rust → 8 Ruby).

---

## Chunk 6: Phase 6 — Make Repos PUBLIC + Publish

### Task 11: Flip existing repos PRIVATE → PUBLIC

The 8 Go repos are already PUBLIC (created in Phase 1). The remaining 32 repos need flipping.

- [ ] **Step 1: Verify Go repos are public**

```bash
gh repo list peasytools --limit 50 --json name,visibility --jq '.[] | select(.name | endswith("-go")) | "\(.name): \(.visibility)"'
```
Expected: All 8 show `PUBLIC`

- [ ] **Step 2: Flip remaining 32 repos**

```bash
# List all private repos
gh repo list peasytools --limit 50 --visibility private --json name --jq '.[].name' | while read repo; do
  gh repo edit "peasytools/$repo" --visibility public
  echo "✅ $repo → PUBLIC"
done
```

- [ ] **Step 3: Verify all 40 repos are public**

```bash
gh repo list peasytools --limit 50 --json name,visibility --jq '.[] | "\(.name): \(.visibility)"' | sort
```
Expected: 40 repos, all PUBLIC.

### Task 12: Publish all updated packages

- [ ] **Step 1: Publish Python packages (8)**

```bash
for pkg in peasy-pdf peasy-image peasy-audio peasy-video peasy-css peasy-compress peasy-document peasytext; do
  cd ~/dev/packages/$pkg
  uv build && uv publish
  echo "✅ PyPI: $pkg"
  cd -
done
```

- [ ] **Step 2: Publish TypeScript packages (8)**

```bash
for pkg in peasy-pdf-js peasy-image-js peasy-audio-js peasy-video-js peasy-css-js peasy-compress-js peasy-document-js peasytext-js; do
  cd ~/dev/packages/$pkg
  npm run build && npm publish
  echo "✅ npm: $pkg"
  cd -
done
```

- [ ] **Step 3: Tag and push Go packages (8)**

Go packages auto-index on pkg.go.dev after tag push.

```bash
for pkg in peasy-pdf-go peasy-image-go peasy-audio-go peasy-video-go peasy-css-go peasy-compress-go peasy-document-go peasytext-go; do
  cd ~/dev/packages/$pkg
  git tag v0.2.0
  git push origin main --tags
  echo "✅ Go: $pkg"
  cd -
done
```

- [ ] **Step 4: Publish Rust packages (8)**

```bash
for pkg in peasy-pdf-rs peasy-image-rs peasy-audio-rs peasy-video-rs peasy-css-rs peasy-compress-rs peasy-document-rs peasytext-rs; do
  cd ~/dev/packages/$pkg
  cargo publish
  echo "✅ crates.io: $pkg"
  cd -
done
```

- [ ] **Step 5: Publish Ruby packages (8)**

Ruby requires MFA OTP per gem. Run interactively:

```bash
for pkg in peasy-pdf-rb peasy-image-rb peasy-audio-rb peasy-video-rb peasy-css-rb peasy-compress-rb peasy-document-rb peasytext-rb; do
  cd ~/dev/packages/$pkg
  gem build *.gemspec && gem push *.gem
  echo "✅ rubygems: $pkg"
  cd -
done
```

### Task 13: Verify all publications

- [ ] **Step 1: Verify PyPI**

```bash
for pkg in peasy-pdf peasy-image peasy-audio peasy-video peasy-css peasy-compress peasy-document peasytext; do
  version=$(pip index versions $pkg 2>/dev/null | head -1)
  echo "$pkg: $version"
done
```

- [ ] **Step 2: Verify npm**

```bash
for pkg in peasy-pdf peasy-image peasy-audio peasy-video peasy-css peasy-compress peasy-document peasytext; do
  version=$(npm view $pkg version 2>/dev/null)
  echo "$pkg: $version"
done
```

- [ ] **Step 3: Verify crates.io**

```bash
for pkg in peasy-pdf peasy-image peasy-audio peasy-video peasy-css peasy-compress peasy-document peasytext; do
  curl -s "https://crates.io/api/v1/crates/$pkg" | python3 -c "import sys,json; print(f'$pkg:', json.load(sys.stdin)['crate']['max_version'])"
done
```

- [ ] **Step 4: Verify rubygems**

```bash
for pkg in peasy-pdf peasy-image peasy-audio peasy-video peasy-css peasy-compress peasy-document peasytext; do
  version=$(gem list $pkg --remote | grep "^$pkg " | grep -oP '\([\d.]+\)')
  echo "$pkg: $version"
done
```

- [ ] **Step 5: Trigger pkg.go.dev indexing**

```bash
for pkg in peasy-pdf-go peasy-image-go peasy-audio-go peasy-video-go peasy-css-go peasy-compress-go peasy-document-go peasytext-go; do
  curl -s "https://pkg.go.dev/github.com/peasytools/$pkg" > /dev/null
  echo "Triggered: $pkg"
done
```

- [ ] **Step 6: Verify backlinks resolve**

```bash
# Spot-check key URLs
for url in \
  "https://peasypdf.com/pdf/pdf-merge/" \
  "https://peasypdf.com/guides/" \
  "https://peasypdf.com/glossary/" \
  "https://peasypdf.com/api/docs/" \
  "https://peasytools.com"; do
  status=$(curl -s -o /dev/null -w "%{http_code}" "$url")
  echo "$url: $status"
done
```

---

## Summary

| Phase | Packages | Action | New Files |
|-------|----------|--------|-----------|
| 1 | 8 Go | Create from scratch | 48 |
| 2 | 8 TypeScript | Add client.ts + api-types.ts | 16 |
| 3 | 8 Rust | Rewrite with API client | 24 |
| 4 | 8 Ruby | Add client.rb | 8 |
| 5 | 8 Python + 40 READMEs | Update API + README overhaul | 0 new, 48 modified |
| 6 | 40 repos | Flip to PUBLIC + publish | 0 |
| **Total** | **40 packages** | | **96 new + 48 modified** |
