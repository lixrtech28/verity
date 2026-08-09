from verity import Evidence, EvidenceGraph, Relation, build_claims, evaluate


def test_evaluator_flags_contradictions_and_unlinked_claims():
    evidence = [
        Evidence("s1", "https://example.com/a", "A", "The process is manual and slow."),
        Evidence("s2", "https://example.com/b", "B", "The process is not manual."),
    ]
    result = build_claims(evidence)
    first, second = result.claims
    graph = EvidenceGraph([
        Relation("s1", first.claim_id, "supports", "source s1 supports claim"),
        Relation(first.claim_id, second.claim_id, "contradicts", "claims conflict"),
    ])

    report = evaluate(evidence, result.claims, graph)

    assert report.status == "review"
    assert report.metrics["contradiction_count"] == 1
    assert any(f.code == "CONTRADICTION" for f in report.findings)
    assert any(f.code == "UNLINKED_CLAIM" for f in report.findings)


def test_evaluator_passes_fully_linked_graph():
    evidence = [Evidence("s1", "https://example.com/a", "A", "The process is manual and slow.")]
    result = build_claims(evidence)
    claim = result.claims[0]
    graph = EvidenceGraph([Relation("s1", claim.claim_id, "supports")])

    report = evaluate(evidence, result.claims, graph)

    assert report.status == "pass"
    assert report.metrics["error_count"] == 0
    assert report.metrics["warning_count"] == 0
