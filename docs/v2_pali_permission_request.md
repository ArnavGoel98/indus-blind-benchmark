# Draft: permission request to SuttaCentral (Pali root texts)

Status: **draft for the project owner to send** (SuttaCentral forum, https://discourse.suttacentral.net,
the channel their licensing page names). Not sent. Written 2026-10-24.

**Why it is needed.** SuttaCentral's licensing page (read 2026-10-24) says the original Pali texts are in
the public domain, and adds: "We politely request that our content not be scraped or used in any way for
the creation of datasets for generative AI or similar." Our use is not generative AI, but it does build a
benchmark dataset from the text, which may count as "or similar". The request has no legal force; the
project's rule is to ask rather than decide for them. Of the other routes checked, VRI's text is
non-commercial only (plan, 2026-10-11), Project Gutenberg has no Pali text (catalogue searched 2026-10-24),
and public-domain printed editions would need OCR, which the project excludes.

---

**Subject:** Permission question: Pali root texts as a reference corpus in a decipherment benchmark

Dear SuttaCentral team,

I run a small research project, the Indus Blind Decipherment Benchmark (IBDB). It tests whether published
computational decipherment methods can recover the sign values of a known language written in an
artificially "unknown" script. The methods are statistical (frequency matching and expectation-maximisation
over sign-to-sound mappings). No neural network or generative model is trained or used.

One test gives each method a related language as a reference. For Sanskrit we would like to use Pali,
and we would like to ask whether you are comfortable with us using the Mahāsaṅgīti root text (Pali only,
no translations) of a few collections (for example DN and MN) as follows:

- the text is converted to sound units (IAST letters) and used only to count unit and word frequencies
  and to score the methods' outputs against a table of regular Sanskrit-to-Pali sound correspondences
  taken from Geiger (1916);
- no machine-learning model, generative or otherwise, is trained on it;
- we would not redistribute the text; the repository would hold a script that fetches it from your
  `bilara-data` repository, with attribution, and only derived numbers (scores, frequencies) would be
  published;
- the work is non-commercial and open source.

Your licensing page asks that your content not be used to create datasets for generative AI "or similar".
We do not want to read that request narrowly to suit ourselves, so we are asking directly. If you would
prefer that we do not use the texts, we will not, and will say in our paper that the Pali comparison was
left out at SuttaCentral's request.

Thank you for your work and for considering this.

[name, affiliation, contact; repository link]
