from src.opportunity_intelligence import Source, build_report, extract_findings


def test_extracts_pain_signals_with_provenance():
    source = Source(
        url="https://example.com/a",
        title="Customer notes",
        text="Teams report a manual reporting process. The product launched in 2025.",
    )
    findings = extract_findings([source])
    assert len(findings) == 1
    assert findings[0].kind == "pain_signal"
    assert findings[0].source_url == source.url
    assert findings[0].source_title == source.title
    assert len(findings[0].id) == 16


def test_duplicate_evidence_is_stable_and_deduplicated():
    source = Source(
        url="https://example.com/b",
        title="Interview",
        text="Customers say the workflow is expensive and slow. Customers say the workflow is expensive and slow.",
    )
    findings = extract_findings([source])
    assert len(findings) == 1
    assert findings[0].id == extract_findings([source])[0].id


def test_report_preserves_evidence_and_requires_approval():
    source = Source(
        url="https://example.com/c",
        title="Interview",
        text="Customers say the workflow is expensive and slow.",
    )
    report = build_report([source])
    assert report["schema_version"] == "0.2"
    assert report["findings"][0]["evidence"]["url"] == source.url
    assert report["hypotheses"][0]["status"] == "hypothesis"
    assert report["human_approval_required"] is True
