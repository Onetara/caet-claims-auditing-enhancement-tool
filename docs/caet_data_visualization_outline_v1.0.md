CAET: Claims Auditing Enhancement Tool
Methodology

Dr. Stacy Lisa Toriola, MD, MSc


Abstract

The Claims Auditing Enhancement Tool (CAET) is a fraud risk-scoring
system developed to identify potentially fraudulent durable medical
equipment (DME) claims within Medicare data. Using the Centers for
Medicare & Medicaid Services (CMS) 2023 DME by Supplier and Service dataset,
two hypotheses were tested: general DME fraud detection (H1) and
intermittent catheter fraud detection (H2). Statistical signal
detection combined with a member-call verification amplifier was used
to produce tiered composite risk scores for providers. Results
indicated that statistical signals alone were insufficient to
distinguish legitimate high-volume providers from fraudulent ones, and
that member-call data was required to surface high-risk cases.

Research Question

Can statistical fraud signals, derived from Medicare DME claims data
alone, reliably distinguish legitimate high-volume providers from
fraud rings, or is additional corroborating information required to
achieve a reliable risk classification?

Method

Data Source

Data were drawn from the CMS Medicare DME by Supplier and Service 2023
dataset, comprising 463,784 claim-level records after signal
processing (dme_with_signals.csv). Member-call data used in this study
are simulated for demonstration (41 calls).

Design

Two hypotheses were defined and tested independently:

    H1 (General DME Fraud Detection). Composite risk scoring was
    applied to the full population of 59,592 providers, with a 70%
    threshold for classification as high risk.

    H2 (Intermittent Catheter Fraud Detection). Composite risk scoring
    was applied to the 206 suppliers billing 8 or more distinct
    catheter codes. The 41 of these located in the five high-risk
    catheter states (OK, FL, NY, TX, GA) formed the test pool, with a
    75% threshold for classification as high risk.

    Rationale for H2. General DME scoring multiplies each claim by a
    category risk weight and uses cutoffs pooled across all equipment
    types. Both dampen catheter signals, so catheter fraud can go
    undetected relative to other DME categories. H2 therefore uses
    catheter-specific cutoffs and adds catheter bundling signals. This
    rationale draws on the author's claims-adjustment experience and
    CMS data.

Procedure

For each hypothesis, provider-level signals were aggregated into a
composite score. Two scoring conditions were tested for H1: (a) 
statistical signals alone, applied to the full 59,592-provider
population, and (b) statistical signals combined with member-call
verification data as a risk amplifier. For H2, composite scores were
generated for the 206 catheter suppliers, and the 41 in the five
high-risk states were tested using the combined scoring approach.

Scoring Parameters

    Tiers (composite score, 0 to 100): LOW below 40, MEDIUM 40 to 59,
    HIGH 60 to 79, CRITICAL 80 and above. Provider score = highest
    row score for each signal.

    H1 composite weights: member calls 0.35, upcoding 0.25, volume
    0.20, rental 0.10, geographic 0.10.
      Category risk weight (CMS improper payment rate, multiplies
      upcoding, volume and rental points), each divided by the highest
      (0.576) so the top category scores at full strength: surgical
      dressing 1.000, orthotic 0.891, CGM 0.438, catheter 0.313,
      PAP/CPAP 0.217, other 0.174.
      Upcoding: charge-to-allowed ratio at or above 11.50 (90th
      percentile) 60 points, at or above 29.78 (99th) 100 points.
      Volume: claims per beneficiary at or above 5.67 (90th) 60
      points, at or above 8.80 (99th) 100 points.
      Rental: provider rental ratio at its 90th / 99th percentile,
      60 / 100 points.
      Geographic: CA, FL, TX, NY, IL +30, urban +15 (in those states),
      state volume outlier (above state 95th percentile) +20. Cap 100.

    H2 composite weights: catheter bundling 0.25, units per claim 0.15,
    member calls 0.25, volume 0.15, upcoding 0.10, geographic 0.10.
      Bundling: 14+ catheter codes +55, 8 to 13 +35, 5 to 7 +15;
      straight and coude codes (A4351, A4352) billed together +30;
      accessories without a primary code +25; Oklahoma with more than
      100 catheter claims +20. Cap 100.
      Units per claim: services divided by claims, compared only with
      rows of the same HCPCS code (codes with 20+ supplier rows).
      At or above that code's 90th percentile 60 points, 99th 100
      points; the supplier takes its highest row. Claims show what was
      billed; only member calls show what was received.
      Volume: highest claims per beneficiary above 9.12 +40, average
      above 5.35 +25, total claims above 50,000 +20.
      Upcoding: highest charge-to-allowed ratio above 4.14 +50,
      average above 1.52 +30.
      Geographic: OK, FL, NY, TX, GA +30; OK +10 more.
      Override floor: a provider with 14+ catheter codes and a
      geographic score of 30 or more has a minimum score of 65
      (HIGH). A provider with HIGH bundling and at least one more
      flag has a minimum of 42 (MEDIUM). The floor applies before and
      after member calls.

    Member-call points per validated call: no diagnosis match 60, no
    consent 55, never received 50, wrong item 40, rental not returned
    40. Multiplier by distinct members: 2 members x1.25, 3 or more
    x1.50. Cap 100.

Results

H1. When tested against the full provider population using
statistical signals alone (no member calls applied), 0% of providers
scored in the HIGH or CRITICAL risk tiers. This indicated that
member-call data functions as a required amplifier of the composite
score rather than an optional enhancement.

H2. Testing the full 41-provider test pool with the combined
scoring approach yielded the following tier distribution: 8 providers
(19.5%) scored HIGH, 24 providers scored MEDIUM, and 9 providers
scored LOW. This result fell below the 75% pass threshold set for the
hypothesis.

Discussion

Together, the H1 and H2 findings confirm that statistical claims
signals alone are not sufficient to reliably classify DME fraud risk.
Member-call verification data materially changes classification
outcomes and should be treated as a necessary component of the
scoring model rather than a supplementary one.

Tools and Technology

Data processing and scoring were conducted in Python (pandas). Data
visualization was produced using Matplotlib and Seaborn for exploratory
charts, with Power BI used for the interactive dashboard.

References

Centers for Medicare & Medicaid Services. (2023). Medicare durable
    medical equipment, devices & supplies: By supplier and service
    [Data set]. U.S. Department of Health and Human Services.

Published Date: 08/07/2026
