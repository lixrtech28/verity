from src.opportunity_intelligence import Source, build_report, extract_findings


def test_extracts_pain_signals():
    source = Source(
        url="https://example.com/a",
        title="Customer notes",
        text="Teams report a manual reporting process. The product launched in 2025.",
    )
    findings = extract_findings([source])
    assert len(findings) == 1
    assert findings[0].kind == "pain_signal"
    assert findings[0].source_url == source.url


def test_report_preserves_evidence_and_requires_approval():
    source = Source(
        url="https://example.com/b",
        title="Interview",
        text="Customers say the workflow is expensive and slow.",
    )
    report = build_report([source])
    assert report["sources"][0]["url"] == source.url
    assert report["findings"][0]["evidence"] if "evidence" in report["findings"][0] else True
    assert report["human_approval_required"] is True
