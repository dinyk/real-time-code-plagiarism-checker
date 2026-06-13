from algorithms.rabin_karp import RabinKarpDetector, ReferenceCode


def test_detects_copied_python_fragment():
    reference = ReferenceCode(
        id=1,
        filename="binary.py",
        language="Python",
        code="""def binary_search(arr, target):
    low = 0
    high = len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
    return -1
""",
    )
    submitted = "# student solution\n" + reference.code + "\nprint('done')"

    result = RabinKarpDetector(chunk_size=40).find_matches(submitted, [reference])

    assert result["matches_found"] > 0
    assert result["similarity_percentage"] > 70
    assert result["highlight_ranges"]


def test_returns_zero_for_original_code():
    reference = ReferenceCode(id=1, filename="factorial.cpp", language="C++", code="int factorial(int n) { return n <= 1 ? 1 : n * factorial(n - 1); }")
    submitted = "def add(a, b):\n    return a + b\n"

    result = RabinKarpDetector(chunk_size=25).find_matches(submitted, [reference])

    assert result["matches_found"] == 0
    assert result["similarity_percentage"] == 0.0


def test_short_reference_is_supported():
    reference = ReferenceCode(id=1, filename="tiny.java", language="Java", code="return true;")
    submitted = "if (ok) { return true; }"

    result = RabinKarpDetector(chunk_size=80).find_matches(submitted, [reference])

    assert result["matches_found"] == 1


def test_mixed_short_and_long_references_are_checked_together():
    short_ref = ReferenceCode(id=1, filename="tiny.java", language="Java", code="return true;")
    long_ref = ReferenceCode(
        id=2,
        filename="loop.py",
        language="Python",
        code="""for index in range(10):
    total += index
    print(total)
""",
    )
    submitted = "if (ok) { return true; }\n" + long_ref.code

    result = RabinKarpDetector(chunk_size=30).find_matches(submitted, [short_ref, long_ref])
    filenames = {match["reference_filename"] for match in result["matches"]}

    assert "tiny.java" in filenames
    assert "loop.py" in filenames
