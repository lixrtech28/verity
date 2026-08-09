from verity import Evidence, build_claims


def sample() -> Evidence:
    return Evidence(
        source_id="s1",
        url="https://example.com/a",
        title="Customer notes",
        text="Teams report that weekly reporting takes hours of manual work.",
    )


def test_claim_keeps_provenance():
    result = build_claims([sample()])
    assert len(result.claims) == 1
    claim = result.claims[0]
    assert claim.kind == "observation"
    assert claim.source_id == "s1"
    assert claim.source_url == "https://example.com/a"


def test_claim_id_is_stable():
    first = build_claims([sample()]).claims[0].claim_id
    second = build_claims([sample()]).claims[0].claim_id
    assert first == second


def test_hypotheses_are_separate_from_claims():
    result = build_claims([sample()])
    assert result.claims[0].kind == "observation"
    assert result.hypotheses
    assert result.human_review_required is True


def test_unrelated_text_is_not_promoted_to_evidence():
    item = Evidence(
        source_id="s2",
        url="https://example.com/b",
        title="Announcement",
        text="The company launched a new product in 2026.",
    )
    assert build_claims([item]).claims == ()
