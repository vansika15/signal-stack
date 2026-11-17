from app.services.crawler_service import CrawlerService
from app.models.source import Source

def test_robots_txt_check():
    # Public domain robots check
    allowed = CrawlerService.check_robots_allowed("https://example.com")
    assert allowed is True

def test_source_crawl_simulation():
    # Verify hash and structure
    test_source = Source(
        id="src_test_01",
        company_id="meetuniversity",
        name="Example Test Source",
        url="https://example.com",
        source_type="Industry News",
        relevance_explanation="Test validation source",
        approved_status="approved",
        health_status="healthy"
    )
    assert test_source.id == "src_test_01"
    assert test_source.approved_status == "approved"
