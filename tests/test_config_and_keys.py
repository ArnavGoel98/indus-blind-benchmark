import gzip
import hashlib

from ibdb import config
from ibdb.corpus import AnswerKey, Corpus


def test_every_target_has_citation_and_verification_flag():
    t = config.targets()
    for name, spec in t["targets"].items():
        assert spec.get("citation"), f"{name} lacks a citation"
        assert "verified" in spec, f"{name} lacks a verified flag"
        cits = [spec["citation"]] if isinstance(spec["citation"], str) else spec["citation"]
        for c in cits:
            assert c in t["references"], f"{name}: citation {c} not in references"


def test_every_source_records_license_and_url():
    s = config.sources()
    for name, spec in {**s["languages"], **s["controls"]}.items():
        assert spec.get("license"), name
        if spec.get("method"):
            assert spec.get("url") or spec.get("url_pattern") or spec.get("file_url"), name


def test_key_commitment_roundtrip(tmp_path, toy_source):
    from ibdb.generator.build import Knobs, make_corpus
    from ibdb.generator.script import ScriptSpec
    c, k, _ = make_corpus(toy_source, ScriptSpec(), 100, 4.4, 0, Knobs())
    digest = k.save(tmp_path / "k.key.json.gz")
    assert hashlib.sha256(gzip.decompress((tmp_path / "k.key.json.gz").read_bytes())).hexdigest() == digest
    k2 = AnswerKey.load(tmp_path / "k.key.json.gz")
    assert k2.sign_values == k.sign_values
    c.save(tmp_path / "c.json.gz")
    c2 = Corpus.load(tmp_path / "c.json.gz")
    assert [t.tolist() for t in c2.texts] == [t.tolist() for t in c.texts]
    assert "sign_values" not in (tmp_path / "c.json.gz").read_bytes().decode("latin-1")


def test_answer_keys_are_gitignored():
    from ibdb.paths import project_root
    gi = (project_root() / ".gitignore").read_text()
    assert "private/" in gi


def test_sumerian_excluded_from_challenge_until_cdli_confirms():
    assert "sumerian" in config.experiment()["challenge"]["exclude_sources"]


def test_em_has_original_and_revised_rules_and_matcher_is_not_called_neural():
    from ibdb.methods.decipher import CognateMatcher, KnightEM, KnightEMOriginal
    assert KnightEM.rule == "revised" and KnightEMOriginal.rule == "original"
    assert CognateMatcher.name == "em_cognate_matcher"
    assert "NO neural network" in CognateMatcher.deviations
